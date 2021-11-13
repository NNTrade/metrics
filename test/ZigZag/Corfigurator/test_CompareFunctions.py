import unittest
import logging
import pandas as pd
import numpy as np
from src.ZigZag.Configurator.CompareFunctions import Data_ZZ_Min_func
from src.ZigZag.Constant import VALUE_COL_NAME

class Data_ZZ_Min_funcTestCase(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(format = '%(asctime)s %(module)s %(levelname)s: %(message)s',
                    datefmt = '%m/%d/%Y %I:%M:%S %p', level = logging.DEBUG)

    def test_function_calculation(self):
        data = pd.Series([1,2,3,4])
        minF = Data_ZZ_Min_func(data)

        self.assertTrue(minF.is_best(pd.DataFrame({VALUE_COL_NAME: [2,3,4,5]})))
        self.assertEqual(4, minF.min_delta)

        self.assertFalse(minF.is_best(pd.DataFrame({VALUE_COL_NAME: [2,3,4,6]})))
        self.assertEqual(4, minF.min_delta)

        self.assertTrue(minF.is_best(pd.DataFrame({VALUE_COL_NAME: [2,3,4,4]})))
        self.assertEqual(3, minF.min_delta)

        self.assertTrue(np.isnan(minF.is_best(pd.DataFrame({VALUE_COL_NAME: [1,3,4,5]}))))
        self.assertEqual(3, minF.min_delta)