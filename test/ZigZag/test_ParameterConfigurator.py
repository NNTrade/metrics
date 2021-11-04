import unittest
import logging
import pandas as pd
from src.ZigZag.ParameterConfigurator import Search_by_range
import numpy as np

class ParameterConfiguratorTestCase(unittest.TestCase):
    logging.basicConfig(format = '%(asctime)s %(module)s %(levelname)s: %(message)s',
                    datefmt = '%m/%d/%Y %I:%M:%S %p', level = logging.DEBUG)

    def test_search_work__check(self):
        np.random.seed(1997)
        x_sr = pd.Series(np.cumprod(1 + np.random.randn(300) * 0.01))
        Search_by_range(x_sr, np.arange(-1, 1, 0.1),np.arange(-1, 0, 0.1),check_zz_df=False)
        