from typing import List,Union
#from traiding.indicator.RelativePercent.Factory import get_percent
import pandas as pd
import numpy as np
from enum import Enum

class Compare(Enum):
    """
    Returns:
        [type]: Check if percent higher than expect
    """
    Higher = 1,
    """
    Returns:
        [type]: Check if percent lower than expect
    """
    Lower = 2,
    """
    Returns:
        [type]: Check if percent farer from zero than expect
    """
    VolatilityHigher = 3,
    """
    Returns:
        [type]: Check if percent closer from zero than expect
    """
    VolatilityLower = 4
    
    def ShortName(self)->str:
        if self == Compare.Lower:
            return "LW"
        elif self == Compare.Higher:
            return "HG"
        elif self == Compare.VolatilityHigher:
            return "VH"
        elif self == Compare.VolatilityLower:
            return "VL"

def col_name_default(percent:float, step: int, value_sr_name:str,compare:Compare, **args):
    is_ext = args["is_ext"] if "is_ext" in args else False
    shift_name = "ESh" if is_ext else "Sh"
    return f"P({compare.ShortName()}{percent})[{shift_name}{step}-{value_sr_name}]"

def BuildMatrix(value_sr:pd.Series, step_arr:Union[List[int],pd.Series], percent_arr:List[float], use_abs:bool=False, compare=Compare.VolatilityHigher)->pd.DataFrame:
    """Get matrix of percent step values

    Args:
        value_sr (pd.Series): values series
        step_arr (Union[List[int],pd.Series]): step length
        percent_arr (List[float]): percents checked
        use_abs (bool, optional): use abs percent. Defaults to False.
        compare ([type], optional): set type of compare

    Raises:
        ValueError: Argument errors

    Returns:
        pd.DataFrame: [description]
    """
    step_np = np.array(step_arr)
    percent_np = np.array(percent_arr)
    _check_step(step_np)
    _check_compare(percent_np, compare)
    
    return _BuildMatrix(value_sr,value_sr,step_arr,percent_arr,use_abs,compare)
                
def _check_compare(percent_np:np.array,compare: Compare):
    if compare == Compare.VolatilityHigher or compare == Compare.VolatilityLower:
        if np.any(percent_np < 0):
            raise ValueError(f"percent_arr must be all positiove for {Compare.VolatilityHigher} compare") 

def _check_step(step_np:np.array):
    if np.any(step_np < 1):
        raise ValueError("step_arr has negative value")
    
    u, c = np.unique(step_np, return_counts=True)
    if  np.any(c > 1):
        raise ValueError("step_arr has duplicate value") 

def _BuildMatrix(base_value_sr:pd.Series,value_sr:pd.Series, step_arr:Union[List[int],pd.Series], percent_arr:List[float], use_abs:bool=False, compare=Compare.VolatilityHigher, **args)->pd.DataFrame:
    """Get matrix of percent step values

    Args:
        base_value_sr (pd.Series): values for base
        value_sr (pd.Series): values series
        step_arr (Union[List[int],pd.Series]): step length
        percent_arr (List[float]): percents checked
        use_abs (bool, optional): use abs percent. Defaults to False.
        compare ([type], optional): set type of compare

    Returns:
        pd.DataFrame: [description]
    """
    _ret_pd = pd.DataFrame(index=base_value_sr.index)
    
    for step in step_arr:
        step_val_sr = value_sr.shift(-step)
        perc_sr = None #get_percent(step_val_sr, base_value_sr,use_abs)
        for percent in percent_arr:
            col_name = col_name_default(percent,step,base_value_sr.name,compare,**args)
            if compare == Compare.VolatilityHigher or compare == Compare.VolatilityLower:
                perc_sr = perc_sr.abs()           
                percent = abs(percent)
            if compare == Compare.Higher or compare == Compare.VolatilityHigher:
                _ret_pd[col_name] = perc_sr > percent
            elif compare == Compare.Lower or compare == Compare.VolatilityLower:
                _ret_pd[col_name] = perc_sr < percent
            _ret_pd[col_name][perc_sr.isna()] = np.NAN
    return _ret_pd