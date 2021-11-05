from re import X
import unittest
from src.ZigZag.Configurator.CorrectChecking import Check_len_size,Check_machine,check_no_same_move_direction
import src.ZigZag.Constant as zzb
import pandas as pd
import numpy as np
import logging

class Check_len_sizeTestCase(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(format = '%(asctime)s %(module)s %(levelname)s: %(message)s',
                    datefmt = '%m/%d/%Y %I:%M:%S %p', level = logging.DEBUG)
    
    def test_check(self):
        checker = Check_len_size(min_len=4)
        
        df = pd.DataFrame([1,0,0,-1,0,0,0,0,0,0,0,0,1],columns=[zzb.FLAG_COL_NAME])

        self.assertFalse(checker.check(df))

        df2 = pd.DataFrame([1,0,0,0,-1,0,0,0,0,0,0,0,0,1],columns=[zzb.FLAG_COL_NAME])    

        self.assertTrue(checker.check(df2))


class Checking_listTestCase(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(format = '%(asctime)s %(module)s %(levelname)s: %(message)s',
                    datefmt = '%m/%d/%Y %I:%M:%S %p', level = logging.DEBUG)

    def test_check(self):
        
        checker = Check_len_size(min_len=4)
        checker_manager = Check_machine([check_no_same_move_direction,checker.check])
        
        df = pd.DataFrame([[1,-1],[0,-1],[0,-1],[-1,1],[0,1],[0,1],[0,1],[0,1],[0,1],[1,np.NAN]],columns=[zzb.FLAG_COL_NAME,zzb.ANGLE_COL_NAME])

        self.assertFalse(checker_manager.check_is_correct(df))

        df2 = pd.DataFrame([[1,-1],[0,-1],[0,-1],[0,-1],[-1,-1],[0,1],[0,1],[0,1],[0,1],[0,1],[1,np.NAN]],columns=[zzb.FLAG_COL_NAME,zzb.ANGLE_COL_NAME])

        self.assertFalse(checker_manager.check_is_correct(df2))

        df3 = pd.DataFrame([[1,-1],[0,-1],[0,-1],[0,-1],[-1,1],[0,1],[0,1],[0,1],[0,1],[0,1],[1,np.NAN]],columns=[zzb.FLAG_COL_NAME,zzb.ANGLE_COL_NAME])

        self.assertTrue(checker_manager.check_is_correct(df3))
