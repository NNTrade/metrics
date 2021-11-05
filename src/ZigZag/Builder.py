import pandas as pd
from zigzag import *
import numpy as np
from .Constant import FLAG_COL_NAME, NEXT_INDEX_COL_NAME, ROWS_TO_NEXT_EXT_COL_NAME, VALUE_COL_NAME,ANGLE_COL_NAME,NEAREST_EXT_COL_NAME,DELTA_NEAR_EXT_COL_NAME

class ZigZagBuilder:
    def __init__(self,up_thresh:float=0.02, down_thresh:float=-0.02) -> None:
        self.up_thresh:float = up_thresh
        self.down_thresh:float = down_thresh
        pass

    def build_flags(self, data_sr:pd.Series)->pd.Series:
        data_idx_sr = data_sr.reset_index(drop=True)
        return self.__prepare_return_index(self.__build_flags__(data_idx_sr),data_sr)

    def __build_flags__(self, dropped_data_sr:pd.Series)->pd.Series:
        pivot = peak_valley_pivots(dropped_data_sr, self.up_thresh, self.down_thresh)
        return pd.Series(pivot,index=dropped_data_sr.index,name=FLAG_COL_NAME)
    
    def build_values(self, data_sr:pd.Series)->pd.Series:
        dropped_data_sr = data_sr.reset_index(drop=True)   
        flag_sr = self.__build_flags__(dropped_data_sr)     
        return self.__prepare_return_index(self.__build_values__(dropped_data_sr,flag_sr),data_sr)

    def __build_values__(self, dropped_data_sr:pd.Series,flag_sr:pd.Series=None)->pd.Series:
        filtered_data = dropped_data_sr[flag_sr != 0]
        return pd.Series(np.interp(dropped_data_sr.index, filtered_data.index, filtered_data), index=dropped_data_sr.index, name=VALUE_COL_NAME)

    def build_nearest_ext(self, data_sr:pd.Series)->pd.Series:  
        flag_sr = self.build_flags(data_sr)  
        return self.__prepare_return_index(self.__build_nearest_ext__(data_sr,flag_sr),data_sr)

    def __build_nearest_ext__(self, data_sr:pd.Series, flag_sr:pd.Series)->pd.Series:
        work_df = pd.concat([data_sr.rename("val"), flag_sr], axis=1).sort_index(ascending=False)
        class nearest_ext_worker:
            def __init__(self) -> None:
                self.lastFlag = np.NaN
                self.ext = np.NaN
                pass
            def do(self,value, flag):
                ret_val = self.ext
                if flag * self.lastFlag < 0 or np.isnan(self.ext):
                    self.ext = value
                    self.lastFlag = flag
                return ret_val
        near_ext_wrk = nearest_ext_worker()
        return work_df.apply(lambda row: near_ext_wrk.do(row["val"], row[FLAG_COL_NAME]),axis=1).sort_index(ascending=True).rename(NEAREST_EXT_COL_NAME)

    def build_delta_to_near_ext(self,data_sr:pd.Series)->pd.Series:
        near_ext_sr = self.build_nearest_ext(data_sr=data_sr)
        return self.__build_delta_to_near_ext__(data_sr, near_ext_sr)

    def __build_delta_to_near_ext__(self,data_sr:pd.Series,near_ext_sr:pd.Series)->pd.Series:
        return (near_ext_sr - data_sr).rename(DELTA_NEAR_EXT_COL_NAME)

    def build_angle(self,data_sr:pd.Series)->pd.Series:
        val_sr = self.build_values(data_sr)
        return self.__build_angle__(val_sr)

    def __build_angle__(self, val_sr:pd.Series)->pd.Series:
        class worker:
            def __init__(self) -> None:
                self.prev_value = np.NaN
                pass
            def next(self, cur_val):
                if np.isnan(self.prev_value):
                    self.prev_value = cur_val
                    return np.NaN
                else:
                    ret_val = cur_val - self.prev_value
                    self.prev_value = cur_val
                    return ret_val
        wrk = worker()
        return val_sr.apply(wrk.next).shift(periods=-1).rename(ANGLE_COL_NAME)

    def build_next_index(self, data_sr:pd.Series)->pd.Series:
        flag_sr = self.build_flags(data_sr)
        return self.__build_next_index__(data_sr, flag_sr)

    def __build_next_index__(self, data_sr:pd.Series, flag_sr:pd.Series)->pd.Series:
        class worker:
            def __init__(self) -> None:
                self.prev_idx = np.NaN
                pass
            def next(self, cur_val, cur_index):
                if not np.isnan(cur_val) and cur_val != 0:
                    last_time_idx = self.prev_idx
                    self.prev_idx = cur_index
                    return last_time_idx
                else:
                    return self.prev_idx

        wrk = worker()
        _ret_arr = []
        for idx in reversed(flag_sr.index):
            _ret_arr.append(wrk.next(flag_sr[idx], idx))
        return pd.Series(reversed(_ret_arr), index=data_sr.index,name=NEXT_INDEX_COL_NAME)

    def rows_to_next_ext(self, data_sr:pd.Series)->pd.Series:
        flag_sr = self.build_flags(data_sr)
        return self.__rows_to_next_ext__(data_sr, flag_sr)

    def __rows_to_next_ext__(self, data_sr:pd.Series, flag_sr:pd.Series = None)->pd.Series:
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
        return pd.Series(reversed(_ret_arr), index=data_sr.index,name=ROWS_TO_NEXT_EXT_COL_NAME)

    def build_all(self, data_sr:pd.Series)->pd.DataFrame:
        data_idx_sr = data_sr.reset_index(drop=True)
        flag_sr = self.__build_flags__(data_idx_sr)
        value_sr = self.__build_values__(data_idx_sr, flag_sr)
        _ret = self.__prepare_return_index(pd.concat([flag_sr,value_sr], axis=1),data_sr)
        _ret[ANGLE_COL_NAME] = self.__build_angle__(_ret[VALUE_COL_NAME])
        _ret[NEAREST_EXT_COL_NAME] = self.__build_nearest_ext__(data_sr, _ret[FLAG_COL_NAME])
        _ret[DELTA_NEAR_EXT_COL_NAME] = self.__build_delta_to_near_ext__(data_sr,_ret[NEAREST_EXT_COL_NAME])
        _ret[NEXT_INDEX_COL_NAME] = self.__build_next_index__(data_sr, _ret[FLAG_COL_NAME])
        _ret[ROWS_TO_NEXT_EXT_COL_NAME] = self.__rows_to_next_ext__(data_sr, _ret[FLAG_COL_NAME])
        return _ret

    def __prepare_return_index(self, ret_df:pd.DataFrame, data_sr:pd.Series):
        ret_df.index = data_sr.index
        return ret_df
