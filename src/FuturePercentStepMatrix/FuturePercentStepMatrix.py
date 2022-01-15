from typing import List,Union
from traiding.indicator.RelativePercent.Factory import get_percent
import pandas as pd
import numpy as np
def col_name_default(percent:float, step: int, value_sr_name:str,is_upper:bool):
    return f"P({'up' if is_upper else 'down'}{percent})[Sh{step}-{value_sr_name}]"

def BuildMatrix(value_sr:pd.Series, step_arr:Union[List[int],pd.Series], percent_arr:List[float], use_abs:bool=False, is_upper:bool=True)->pd.DataFrame:
    """Get matrix of percent step values

    Args:
        value_sr (pd.Series): values series
        step_arr (Union[List[int],pd.Series]): step length
        percent_arr (List[float]): percents checked
        use_abs (bool, optional): use abs percent. Defaults to False.
        is_upper (bool, optional): check if percent upper than expected value. Defaults to True.

    Raises:
        ValueError: Argument errors

    Returns:
        pd.DataFrame: [description]
    """
    step_sr = pd.Series(step_arr)
    if (step_sr < 1).any():
        raise ValueError("step_arr has negative value")
    
    if step_sr.duplicated().any():
        raise ValueError("step_arr has duplicate value") 
    
    _ret_pd = pd.DataFrame(index=value_sr.index)
    
    for step in step_arr:
        step_val_sr = value_sr.shift(-step)
        perc_sr = get_percent(step_val_sr, value_sr,use_abs)
        for percent in percent_arr:
            col_name = col_name_default(percent,step,value_sr.name,is_upper)            
            if is_upper:
                _ret_pd[col_name] = perc_sr > percent
            else:
                _ret_pd[col_name] = perc_sr < percent
            _ret_pd[col_name][perc_sr.isna()] = np.NAN
    return _ret_pd
                
        