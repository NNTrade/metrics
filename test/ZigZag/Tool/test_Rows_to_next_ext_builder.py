import unittest
from src.ZigZag.Tool.Rows_to_next_ext_builder import Rows_to_next_ext_builder
import logging
import pandas as pd
from src.ZigZag.Constant import FLAG_COL_NAME
import numpy as np

class Rows_to_next_ext_builderTestCase(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(format = '%(asctime)s %(module)s %(levelname)s: %(message)s',
                    datefmt = '%m/%d/%Y %I:%M:%S %p', level = logging.DEBUG)

    def test_check(self):   
        df = pd.Series([1,0,0,-1,0,0,0,0,0,0,0,0,1])
        expected_df:pd.Series = pd.Series([3,2,1,9,8,7,6,5,4,3,2,1,np.NAN])

        asserted_df= Rows_to_next_ext_builder(df)
        
        self.assertTrue(expected_df.equals(asserted_df))