import pandas as pd
from NNTrade.common.direction import direction
from ..future_extrem_deviation import get_extrem_of, ExtreamType
from .profit_calculation_container import ProfitCalculationContainer
  
def get_profit_by_limit(quote_df:pd.DataFrame, trading_direction:direction, income_limit:float, loss_limit:float, period_limit:int):
  """Get profit by limits

  Args:
      quote_df (pd.DataFrame): quotes
      trading_direction (direction): trading directions
      income_limit (float): limit of income in relation form (1 = 100%)
      loss_limit (float): limit of loss in relation form (1 = 100%). Positive number
      period_limit (int): limit of period of open deal. 1 - only current candle, N - current candle and N-1 future candle
  """
  if trading_direction == direction.Long:
    income_extrem_df = get_extrem_of(quote_df, period_limit,ExtreamType.High,income_limit, True)
    loss_extrem_df = get_extrem_of(quote_df, period_limit,ExtreamType.Low, loss_limit, True)
  elif trading_direction == direction.Short:
    income_extrem_df = get_extrem_of(quote_df, period_limit,ExtreamType.Low, income_limit, True)
    loss_extrem_df = get_extrem_of(quote_df, period_limit,ExtreamType.High, loss_limit, True)
  pcc = ProfitCalculationContainer(quote_df, income_extrem_df, loss_extrem_df, income_limit, loss_limit, period_limit, trading_direction)
  
  return pd.DataFrame([pcc.profit_sr, pcc.close_price_sr, pcc.shift_to_close_sr, pcc.idx_of_close_sr, pcc.type_of_close_sr]).T