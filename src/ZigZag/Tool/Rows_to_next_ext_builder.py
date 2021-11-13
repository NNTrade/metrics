import pandas as pd
from ..Constant import ROWS_TO_NEXT_EXT_COL_NAME
import numpy as np

def Rows_to_next_ext_builder(flag_sr:pd.Series)->pd.Series:
    class worker:
        def __init__(self) -> None:
            self.cur_counter = np.NAN
            pass
        def next(self, cur_val):
            if np.isnan(cur_val):
                return np.NAN
            else:
                if cur_val != 0:
                    _ret = self.cur_counter + 1
                    self.cur_counter = 0
                    return _ret
                else:
                    self.cur_counter = self.cur_counter + 1 
                    return self.cur_counter

    wrk = worker()
    _ret_arr = []
    for idx in reversed(flag_sr.index):
        _ret_arr.append(wrk.next(flag_sr[idx]))
    return pd.Series(reversed(_ret_arr), index=flag_sr.index,name=ROWS_TO_NEXT_EXT_COL_NAME)