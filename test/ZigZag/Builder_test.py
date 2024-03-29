from re import X
import unittest
from src.ZigZag.Builder import ZigZagBuilder
import src.ZigZag.Constant as zzb
import pandas as pd
import numpy as np
import logging
from datetime import date
from datetime import timedelta 

class ZigZagBuilderTestCase(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(format = '%(asctime)s %(module)s %(levelname)s: %(message)s',
                    datefmt = '%m/%d/%Y %I:%M:%S %p', level = logging.DEBUG)

    def test_flags(self):
        np.random.seed(1997)
        x_sr = pd.Series(np.cumprod(1 + np.random.randn(10) * 0.01))
        zz_f = ZigZagBuilder(0.01, -0.0001)

        asserted_sr = zz_f.build_flags(x_sr)
        expected_sr = pd.Series([-1, 1,-1, 0, 0, 0, 0, 1, 0, 1,])
        
        self.logger.debug(x_sr)
        self.logger.debug(asserted_sr)

        self.assertEqual(len(asserted_sr), len(expected_sr))
        for i in range(len(expected_sr)):
            self.assertEqual(expected_sr[i], asserted_sr[i])

    def test_flags_def_name(self):
        np.random.seed(1997)
        x_sr = pd.Series(np.cumprod(1 + np.random.randn(10) * 0.01))
        zz_f = ZigZagBuilder(0.01, -0.0001)

        asserted_sr = zz_f.build_flags(x_sr)        
        self.assertEqual(zzb.FLAG_COL_NAME, asserted_sr.name)
       
    def test_values(self):
        np.random.seed(1997)
        x_sr = pd.Series(np.cumprod(1 + np.random.randn(10) * 0.01))
        zz_f = ZigZagBuilder(0.01, -0.0001)

        asserted_sr = zz_f.build_values(x_sr)
        expected_sr = pd.Series([1.0044463998665076,   1.0046937332832246,   1.0045308129101491,   1.0151116686597472,   1.0256925244093453,   1.0362733801589432,   1.0468542359085413,   1.0574350916581394,   1.0611845576172567,   1.0649340235763742])
        
        self.logger.debug(x_sr)
        self.logger.debug(zz_f.build_flags(x_sr))
        self.logger.debug(asserted_sr)

        self.assertEqual(len(asserted_sr), len(expected_sr))
        for i in range(len(expected_sr)):
            self.logger.debug(f"Compare")
            self.assertEqual(expected_sr[i], asserted_sr[i], msg=f"index {i}")

    def test_value_def_name(self):
        np.random.seed(1997)
        x_sr = pd.Series(np.cumprod(1 + np.random.randn(10) * 0.01))
        zz_f = ZigZagBuilder(0.01, -0.0001)

        asserted_sr = zz_f.build_values(x_sr)
        self.assertEqual(zzb.VALUE_COL_NAME, asserted_sr.name)    

    def test_angle(self):
        np.random.seed(1997)
        x_sr = pd.Series(np.cumprod(1 + np.random.randn(10) * 0.01))
        zz_f = ZigZagBuilder(0.01, -0.0001)

        asserted_sr = zz_f.build_angle(x_sr)
        expected_sr = pd.Series([
            1.0046937332832246-1.0044463998665076,   
            1.0045308129101491-1.0046937332832246,   
            1.0151116686597472-1.0045308129101491,   
            1.0256925244093453-1.0151116686597472,   
            1.0362733801589432-1.0256925244093453,   
            1.0468542359085413-1.0362733801589432,   
            1.0574350916581394-1.0468542359085413,   
            1.0611845576172567-1.0574350916581394,   
            1.0649340235763742-1.0611845576172567,   
            np.NaN])
        
        self.logger.debug(x_sr)
        self.logger.debug(zz_f.build_flags(x_sr))
        self.logger.debug(zz_f.build_angle(x_sr))
        self.logger.debug(asserted_sr)

        self.assertEqual(len(asserted_sr), len(expected_sr))
        for i in range(len(expected_sr)):
            self.logger.debug(f"Compare")
            if i != len(expected_sr)-1:
                self.assertEqual(expected_sr[i], asserted_sr[i], msg=f"index {i}")
            else:
                self.assertTrue(np.isnan(asserted_sr[i]))

    def test_angle_name(self):
        np.random.seed(1997)
        x_sr = pd.Series(np.cumprod(1 + np.random.randn(10) * 0.01))
        zz_f = ZigZagBuilder(0.01, -0.0001)

        asserted_sr = zz_f.build_angle(x_sr)

        self.assertEqual(asserted_sr.name, zzb.ANGLE_COL_NAME)

    def test_nearest_ext(self):
        np.random.seed(1997)

        x_sr = pd.Series(data=[
                                1.004446,
                                1.004556,
                                1.004694,
                                1.004531,
                                1.006831,
                                1.019180,
                                1.039182,
                                1.050652,
                                1.057435,
                                1.054692,
                                1.064934
                            ],
                        name="V")
        x_sr.index = x_sr.index.values
        zz_f = ZigZagBuilder(0.01, -0.0001)

        asserted_sr = zz_f.build_nearest_ext(x_sr)
        flag_sr = zz_f.build_flags(x_sr)
        expected_sr = pd.Series([
                                    1.004694,
                                    1.004694,
                                    1.004531,
                                    1.064934,
                                    1.064934,
                                    1.064934,
                                    1.064934,
                                    1.064934,
                                    1.064934,
                                    1.064934,
                                    np.NaN
                                ])
        
        self.logger.debug(pd.concat([x_sr,flag_sr, asserted_sr],axis=1))
        self.assertEqual(len(asserted_sr), len(expected_sr))
        for i in range(len(expected_sr)):
            if i != len(expected_sr)-1:
                self.assertEqual(expected_sr[i], asserted_sr[i], msg=f"index {i}")
            else:
                self.assertTrue(np.isnan(asserted_sr[i]))
            
    
    def test_nearest_ext_name(self):
        np.random.seed(1997)
        x_sr = pd.Series(np.cumprod(1 + np.random.randn(10) * 0.01))
        zz_f = ZigZagBuilder(0.01, -0.0001)

        asserted_sr = zz_f.build_nearest_ext(x_sr)

        self.assertEqual(asserted_sr.name, zzb.NEAREST_EXT_COL_NAME)

        
    def test_delta_to_near_ext(self):
        np.random.seed(1997)

        x_sr = pd.Series(data=[
                                1.004446,
                                1.004556,
                                1.004694,
                                1.004531,
                                1.006831,
                                1.019180,
                                1.039182,
                                1.050652,
                                1.057435,
                                1.054692,
                                1.064934
                            ],
                        name="V")
        x_sr.index = x_sr.index.values
        zz_f = ZigZagBuilder(0.01, -0.0001)

        asserted_sr = zz_f.build_delta_to_near_ext(x_sr)
        near_ext_sr = zz_f.build_nearest_ext(x_sr)
        expected_sr = pd.Series([
                                    1.004694-1.004446,
                                    1.004694-1.004556,
                                    1.004531-1.004694,
                                    1.064934-1.004531,
                                    1.064934-1.006831,
                                    1.064934-1.019180,
                                    1.064934-1.039182,
                                    1.064934-1.050652,
                                    1.064934-1.057435,
                                    1.064934-1.054692,
                                    np.NaN
                                ])
        self.logger.debug(pd.concat([x_sr,near_ext_sr, asserted_sr],axis=1))
        self.assertEqual(len(asserted_sr), len(expected_sr))
        for i in range(len(expected_sr)):
            if i != len(expected_sr)-1:
                self.assertEqual(expected_sr[i], asserted_sr[i], msg=f"index {i}")
            else:
                self.assertTrue(np.isnan(asserted_sr[i]))
    
    def test_delta_to_near_ext_name(self):
        np.random.seed(1997)

        x_sr = pd.Series(np.cumprod(1 + np.random.randn(10) * 0.01))
        x_sr.index = x_sr.index.values
        zz_f = ZigZagBuilder(0.01, -0.0001)

        asserted_sr = zz_f.build_delta_to_near_ext(x_sr)
        
        self.assertEqual(asserted_sr.name, zzb.DELTA_NEAR_EXT_COL_NAME)


    def test_index_return_same_index__check(self):
        np.random.seed(1997)
        X = np.cumprod(1 + np.random.randn(300) * 0.01)
        start_date = date(2000,1,1)
        x_dt_idx = []
        for i in range(300):
            x_dt_idx.append(start_date)
            start_date = start_date+timedelta(days=1)
            while start_date.weekday() >= 5:
                start_date = start_date+timedelta(days=1)

        x_sr = pd.Series(X,index=x_dt_idx)
        zz_df = ZigZagBuilder(0.01, -0.0001).build_all(x_sr)

        self.assertTrue((np.array(x_sr.index) == np.array(zz_df.index)).all())

        zz_df = ZigZagBuilder(0.01, -0.0001).build_angle(x_sr)

        self.assertTrue((np.array(x_sr.index) == np.array(zz_df.index)).all())

        zz_df = ZigZagBuilder(0.01, -0.0001).build_delta_to_near_ext(x_sr)

        self.assertTrue((np.array(x_sr.index) == np.array(zz_df.index)).all())

        zz_df = ZigZagBuilder(0.01, -0.0001).build_flags(x_sr)

        self.assertTrue((np.array(x_sr.index) == np.array(zz_df.index)).all())

        zz_df = ZigZagBuilder(0.01, -0.0001).build_nearest_ext(x_sr)

        self.assertTrue((np.array(x_sr.index) == np.array(zz_df.index)).all())

        zz_df = ZigZagBuilder(0.01, -0.0001).build_values(x_sr)

        self.assertTrue((np.array(x_sr.index) == np.array(zz_df.index)).all())

    def test_values_if_index_is_dt(self):
        np.random.seed(1997)
        
        start_date = date(2000,1,1)
        x_dt_idx = []
        for i in range(10):
            x_dt_idx.append(start_date)
            start_date = start_date+timedelta(days=1)
            while start_date.weekday() >= 5:
                start_date = start_date+timedelta(days=1)
        
        x_sr = pd.Series(np.cumprod(1 + np.random.randn(10) * 0.01), index=x_dt_idx)

        zz_f = ZigZagBuilder(0.01, -0.0001)

        asserted_sr = zz_f.build_values(x_sr)
        expected_sr = pd.Series([1.0044463998665076,   1.0046937332832246,   1.0045308129101491,   1.0151116686597472,   1.0256925244093453,   1.0362733801589432,   1.0468542359085413,   1.0574350916581394,   1.0611845576172567,   1.0649340235763742], index=x_dt_idx)
        
        self.logger.debug(x_sr)
        self.logger.debug(zz_f.build_flags(x_sr))
        self.logger.debug(asserted_sr)

        self.assertEqual(len(asserted_sr), len(expected_sr))
        for i in x_dt_idx:
            self.logger.debug(f"Compare")
            self.assertEqual(expected_sr[i], asserted_sr[i], msg=f"index {i}")


    def test_index_next_ext(self):
        np.random.seed(1997)
        
        start_date = date(2000,1,1)
        x_dt_idx = []
        for i in range(10):
            x_dt_idx.append(start_date)
            start_date = start_date+timedelta(days=1)
            while start_date.weekday() >= 5:
                start_date = start_date+timedelta(days=1)
        
        x_sr = pd.Series(np.cumprod(1 + np.random.randn(10) * 0.01), index=x_dt_idx)

        zz_f = ZigZagBuilder(0.01, -0.0001)

        asserted_sr = zz_f.build_next_index(x_sr)
        expected_sr = pd.Series([   date(2000,1,3),
                                    date(2000,1,4),
                                    date(2000,1,11),
                                    date(2000,1,11),
                                    date(2000,1,11),
                                    date(2000,1,11),
                                    date(2000,1,11),
                                    date(2000,1,13),
                                    date(2000,1,13),
                                    np.NaN], index=x_dt_idx)
        
        self.logger.debug(x_sr)
        self.logger.debug(asserted_sr)
        self.logger.debug(expected_sr)

        self.assertEqual(len(asserted_sr), len(expected_sr))
        for i in x_dt_idx:
            self.logger.debug(f"Compare")
            if expected_sr[i] is not np.NaN:
                self.assertEqual(expected_sr[i], asserted_sr[i], msg=f"index {i}")
            else:
                self.assertTrue(np.isnan(asserted_sr[i]))
    
    def test_row_to_next_ext(self):
        np.random.seed(1997)
        
        start_date = date(2000,1,1)
        x_dt_idx = []
        for i in range(10):
            x_dt_idx.append(start_date)
            start_date = start_date+timedelta(days=1)
            while start_date.weekday() >= 5:
                start_date = start_date+timedelta(days=1)
        
        x_sr = pd.Series(np.cumprod(1 + np.random.randn(10) * 0.01), index=x_dt_idx)

        zz_f = ZigZagBuilder(0.01, -0.0001)

        asserted_sr = zz_f.rows_to_next_ext(x_sr)
        expected_sr = pd.Series([   1,
                                    1,
                                    5,
                                    4,
                                    3,
                                    2,
                                    1,
                                    2,
                                    1,
                                    np.NaN], index=x_dt_idx)
        
        self.logger.debug(x_sr)
        self.logger.debug(asserted_sr)
        self.logger.debug(expected_sr)

        self.assertEqual(len(asserted_sr), len(expected_sr))
        for i in x_dt_idx:
            self.logger.debug(f"Compare")
            if np.isnan(expected_sr[i]):
                self.assertTrue(np.isnan(asserted_sr[i]))
            else:
                self.assertEqual(expected_sr[i], asserted_sr[i], msg=f"index {i}")