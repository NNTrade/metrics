from ..Tool import Rows_to_next_ext_builder
from ..Constant import FLAG_COL_NAME, ANGLE_COL_NAME, ROWS_TO_NEXT_EXT_COL_NAME
import pandas as pd
from typing import List
import numpy as np

class Check_machine:
    def __init__(self,check_func_list:List):
        self.check_func_list = check_func_list
        pass

    def is_correct(self, zz_df:pd.DataFrame)->bool:
        for func in self.check_func_list:
            if not func(zz_df):
                return False
        return True


def no_same_move_direction_is_correct(zz_df:pd.DataFrame):
    picks_zz = zz_df[zz_df[FLAG_COL_NAME]!=0]
    angle_check:pd.Series = picks_zz[FLAG_COL_NAME] * picks_zz[ANGLE_COL_NAME]     
    return not angle_check[angle_check>0].any()   

class Check_len_size:       
    def __init__(self,min_len = 10, max_len = np.NaN) -> None:
        self.min_len = min_len
        self.max_len = max_len
        pass

    def is_correct(self,zz_df:pd.DataFrame)->bool:
        min_max_tuple = Check_len_size.get_min_max(zz_df[FLAG_COL_NAME])
        is_correct = True
        if not np.isnan(self.min_len):
            is_correct = is_correct and not min_max_tuple[0] < self.min_len
        if not np.isnan(self.max_len):
            is_correct = is_correct and not min_max_tuple[1] > self.max_len
        return is_correct

    @staticmethod
    def get_min_max(zz_sr:pd.Series)->int:
        data_idx_sr = zz_sr.reset_index(drop=True)
        idx_df = pd.DataFrame(data_idx_sr[data_idx_sr!=0].index,columns=["idx"])
        idx_df["next_idx"] = idx_df["idx"].shift(-1)
        idx_df["move"] = idx_df["next_idx"] - idx_df["idx"]
        return (idx_df["move"].min(), idx_df["move"].max())