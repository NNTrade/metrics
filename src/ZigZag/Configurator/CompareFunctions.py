import typing
import pandas as pd
import numpy as np
from ..ProfitCalculator import get_prod_of_profit
from typing import List, Tuple
from ..Constant import VALUE_COL_NAME

class Prod_Max_func:
    '''
    Сравнивает ZigZag на максимальную доходность
    '''
    def __init__(self) -> None:
        self.max_prod = np.NAN
        pass

    def is_best(self, zz_df:pd.DataFrame)->bool:
        prod = get_prod_of_profit(zz_df)
        if np.isnan(self.max_prod) or prod > self.max_prod:
            self.__set_is_best__(zz_df,prod)
            return True
        elif prod == self.max_prod:
            return np.NaN
        else:
            return False

    def __set_is_best__(self, zz_df:pd.DataFrame, prod = np.NAN):
        if np.isnan(prod):
            prod = get_prod_of_profit(zz_df)
        self.max_prod = prod

class Data_ZZ_Min_func:
    '''
    Сравнивает ZigZag на минимальное расхождение свечей и ZigZag
    '''
    def __init__(self,data:pd.Series) -> None:
        self.min_delta = np.NAN
        self.data = data
        pass

    def is_best(self, zz_df:pd.DataFrame)->bool:
        cur_delta = (self.data - zz_df[VALUE_COL_NAME]).abs().sum()
        if np.isnan(self.min_delta) or cur_delta < self.min_delta:
            self.__set_is_best__(zz_df,cur_delta)
            return True
        elif cur_delta == self.min_delta:
            return np.NaN
        else:
            return False
    
    def __set_is_best__(self, zz_df:pd.DataFrame, cur_delta = np.NAN):
        if np.isnan(cur_delta):
            cur_delta = (self.data - zz_df[VALUE_COL_NAME]).abs().sum()
        self.min_delta = cur_delta

class CompareSequenceFunc:
    '''
    Набор индикаторов сравнения
    '''
    def __init__(self, compare_cls) -> None:
        self.compare_cls_list = compare_cls
        pass

    def is_best(self, zz_df:pd.DataFrame):
        res = np.NAN
        for funcCls in self.compare_cls_list:
            if np.isnan(res):
                res = funcCls.is_best(zz_df)
            
            if np.isnan(res) != True:
                break
        
        if res:
            for funcCls in self.compare_cls_list:
                funcCls.__set_is_best__(zz_df)
        
        return res


            


