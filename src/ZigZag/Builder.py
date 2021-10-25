from os import name
from re import S
from unittest import runner
from numpy.random.mtrand import f
import pandas as pd
from zigzag import *
import numpy as np

FLAG_COL_NAME = "Flag"
VALUE_COL_NAME = "Value"
ANGLE_COL_NAME = "Angle"
NEAREST_EXT = "Nearest_Ext"
DELTA_NEAR_EXT = "Delta_Near_Ext"

class ZigZagBuilder:
    def __init__(self,up_thresh:float=0.02, down_thresh:float=-0.02) -> None:
        self.up_thresh:float = up_thresh
        self.down_thresh:float = down_thresh
        self.flag_col_name = FLAG_COL_NAME
        self.value_col_name = VALUE_COL_NAME
        self.angle_col_name = ANGLE_COL_NAME
        self.nearest_col_name = NEAREST_EXT
        self.delta_near_ext_name = DELTA_NEAR_EXT
        pass

    def build_flags(self, data_sr:pd.Series)->pd.Series:
        pivot = peak_valley_pivots(data_sr, self.up_thresh, self.down_thresh)
        return pd.Series(pivot,index=data_sr.index,name=self.flag_col_name)
    
    def __build_values__(self, data_sr:pd.Series,flag_sr:pd.Series)->pd.Series:
        filtered_data = data_sr[flag_sr != 0]
        return pd.Series(np.interp(data_sr.index, filtered_data.index, filtered_data), index=data_sr.index, name=self.value_col_name)

    def build_values(self, data_sr:pd.Series)->pd.Series:
        flag_sr = self.build_flags(data_sr)
        return self.__build_values__(data_sr, flag_sr)

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
        return work_df.apply(lambda row: near_ext_wrk.do(row["val"], row[self.flag_col_name]),axis=1).sort_index(ascending=True).rename(self.nearest_col_name)

    def build_nearest_ext(self, data_sr:pd.Series)->pd.Series:
        flag_sr = self.build_flags(data_sr)
        return self.__build_nearest_ext__(data_sr,flag_sr)

    def __build_delta_to_near_ext__(self,data_sr:pd.Series,near_ext_sr:pd.Series)->pd.Series:
        return (near_ext_sr - data_sr).rename(self.delta_near_ext_name)

    def build_delta_to_near_ext(self,data_sr:pd.Series)->pd.Series:
        near_ext_sr = self.build_nearest_ext(data_sr=data_sr)
        return self.__build_delta_to_near_ext__(data_sr, near_ext_sr)

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
        return val_sr.apply(wrk.next).shift(periods=-1).rename(self.angle_col_name)

    def build_angle(self,data_sr:pd.Series)->pd.Series:
        val_sr = self.build_values(data_sr)
        return self.__build_angle__(val_sr)


    def build_all(self, data_sr:pd.Series)->pd.DataFrame:
        flag_sr = self.build_flags(data_sr)
        value_sr = self.__build_values__(data_sr, flag_sr)
        angle_sr = self.__build_angle__(value_sr)
        nearest_ext_sr = self.__build_nearest_ext__(data_sr, flag_sr)
        delta_near_ext_sr = self.__build_delta_to_near_ext__(data_sr,nearest_ext_sr)
        return pd.concat([flag_sr,value_sr,angle_sr, nearest_ext_sr,delta_near_ext_sr], axis=1)



