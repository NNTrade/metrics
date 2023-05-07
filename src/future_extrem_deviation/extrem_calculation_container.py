import pandas as pd
from .extrem_type import ExtreamType
from typing import Tuple


class ExtremCalculationContainer:
  def __init__(self,open_sr:pd.Series, shifted_v_df:pd.DataFrame,extrem_type:ExtreamType, limit:float) -> None:
    self.open_sr = open_sr
    self.shifted_v_df = shifted_v_df
    self.extrem_type = extrem_type
    self.limit = limit
    self.sided_limit = extrem_type.value * limit 
    pass
  
  def __get_new_value_rel_sr(self,new_value_sr: pd.Series):
    using_open_sr = self.open_sr.loc[new_value_sr.index]
    new_rel_sr:pd.Series = new_value_sr / using_open_sr - 1 #(new_value_sr  - using_open_sr) / using_open_sr
    
    over_limit_sr = (self.extrem_type.value * new_rel_sr - self.limit) > 0
    if len(over_limit_sr) > 0:
      new_rel_sr[over_limit_sr] = self.sided_limit
      new_value_sr[over_limit_sr] = (self.sided_limit + 1) * using_open_sr[over_limit_sr]
    return new_value_sr,new_rel_sr
  
  def get_extrem_with_lim(self)->Tuple[pd.Series,pd.Series]:
    if self.limit <= 0:
      raise AttributeError("Limit must be positive number")
    
    extremum_value_sr, extremum_relation_sr = self.__get_new_value_rel_sr(self.shifted_v_df[self.shifted_v_df.columns[0]])
    extremum_idx_sr = pd.Series(0, index=extremum_value_sr.index)
    
    for c in self.shifted_v_df.columns[1:]:
        new_value_sr, new_rel_sr = self.__get_new_value_rel_sr(self.shifted_v_df[c][self.__get_filter_new_extrem_better_than_current(extremum_value_sr, c) &
                                                                                    self.__get_filter_rel_sr_not_overstep_limit(extremum_relation_sr)])

        extremum_value_sr.loc[new_value_sr.index] = new_value_sr
        extremum_idx_sr.loc[new_value_sr.index] = c
        extremum_relation_sr.loc[new_value_sr.index] = new_rel_sr
        if self.__check_if_all_rel_sr_overstep_limit(extremum_relation_sr):
          break
        
    return extremum_relation_sr, extremum_value_sr, extremum_idx_sr

  def __get_filter_new_extrem_better_than_current(self, extremum_value_sr:pd.Series, shift_column:str)->pd.Series:
    """get pandas filter for extream values DataFrame(self.shifted_v_df), \n
       where value from self.shifted_v_df[shift_column] is better than current value in extremum_value_sr

    Args:
        extremum_value_sr (pd.Series): current extremum values
        shift_column (str): name of column of shifted values

    Returns:
        pd.Series: Pandas filter
    """
    return (self.extrem_type.value * ( self.shifted_v_df[shift_column] - extremum_value_sr) > 0)

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
