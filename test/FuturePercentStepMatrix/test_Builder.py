from asyncio.log import logger
from cmath import nan
from multiprocessing.context import assert_spawning
import numpy as np
from re import X
import unittest
from src.FuturePercentStepMatrix.Builder import BuildMatrix, Compare
import pandas as pd
import logging

class FuturePercentStepMatrixTestCase(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(format = '%(asctime)s %(module)s %(levelname)s: %(message)s',
                    datefmt = '%m/%d/%Y %I:%M:%S %p', level = logging.DEBUG)
    
    def test_negative_step_than_error(self):
        with self.assertRaises(ValueError):
            BuildMatrix(pd.Series(), [-1,1,2,3], [1,2,3])

    def test_negative_perc_on_Volatility_than_error(self):
        with self.assertRaises(ValueError):
            BuildMatrix(pd.Series(), [1,2,3], [1,-2,3], compare=Compare.VolatilityHigher)
            
    def test_zero_step_than_error(self):
        with self.assertRaises(ValueError):
            BuildMatrix(pd.Series(), [2,1,0,3], [1,2,3])
            
    def test_duplicate_step_than_error(self):
        with self.assertRaises(ValueError):
            BuildMatrix(pd.Series(), pd.Series([2,1,1,3]), [1,2,3])
            
    def test_upper_matrix(self):
        value_sr = pd.Series([1,2,4,8],name="cls", index=["A1","B2","C3","D4"])
        assert_matrix = BuildMatrix(value_sr,[1,2],[49,99, 300],compare=Compare.Higher)
        expect_matrix = pd.DataFrame({
            "P(HG49)[Sh1-cls]":[True,True,True,np.NAN],
            "P(HG99)[Sh1-cls]":[True,True,True,np.NAN],
            "P(HG300)[Sh1-cls]":[False,False,False,np.NAN],
            "P(HG49)[Sh2-cls]":[True,True,np.NAN,np.NAN],
            "P(HG99)[Sh2-cls]":[True,True,np.NAN,np.NAN],
            "P(HG300)[Sh2-cls]":[False,False,np.NAN,np.NAN]            
        },index=["A1","B2","C3","D4"])
        
        self.assertEqual(len(assert_matrix.columns), len(expect_matrix.columns))
        self.assertEqual(len(assert_matrix), len(expect_matrix))
        for col in assert_matrix:
            self.logger.info(f"Col:{col}")
            self.logger.info(assert_matrix[col])
            for idx in assert_matrix.index:
                if np.isnan(assert_matrix[col][idx]):
                    self.assertTrue(np.isnan(expect_matrix[col][idx]))
                else:
                    self.assertEqual(assert_matrix[col][idx], expect_matrix[col][idx])
                    
    def test_negative_percent_upper_matrix(self):
        value_sr = pd.Series([8,4,2,1],name="cls", index=["A1","B2","C3","D4"])
        assert_matrix = BuildMatrix(value_sr,[1,2],[-51,-76, -300],compare=Compare.Higher)
        expect_matrix = pd.DataFrame({
            "P(HG-51)[Sh1-cls]":[True,True,True,np.NAN],
            "P(HG-76)[Sh1-cls]":[True,True,True,np.NAN],
            "P(HG-300)[Sh1-cls]":[True,True,True,np.NAN],
            "P(HG-51)[Sh2-cls]":[False,False,np.NAN,np.NAN],
            "P(HG-76)[Sh2-cls]":[True,True,np.NAN,np.NAN],
            "P(HG-300)[Sh2-cls]":[True,True,np.NAN,np.NAN]            
        },index=["A1","B2","C3","D4"])
        
        self.assertEqual(len(assert_matrix.columns), len(expect_matrix.columns))
        self.assertEqual(len(assert_matrix), len(expect_matrix))
        for col in assert_matrix:
            self.logger.info(f"Col:{col}")
            self.logger.info(assert_matrix[col])
            for idx in assert_matrix.index:
                if np.isnan(assert_matrix[col][idx]):
                    self.assertTrue(np.isnan(expect_matrix[col][idx]), f"{col} idx {idx}")
                else:
                    self.assertEqual(assert_matrix[col][idx], expect_matrix[col][idx], f"{col} idx {idx}")
                             
    def test_is_lowwer_matrix(self):
        value_sr = pd.Series([1,2,4,8],name="cls", index=["A1","B2","C3","D4"])
        assert_matrix = BuildMatrix(value_sr,[1,2],[49,101, 301],compare=Compare.Lower)
        expect_matrix = pd.DataFrame({
            "P(LW49)[Sh1-cls]":[False,False,False,np.NAN],
            "P(LW101)[Sh1-cls]":[True,True,True,np.NAN],
            "P(LW301)[Sh1-cls]":[True,True,True,np.NAN],
            "P(LW49)[Sh2-cls]":[False,False,np.NAN,np.NAN],
            "P(LW101)[Sh2-cls]":[False,False,np.NAN,np.NAN],
            "P(LW301)[Sh2-cls]":[True,True,np.NAN,np.NAN]            
        },index=["A1","B2","C3","D4"])
        
        self.assertEqual(len(assert_matrix.columns), len(expect_matrix.columns))
        self.assertEqual(len(assert_matrix), len(expect_matrix))
        for col in assert_matrix:
            self.logger.info(f"Col:{col}")
            self.logger.info(assert_matrix[col])
            for idx in assert_matrix.index:
                if np.isnan(assert_matrix[col][idx]):
                    self.assertTrue(np.isnan(expect_matrix[col][idx]), f"{col} idx {idx}: {assert_matrix[col][idx]} != {expect_matrix[col][idx]}")
                else:
                    self.assertEqual(assert_matrix[col][idx], expect_matrix[col][idx], f"{col} idx {idx}: {assert_matrix[col][idx]} != {expect_matrix[col][idx]}")
                    
    def test_negative_is_lower_percent_matrix(self):
        value_sr = pd.Series([8,4,2,1],name="cls", index=["A1","B2","C3","D4"])
        assert_matrix = BuildMatrix(value_sr,[1,2],[-49,-76, -300],compare=Compare.Lower)
        expect_matrix = pd.DataFrame({
            "P(LW-49)[Sh1-cls]":[True,True,True,np.NAN],
            "P(LW-76)[Sh1-cls]":[False,False,False,np.NAN],
            "P(LW-300)[Sh1-cls]":[False,False,False,np.NAN],
            "P(LW-49)[Sh2-cls]":[True,True,np.NAN,np.NAN],
            "P(LW-76)[Sh2-cls]":[False,False,np.NAN,np.NAN],
            "P(LW-300)[Sh2-cls]":[False,False,np.NAN,np.NAN]            
        },index=["A1","B2","C3","D4"])
        
        self.assertEqual(len(assert_matrix.columns), len(expect_matrix.columns))
        self.assertEqual(len(assert_matrix), len(expect_matrix))
        for col in assert_matrix:
            self.logger.info(f"Col:{col}")
            self.logger.info(assert_matrix[col])
            for idx in assert_matrix.index:
                if np.isnan(assert_matrix[col][idx]):
                    self.assertTrue(np.isnan(expect_matrix[col][idx]), f"{col} idx {idx}")
                else:
                    self.assertEqual(assert_matrix[col][idx], expect_matrix[col][idx], f"{col} idx {idx}")
        
    
    def test_volupper_matrix(self):
        value_sr = pd.Series([1,2,4,8],name="cls", index=["A1","B2","C3","D4"])
        assert_matrix = BuildMatrix(value_sr,[1,2],[49,101, 300],compare=Compare.VolatilityHigher)
        expect_matrix = pd.DataFrame({
            "P(VH49)[Sh1-cls]":[True,True,True,np.NAN],
            "P(VH101)[Sh1-cls]":[False,False,False,np.NAN],
            "P(VH300)[Sh1-cls]":[False,False,False,np.NAN],
            "P(VH49)[Sh2-cls]":[True,True,np.NAN,np.NAN],
            "P(VH101)[Sh2-cls]":[True,True,np.NAN,np.NAN],
            "P(VH300)[Sh2-cls]":[False,False,np.NAN,np.NAN]            
        },index=["A1","B2","C3","D4"])
        
        self.assertEqual(len(assert_matrix.columns), len(expect_matrix.columns))
        self.assertEqual(len(assert_matrix), len(expect_matrix))
        for col in assert_matrix:
            self.logger.info(f"Col:{col}")
            self.logger.info(assert_matrix[col])
            for idx in assert_matrix.index:
                if np.isnan(assert_matrix[col][idx]):
                    self.assertTrue(np.isnan(expect_matrix[col][idx]))
                else:
                    self.assertEqual(assert_matrix[col][idx], expect_matrix[col][idx], f"{col} idx {idx}")
    
    def test_negative_percent_volupper_matrix(self):
        value_sr = pd.Series([8,4,2,1],name="cls", index=["A1","B2","C3","D4"])
        assert_matrix = BuildMatrix(value_sr,[1,2],[49,74, 300],compare=Compare.VolatilityHigher)
        expect_matrix = pd.DataFrame({
            "P(VH49)[Sh1-cls]":[True,True,True,np.NAN],
            "P(VH74)[Sh1-cls]":[False,False,False,np.NAN],
            "P(VH300)[Sh1-cls]":[False,False,False,np.NAN],
            "P(VH49)[Sh2-cls]":[True,True,np.NAN,np.NAN],
            "P(VH74)[Sh2-cls]":[True,True,np.NAN,np.NAN],
            "P(VH300)[Sh2-cls]":[False,False,np.NAN,np.NAN]            
        },index=["A1","B2","C3","D4"])
        
        self.assertEqual(len(assert_matrix.columns), len(expect_matrix.columns))
        self.assertEqual(len(assert_matrix), len(expect_matrix))
        for col in assert_matrix:
            self.logger.info(f"Col:{col}")
            self.logger.info(assert_matrix[col])
            for idx in assert_matrix.index:
                if np.isnan(assert_matrix[col][idx]):
                    self.assertTrue(np.isnan(expect_matrix[col][idx]), f"{col} idx {idx}")
                else:
                    self.assertEqual(assert_matrix[col][idx], expect_matrix[col][idx], f"{col} idx {idx}")
                    
    def test_is_lowwer_matrix(self):
        value_sr = pd.Series([1,2,4,8],name="cls", index=["A1","B2","C3","D4"])
        assert_matrix = BuildMatrix(value_sr,[1,2],[51,101, 301],compare=Compare.VolatilityLower)
        expect_matrix = pd.DataFrame({
            "P(VL51)[Sh1-cls]":[False,False,False,np.NAN],
            "P(VL101)[Sh1-cls]":[True,True,True,np.NAN],
            "P(VL301)[Sh1-cls]":[True,True,True,np.NAN],
            "P(VL51)[Sh2-cls]":[False,False,np.NAN,np.NAN],
            "P(VL101)[Sh2-cls]":[False,False,np.NAN,np.NAN],
            "P(VL301)[Sh2-cls]":[True,True,np.NAN,np.NAN]            
        },index=["A1","B2","C3","D4"])
        
        self.assertEqual(len(assert_matrix.columns), len(expect_matrix.columns))
        self.assertEqual(len(assert_matrix), len(expect_matrix))
        for col in assert_matrix:
            self.logger.info(f"Col:{col}")
            self.logger.info(assert_matrix[col])
            for idx in assert_matrix.index:
                if np.isnan(assert_matrix[col][idx]):
                    self.assertTrue(np.isnan(expect_matrix[col][idx]), f"{col} idx {idx}: {assert_matrix[col][idx]} != {expect_matrix[col][idx]}")
                else:
                    self.assertEqual(assert_matrix[col][idx], expect_matrix[col][idx], f"{col} idx {idx}: {assert_matrix[col][idx]} != {expect_matrix[col][idx]}")
                    
    def test_negative_is_lower_percent_matrix(self):
        value_sr = pd.Series([8,4,2,1],name="cls", index=["A1","B2","C3","D4"])
        assert_matrix = BuildMatrix(value_sr,[1,2],[49,74, 300],compare=Compare.VolatilityLower)
        expect_matrix = pd.DataFrame({
            "P(VL49)[Sh1-cls]":[False,False,False,np.NAN],
            "P(VL74)[Sh1-cls]":[True,True,True,np.NAN],
            "P(VL300)[Sh1-cls]":[True,True,True,np.NAN],
            "P(VL49)[Sh2-cls]":[False,False,np.NAN,np.NAN],
            "P(VL74)[Sh2-cls]":[False,False,np.NAN,np.NAN],
            "P(VL300)[Sh2-cls]":[True,True,np.NAN,np.NAN]            
        },index=["A1","B2","C3","D4"])
        
        self.assertEqual(len(assert_matrix.columns), len(expect_matrix.columns))
        self.assertEqual(len(assert_matrix), len(expect_matrix))
        for col in assert_matrix:
            self.logger.info(f"Col:{col}")
            self.logger.info(assert_matrix[col])
            for idx in assert_matrix.index:
                if np.isnan(assert_matrix[col][idx]):
                    self.assertTrue(np.isnan(expect_matrix[col][idx]), f"{col} idx {idx}")
                else:
                    self.assertEqual(assert_matrix[col][idx], expect_matrix[col][idx], f"{col} idx {idx}")