from re import X
import unittest
from src.ZigZag.Configurator.IsCorrectFunctions import Check_len_size,Check_machine,no_same_move_direction_is_correct
import src.ZigZag.Constant as zzb
import pandas as pd
import numpy as np
import logging

class Check_len_sizeTestCase(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(format = '%(asctime)s %(module)s %(levelname)s: %(message)s',
                    datefmt = '%m/%d/%Y %I:%M:%S %p', level = logging.DEBUG)
    
    def test_min_len__check(self):
        checker = Check_len_size(min_len=4)
        
        df = pd.DataFrame([1,0,0,-1,0,0,0,0,0,0,0,0,1],columns=[zzb.FLAG_COL_NAME])

        self.assertFalse(checker.is_correct(df))

        df2 = pd.DataFrame([1,0,0,0,-1,0,0,0,0,0,0,0,0,1],columns=[zzb.FLAG_COL_NAME])    

        self.assertTrue(checker.is_correct(df2))

    def test_max_len__check_is_incorrect(self):
        checker = Check_len_size(max_len=4)
        
        df = pd.DataFrame([1,0,0,-1,0,0,0,0,0,0,0,0,1],columns=[zzb.FLAG_COL_NAME])

        self.assertFalse(checker.is_correct(df))

    def test_max_len__check_is_correct(self):
        checker = Check_len_size(min_len = np.NAN,max_len=4)

        df2 = pd.DataFrame([1,0,0,0,-1,0,0,0,-1,0,0,1,0,-1],columns=[zzb.FLAG_COL_NAME])    

        self.assertTrue(checker.is_correct(df2))


class Checking_listTestCase(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(format = '%(asctime)s %(module)s %(levelname)s: %(message)s',
                    datefmt = '%m/%d/%Y %I:%M:%S %p', level = logging.DEBUG)

    def test_check(self):
        
        checker = Check_len_size(min_len=4)
        checker_manager = Check_machine([no_same_move_direction_is_correct,checker.is_correct])
        
        df = pd.DataFrame([[1,-1],[0,-1],[0,-1],[-1,1],[0,1],[0,1],[0,1],[0,1],[0,1],[1,np.NAN]],columns=[zzb.FLAG_COL_NAME,zzb.ANGLE_COL_NAME])

        self.assertFalse(checker_manager.is_correct(df))

        df2 = pd.DataFrame([[1,-1],[0,-1],[0,-1],[0,-1],[-1,-1],[0,1],[0,1],[0,1],[0,1],[0,1],[1,np.NAN]],columns=[zzb.FLAG_COL_NAME,zzb.ANGLE_COL_NAME])

        self.assertFalse(checker_manager.is_correct(df2))

        df3 = pd.DataFrame([[1,-1],[0,-1],[0,-1],[0,-1],[-1,1],[0,1],[0,1],[0,1],[0,1],[0,1],[1,np.NAN]],columns=[zzb.FLAG_COL_NAME,zzb.ANGLE_COL_NAME])

        self.assertTrue(checker_manager.is_correct(df3))
