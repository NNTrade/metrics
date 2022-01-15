import pandas as pd
from typing import List, Union
from .Builder import Compare, _check_step, _check_compare, _BuildMatrix, BuildMatrix
import numpy as np


class Factory:
    def __init__(self, use_abs: bool = False) -> None:
        self.use_abs = use_abs
        pass

    def GetInClose(self, value_sr: pd.Series, step_arr: Union[List[int], pd.Series], percent_arr: List[float], compare: Compare = Compare.VolatilityHigher):
        return BuildMatrix(value_sr, step_arr, percent_arr, self.use_abs, compare)

    @staticmethod
    def _agr_values(varue_sr: pd.Series, step: int, use_first: bool) -> pd.Series:
        _ret_df: pd.DataFrame = pd.DataFrame(varue_sr)
        first = 0 if use_first else 1

        for st in range(first, step):
            _ret_df[f"Sh{st}"] = varue_sr.shift(st)
        return _ret_df

    @staticmethod
    def _get_ext(df: pd.DataFrame, compare: Compare) -> pd.Series:
        if compare == Compare.Higher or compare == Compare.VolatilityHigher:
            return df.max(axis=1)
        else:
            return df.min(axis=1)

    def GetInExterem(self, base_value_sr: pd.Series, value_df: pd.DataFrame, step_arr: Union[List[int], pd.Series], percent_arr: List[float], use_first: bool, compare: Compare = Compare.VolatilityHigher) -> pd.DataFrame:

        if compare == Compare.VolatilityLower:
            raise ValueError(
                f"No sense try find Volatility lower it is always eq 0")

        value_sr = Factory._get_ext(value_df.join(base_value_sr, rsuffix='_other'), compare)

        step_np = np.array(step_arr)
        percent_np = np.array(percent_arr)
        _check_step(step_np)
        _check_compare(percent_np, compare)
        
        args = {"is_ext": True}
        _ret_df: pd.DataFrame = pd.DataFrame(index=base_value_sr.index)
        for step in step_arr:
            agr_value_sr = Factory._get_ext(
                Factory._agr_values(value_sr, step, use_first), compare)
            _ret_df = _ret_df.join(_BuildMatrix(base_value_sr, agr_value_sr, [
                                   step], percent_arr, self.use_abs, compare,**args))

        return _ret_df
