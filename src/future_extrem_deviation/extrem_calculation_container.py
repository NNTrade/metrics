import pandas as pd
from .extrem_type import ExtreamType
from typing import Tuple

class ExtremCalculationContainer:
  def __init__(self,open_sr:pd.Series, extr_value_sr:pd.Series ,extrem_type:ExtreamType, limit:float,period_limit:int = None) -> None:
    if limit <= 0:
      raise AttributeError("Limit must be positive number")
    if period_limit is not None and period_limit <=0:
      raise AttributeError("Period limit must be >= 1")
    self.open_sr = open_sr
    self.extrem_type = extrem_type
    self.limit = limit
    self.sided_limit = extrem_type.value * limit 
    self.extr_value_sr = extr_value_sr
    self.shift_limit = period_limit if period_limit is not None else len(extr_value_sr.index)
    pass
  
  def __get_new_value_rel_sr(self,value_sr: pd.Series):
    using_open_sr = self.open_sr.loc[value_sr.index]
    new_rel_sr:pd.Series = value_sr / using_open_sr - 1 #(new_value_sr  - using_open_sr) / using_open_sr
    new_value_sr = value_sr.copy()
    over_limit_sr = (self.extrem_type.value * new_rel_sr - self.limit) > 0
    if len(over_limit_sr) > 0:
      new_rel_sr[over_limit_sr] = self.sided_limit
      new_value_sr[over_limit_sr] = (self.sided_limit + 1) * using_open_sr[over_limit_sr]
    return new_value_sr,new_rel_sr

  def get_extrem_with_lim(self)->Tuple[pd.Series,pd.Series]:
    extremum_value_sr, extremum_relation_sr = self.__get_new_value_rel_sr(self.extr_value_sr)
    extremum_shift_sr = pd.Series(0, index=extremum_value_sr.index)
    
    for shift in range(1, self.shift_limit):
        cur_values_sr = self.extr_value_sr.shift(-shift)
        new_value_sr, new_rel_sr = self.__get_new_value_rel_sr(cur_values_sr[self.__get_filter_new_extrem_better_than_current(extremum_value_sr, cur_values_sr) &
                                                                                    self.__get_filter_rel_sr_not_overstep_limit(extremum_relation_sr)])
  
        extremum_value_sr.loc[new_value_sr.index] = new_value_sr
        extremum_shift_sr.loc[new_value_sr.index] = shift
        extremum_relation_sr.loc[new_value_sr.index] = new_rel_sr
        if self.__check_if_all_rel_sr_overstep_limit(extremum_relation_sr):
          break
        
    return extremum_relation_sr, extremum_value_sr, extremum_shift_sr
  
  def __get_filter_new_extrem_better_than_current(self, extremum_value_sr:pd.Series, cur_values_sr:pd.Series)->pd.Series:
    """get pandas filter for extream values DataFrame(self.shifted_v_df), \n
       where value from cur_values_sr is better than current value in extremum_value_sr

    Args:
        extremum_value_sr (pd.Series): current extremum values
        cur_extrem_sr (pd.Series): current price values

    Returns:
        pd.Series: Pandas filter
    """
    return (self.extrem_type.value * ( cur_values_sr - extremum_value_sr) > 0)

  def __get_filter_rel_sr_not_overstep_limit(self, rel_sr:pd.Series)->pd.Series:
    """get pandas filter for relation series (rel_sr), \n
       where value has not overcrossed limit

    Args:
        rel_sr (pd.Series): relation series

    Returns:
        pd.Series : Pandas filter
    """
    return (self.extrem_type.value * rel_sr - self.limit < 0)

  def __check_if_all_rel_sr_overstep_limit(self, rel_sr:pd.Series)->bool:
    """check if all elements in relation series (rel_sr) has overcrossed limit

    Args:
        rel_sr (pd.Series): relation series

    Returns:
        pd.Series: boolean
    """
    return (self.extrem_type.value * rel_sr - self.limit >= 0).all()
