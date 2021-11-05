from ..Constant import FLAG_COL_NAME, ANGLE_COL_NAME
import pandas as pd
from typing import List

class Check_machine:
    def __init__(self,check_func_list:List):
        self.check_func_list = check_func_list
        pass

    def check_is_correct(self, zz_df:pd.DataFrame)->bool:
        for func in self.check_func_list:
            if not func(zz_df):
                return False
        return True


def check_no_same_move_direction(zz_df:pd.DataFrame):
    picks_zz = zz_df[zz_df[FLAG_COL_NAME]!=0]
    angle_check:pd.Series = picks_zz[FLAG_COL_NAME] * picks_zz[ANGLE_COL_NAME]     
    return not angle_check[angle_check>0].any()   

class Check_len_size:
    
    def __init__(self,min_len = 10) -> None:
        self.min_len = min_len
        pass

    def check(self,zz_df:pd.DataFrame)->bool:
        data_idx_sr = zz_df.reset_index(drop=True)
        idx_df = pd.DataFrame(data_idx_sr[data_idx_sr[FLAG_COL_NAME]!=0].index,columns=["idx"])
        idx_df["next_idx"] = idx_df["idx"].shift(-1)
        idx_df["move"] = idx_df["next_idx"] - idx_df["idx"]
        return not idx_df[idx_df["move"] < self.min_len]["move"].any()
        