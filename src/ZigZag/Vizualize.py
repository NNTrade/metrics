import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from .Constant import *

def draw_chart(chart_sr:pd.Series, zz_df:pd.DataFrame):
    f, axs = plt.subplots(3,1,figsize=(30,20), dpi=80)
    plt.subplots_adjust(hspace=0)

    axs[0].set_xlim(0, len(chart_sr))
    axs[0].set_ylim(chart_sr.min()*0.99, chart_sr.max()*1.01)

    axs[0].plot(np.arange(len(chart_sr)), chart_sr, 'k:', alpha=0.5)
    axs[0].plot(np.arange(len(chart_sr)), zz_df[VALUE_COL_NAME], 'k-')
    axs[0].scatter(np.arange(len(chart_sr))[zz_df[FLAG_COL_NAME] == 1], zz_df[VALUE_COL_NAME][zz_df[FLAG_COL_NAME] == 1], color='g')
    axs[0].scatter(np.arange(len(chart_sr))[zz_df[FLAG_COL_NAME] == -1], zz_df[VALUE_COL_NAME][zz_df[FLAG_COL_NAME] == -1], color='r')

    return (f, axs)