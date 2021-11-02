import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from .Constant import *

def draw_chart(chart_sr:pd.Series, zz_df:pd.DataFrame,figsize=(30,10)):
    plt.figure(figsize=figsize, dpi=80)

    plt.xlim(0, len(chart_sr))
    plt.ylim(chart_sr.min()*0.99, chart_sr.max()*1.01)

    plt.plot(np.arange(len(chart_sr)), chart_sr, 'k:', alpha=0.5)
    plt.plot(np.arange(len(chart_sr)), zz_df[VALUE_COL_NAME], 'k-')
    plt.scatter(np.arange(len(chart_sr))[zz_df[FLAG_COL_NAME] == 1], zz_df[VALUE_COL_NAME][zz_df[FLAG_COL_NAME] == 1], color='g')
    plt.scatter(np.arange(len(chart_sr))[zz_df[FLAG_COL_NAME] == -1], zz_df[VALUE_COL_NAME][zz_df[FLAG_COL_NAME] == -1], color='r')
