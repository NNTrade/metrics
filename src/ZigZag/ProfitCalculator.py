from typing import Dict
from numpy import double
import pandas as pd
from .Constant import FLAG_COL_NAME, DELTA_NEAR_EXT, VALUE_COL_NAME
import typing

def __get_perc_moves__(zz_df:pd.DataFrame)->pd.Series:
    moves = zz_df[zz_df[FLAG_COL_NAME]!=0][[VALUE_COL_NAME,DELTA_NEAR_EXT]].abs()
    perc_moves = moves[DELTA_NEAR_EXT]/moves[VALUE_COL_NAME]
    return perc_moves

def get_prod_of_profit(zz_df: pd.DataFrame)->double:
    perc_moves = __get_perc_moves__(zz_df)
    return (perc_moves+1).product()

def get_sum_of_profit(zz_df: pd.DataFrame)->double:
    perc_moves = __get_perc_moves__(zz_df)
    return perc_moves.sum()

def get_profit(zz_df:pd.DataFrame)->typing.Dict[str,double]:
    perc_moves = __get_perc_moves__(zz_df)
    return {"sum":perc_moves.sum(), "prod":(perc_moves+1).product()}