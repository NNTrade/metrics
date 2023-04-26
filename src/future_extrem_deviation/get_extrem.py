import pandas as pd
from .extrem_type import ExtreamType
from NNTrade.common.candle_col_name import OPEN, HIGH, LOW
from typing import List


def __value_col(extrem_type:ExtreamType)->str:
  return f"Extrem_of_{extrem_type.name}"

def __idx_col(extrem_type:ExtreamType)->str:
  return f"Idx_of_{extrem_type.name}"    

def __shift_col(extrem_type:ExtreamType)->str:
  return f"Shift_to_{extrem_type.name}"

def __rel_col(extrem_type:ExtreamType)->str:
  return f"Rel_of_{extrem_type.name}"

def get_extrem_of(quote_df:pd.DataFrame, period:int, extrem_type:ExtreamType)->pd.DataFrame:
  """Get extem in period

  Args:
      quote_df (pd.DataFrame): _description_
      period (int): period of getting extem. 1 - only current candle, N - current candle and N-1 future candle
      extrem_type (ExtreamType): _description_

  Raises:
      AttributeError: _description_

  Returns:
      pd.Series: _description_
  """
  if extrem_type == ExtreamType.High:
    col = HIGH
  elif extrem_type == ExtreamType.Low:
    col = LOW
  else:
    raise AttributeError("Wrong extrem type must be ExtreamType.High or ExtreamType.Low", "extrem_type", extrem_type)
  
  result_v_name = __value_col(extrem_type)    
  result_id_name = __idx_col(extrem_type)    
  result_shift_name = __shift_col(extrem_type)    
  
  if period <= 0:
    raise AttributeError("Period must be > 0", "period", period)
  
  shifted_v_df = pd.DataFrame([quote_df[col].shift(-shift).rename(shift) for shift in range(period)]).T
  shifted_idx_df = pd.DataFrame([quote_df.index.to_series().shift(-shift).rename(shift) for shift in range(period)]).T
  if extrem_type == ExtreamType.High:
    extrem_sr = shifted_v_df.max(axis=1)
    shift_to_extrem = shifted_v_df.idxmax(axis=1).astype(int)
  else:
    extrem_sr = shifted_v_df.min(axis=1)
    shift_to_extrem = shifted_v_df.idxmin(axis=1).astype(int)
    
  extrem_id_sr = shifted_idx_df.apply(lambda row: row[shift_to_extrem.loc[row.name]], axis=1)
  return pd.DataFrame({result_v_name: extrem_sr,result_id_name:extrem_id_sr, result_shift_name:shift_to_extrem}, index=quote_df.index)
  #return (shifted_v_df.max(axis=1) if extrem_type == ExtreamType.High else shifted_v_df.min(axis=1)).rename(result_v_name)

def get_extrem_rel_of(quote_df:pd.DataFrame, period:int, extrem_type:ExtreamType)->pd.DataFrame:
  """Get extrem rel between all extemum in period and candle open

  Args:
      quote_df (pd.DataFrame): _description_
      period (int): period of getting extem. 1 - only current candle, N - current candle and N-1 future candle
      extrem_type (ExtreamType): _description_

  Returns:
      pd.Series: _description_
  """
  extrem_df = get_extrem_of(quote_df, period, extrem_type)
  rel_sr = ((extrem_df[__value_col(extrem_type)] - quote_df[OPEN]) / quote_df[OPEN]).rename(__rel_col(extrem_type))
  v_col = __value_col(extrem_type)
  return pd.concat([rel_sr, *[extrem_df[c] for c in extrem_df.columns if c != v_col]],axis=1)
  

def get_extrem_rel_matrix_of(quote_df:pd.DataFrame, periods:List[int], extrem_types:List[ExtreamType] = [ExtreamType.High, ExtreamType.Low])->pd.DataFrame:
  dfs = []
  for p in periods:
    for ext_t in extrem_types:
      ext_rel = get_extrem_rel_of(quote_df, p, ext_t)
      ext_rel.columns = [(p, c) for c in ext_rel.columns]
      dfs.append(ext_rel)
  matrix_df = pd.concat(dfs,axis=1)
  matrix_df.columns = pd.MultiIndex.from_tuples(matrix_df.columns)
  return matrix_df