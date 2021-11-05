from typing import List
from numpy import log
import pandas as pd
from typing import List,Tuple
from ..Builder import ZigZagBuilder
from ..ProfitCalculator import get_prod_of_profit
from .CorrectChecking import Check_machine, check_no_same_move_direction, Check_len_size
import logging
from ...misc.counter import Counter
from ..Constant import FLAG_COL_NAME, ANGLE_COL_NAME


def prod_max_func(zz_df: pd.DataFrame, max_val: None)->Tuple[bool,float]:
    prod = get_prod_of_profit(zz_df)
    if not max_val is not None:
        return (True, prod)
    if prod > max_val:
        return (True, prod)
    else:
        return (False,)
            
def __base_check__():
    len_checker = Check_len_size(10)
    return Check_machine([check_no_same_move_direction, len_checker.check]).check_is_correct

def Search_by_range(sr:pd.Series, up_thresh_list:List[float], down_thresh_list:List[float], compare_func = prod_max_func, check_func = __base_check__(), check_zz_df:bool = True)->Tuple[float,float]:
    max_val = None
    best_parameter = None
    logger = logging.getLogger("Search_by_range")
    counter = Counter(len(up_thresh_list)*len(down_thresh_list))

    for up_thresh in up_thresh_list:
        for down_thresh in down_thresh_list:
            logger.log(logging.DEBUG,f"Check up_thresh={up_thresh}, down_thresh={down_thresh}")
            counter.next()
            zzb = ZigZagBuilder(up_thresh, down_thresh)
            zz_df = zzb.build_all(sr)
            
            if check_zz_df and not check_func(zz_df):
                continue
            comp_res = compare_func(zz_df, max_val)
            if comp_res[0]:
                max_val = comp_res[1]
                best_parameter = (up_thresh, down_thresh)    
    return best_parameter
