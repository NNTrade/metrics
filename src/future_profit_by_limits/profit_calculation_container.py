import pandas as pd
from NNTrade.common.direction import direction
from ..future_extrem_deviation import get_extrem_of, ExtreamType
from ..future_extrem_deviation.constant import get_value_col, get_shift_col, SHIFT_OF_BASE, EXTREM_OF_BASE, IDX_OF_BASE
from .constant.output_col_name import PROFIT, CLOSE_PRICE, SHIFT_TO_CLOSE, IDX_OF_CLOSE, TYPE_OF_CLOSE
from .constant.closing_types import ClosingType
from NNTrade.common.candle_col_name import OPEN, CLOSE

class ProfitCalculationContainer:
  
  def __init__(self,quote_df:pd.DataFrame, income_extrem_df: pd.DataFrame,loss_extrem_df:pd.DataFrame, 
               income_limit:float, loss_limit:float, period_limit:int,
               trading_direction:direction) -> None:
    self.income_limit:float = income_limit
    self.loss_limit:float = loss_limit
    self.period_limit:int = period_limit
    self.trading_dir = trading_direction
    
    self.quote_df:pd.DataFrame = quote_df
    self.income_extrem_df: pd.DataFrame = income_extrem_df
    self.income_extrem_sr:pd.Series = income_extrem_df[EXTREM_OF_BASE]
    
    self.loss_extrem_df:pd.DataFrame = loss_extrem_df
    
    self.clear_cache()
    
  def clear_cache(self):
    self.__close_price_sr = None
    self.__profit_sr = None
    self.__income_sr = None
    self.__loss_sr = None
    self.__shift_to_close_sr = None
    self.__idx_of_close_sr = None
    self.__type_of_close_sr = None
    
  @property
  def type_of_close_sr(self)->pd.Series:
    if self.__type_of_close_sr is None:
      self.__type_of_close_sr = self.__get_type_of_close_sr()
    return self.__type_of_close_sr
   
  def __get_type_of_close_sr(self)->pd.Series:
    _ret_sr = pd.Series(ClosingType.OnClose, index=self.income_extrem_df.index)
    
    loss_filter = self._filter_loss_limit_reach_first()
    _ret_sr[loss_filter] = ClosingType.OnLossLimit
    
    # add positive profit
    income_filter = self._filter_income_limit_reach_first()
    _ret_sr[income_filter] = ClosingType.OnIncomeLimit
    
    return _ret_sr.rename(TYPE_OF_CLOSE)
  
  @property
  def income_shift_sr(self)->pd.Series:
     return self.income_extrem_df[SHIFT_OF_BASE]
   
  @property
  def loss_shift_sr(self)->pd.Series:
     return self.loss_extrem_df[SHIFT_OF_BASE]
  
  @property
  def income_sr(self)->pd.Series:
    if self.__income_sr is None:
      self.__income_sr = (self.trading_dir.value * (self.income_extrem_df[EXTREM_OF_BASE] - self.quote_df[OPEN]) / self.quote_df[OPEN]).round(5)
      self.__income_sr.loc[self.__income_sr > self.income_limit] = self.income_limit
    return self.__income_sr
  
  @property
  def loss_sr(self)->pd.Series:
    if self.__loss_sr is None:
      self.__loss_sr = (self.trading_dir.value * (self.loss_extrem_df[EXTREM_OF_BASE] - self.quote_df[OPEN]) / self.quote_df[OPEN]).round(5)
      self.__loss_sr.loc[self.__loss_sr < -self.loss_limit] = -self.loss_limit
    return self.__loss_sr
  
  def __add_negative_and_positive_effects(self, base_sr:pd.Series, working_column:str)->pd.Series:
     # add negative profit
    loss_filter = self._filter_loss_limit_reach_first()
    base_sr.loc[loss_filter] = self.loss_extrem_df[working_column][loss_filter]
    
    # add positive profit
    income_filter = self._filter_income_limit_reach_first()
    base_sr.loc[income_filter] = self.income_extrem_df[working_column][income_filter]
  
    return base_sr
  
  @property
  def shift_to_close_sr(self)->pd.Series:
    if self.__shift_to_close_sr is None:
      self.__shift_to_close_sr = self.__get_shift_to_close_sr()
    return self.__shift_to_close_sr
  
  def __get_shift_to_close_sr(self)->pd.Series:
    # get all on close
    _ret_sr = pd.Series(self.period_limit-1, index=self.income_extrem_df.index)
    
    return self.__add_negative_and_positive_effects(_ret_sr, SHIFT_OF_BASE).rename(SHIFT_TO_CLOSE)
  
  @property
  def idx_of_close_sr(self)->pd.Series:
    if self.__idx_of_close_sr is None:
      self.__idx_of_close_sr = self.__get_idx_of_close_sr()
    return self.__idx_of_close_sr
  
  def __get_idx_of_close_sr(self)->pd.Series:
    # get all on close
    _ret_sr = pd.Series(self.quote_df.index, index=self.quote_df.index).shift(-(self.period_limit-1))
    
    return self.__add_negative_and_positive_effects(_ret_sr, IDX_OF_BASE).rename(IDX_OF_CLOSE)
  
  @property
  def close_price_sr(self)->pd.Series:
    if self.__close_price_sr is None:
      self.__close_price_sr = self.__get_close_price_sr()
    return self.__close_price_sr
  
  def __get_close_price_sr(self)->pd.Series:
    # get all on close
    _ret_sr =  self.quote_df[CLOSE].shift(-(self.period_limit-1))
    
    return self.__add_negative_and_positive_effects(_ret_sr, EXTREM_OF_BASE).rename(CLOSE_PRICE)
  
  @property
  def profit_sr(self)->pd.Series:
    if self.__profit_sr is None:
      self.__profit_sr = self.__get_profit_sr()
    return self.__profit_sr
  
  def __get_profit_sr(self)->pd.Series:
    _ret_profit =  (self.trading_dir.value * (self.close_price_sr - self.quote_df[OPEN]) / self.quote_df[OPEN]).round(5)
    return _ret_profit.rename(PROFIT)
  
  def _filter_income_reach_extrem_before_loss_reach_limit(self)->pd.Series:
    return (self.income_shift_sr < self.loss_shift_sr) | (self.loss_sr > -self.loss_limit)
   
  def _filter_income_limit_reach_first(self):
    return (self.income_sr >= self.income_limit) & (self._filter_income_reach_extrem_before_loss_reach_limit())
  
  def _filter_loss_reach_extrem_before_income_reach_limit(self)->pd.Series:
    return (self.loss_shift_sr <= self.income_shift_sr) | (self.income_sr < self.income_limit)
  
  def _filter_loss_limit_reach_first(self):
     return (self.loss_sr <= -self.loss_limit) & (self._filter_loss_reach_extrem_before_income_reach_limit())