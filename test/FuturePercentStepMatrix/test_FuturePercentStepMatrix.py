from asyncio.log import logger
from cmath import nan
from multiprocessing.context import assert_spawning
import numpy as np
from re import X
import unittest
from src.FuturePercentStepMatrix.FuturePercentStepMatrix import BuildMatrix
import pandas as pd
import logging

class FuturePercentStepMatrixTestCase(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(format = '%(asctime)s %(module)s %(levelname)s: %(message)s',
                    datefmt = '%m/%d/%Y %I:%M:%S %p', level = logging.DEBUG)
    
    def test_negative_step_than_error(self):
        with self.assertRaises(ValueError):
            BuildMatrix(pd.Series(), [-1,1,2,3], [1,2,3])

    
    def test_zero_step_than_error(self):
        with self.assertRaises(ValueError):
            BuildMatrix(pd.Series(), [2,1,0,3], [1,2,3])
            
    def test_duplicate_step_than_error(self):
        with self.assertRaises(ValueError):
            BuildMatrix(pd.Series(), pd.Series([2,1,1,3]), [1,2,3])
            
    def test_matrix(self):
        value_sr = pd.Series([1,2,4,8],name="cls", index=["A1","B2","C3","D4"])
        assert_matrix = BuildMatrix(value_sr,[1,2],[49,99, 300])
        expect_matrix = pd.DataFrame({
            "P(up49)[Sh1-cls]":[True,True,True,np.NAN],
            "P(up99)[Sh1-cls]":[True,True,True,np.NAN],
            "P(up300)[Sh1-cls]":[False,False,False,np.NAN],
            "P(up49)[Sh2-cls]":[True,True,np.NAN,np.NAN],
            "P(up99)[Sh2-cls]":[True,True,np.NAN,np.NAN],
            "P(up300)[Sh2-cls]":[False,False,np.NAN,np.NAN]            
        },index=["A1","B2","C3","D4"])
        
        self.assertEqual(len(assert_matrix.columns), len(expect_matrix.columns))
        self.assertEqual(len(assert_matrix), len(expect_matrix))
        for col in assert_matrix:
            logger.info(f"Col:{col}")
            logger.info(assert_matrix[col])
            for idx in assert_matrix.index:
                if np.isnan(assert_matrix[col][idx]):
                    self.assertTrue(np.isnan(expect_matrix[col][idx]))
                else:
                    self.assertEqual(assert_matrix[col][idx], expect_matrix[col][idx])
                
        
        