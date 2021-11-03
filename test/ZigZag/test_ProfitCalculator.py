import unittest
import logging
import pandas as pd
from src.ZigZag.Constant import FLAG_COL_NAME, VALUE_COL_NAME, DELTA_NEAR_EXT
from src.ZigZag.ProfitCalculator import get_profit

class ProfitCalculatorTestCase(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(format = '%(asctime)s %(module)s %(levelname)s: %(message)s',
                    datefmt = '%m/%d/%Y %I:%M:%S %p', level = logging.DEBUG)

    def test_profitCalculation__check(self):
        zz_df = pd.DataFrame(data=[[1, 1, 0.5],[-1, 1.5, 0.75]],columns=[FLAG_COL_NAME, VALUE_COL_NAME, DELTA_NEAR_EXT])
        
        asserted_df = get_profit(zz_df)

        self.assertEqual(0.5+0.5, asserted_df["sum"])
        self.assertEqual(1.5*1.5, asserted_df["prod"])