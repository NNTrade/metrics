from typing import List
import numpy as np
import pandas as pd
from typing import List,Tuple
from ..Builder import ZigZagBuilder
from .CompareFunctions import Prod_Max_func
from .IsCorrectFunctions import Check_machine, no_same_move_direction_is_correct, Check_len_size
import logging
from ...misc.counter import Counter
from ..Constant import FLAG_COL_NAME, ANGLE_COL_NAME

def __base_check__():
    len_checker = Check_len_size(10)
    return Check_machine([no_same_move_direction_is_correct, len_checker.is_correct]).is_correct

def Search_by_range(sr:pd.Series, up_thresh_list:List[float], down_thresh_list:List[float], compare_func = Prod_Max_func().is_best, check_func = __base_check__(), check_zz_df:bool = True)->Tuple[float,float]:
    best_parameter = np.NAN
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
            if compare_func(zz_df):
                best_parameter = (up_thresh, down_thresh)    
    return best_parameter
