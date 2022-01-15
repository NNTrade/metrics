import unittest
from src.FuturePercentStepMatrix.Builder import BuildMatrix, Compare
from src.FuturePercentStepMatrix.Factory import Factory
import logging
import pandas as pd
import numpy as np


class FactoryTestCase(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    def test_GetInExterem(self):

        base_value_sr = pd.Series([1, 2, 4], name="cls", index=[
                                  "A1", "B2", "C3"])
        value_df = pd.DataFrame({"H": [100, 2.5, 2],"L": [50, 1, 5]}, index=base_value_sr.index).join(base_value_sr)

        expect_matrix = pd.DataFrame({
            "P(VH149)[ESh1-cls]": [True, True, np.NAN],
            "P(VH151)[ESh1-cls]": [False, False, np.NAN],
            "P(VH401)[ESh1-cls]": [False, False, np.NAN],
            "P(VH149)[ESh2-cls]": [True, np.NAN, np.NAN],
            "P(VH151)[ESh2-cls]": [True, np.NAN, np.NAN],
            "P(VH401)[ESh2-cls]": [False, np.NAN, np.NAN]
        }, index=["A1", "B2", "C3"])

        fctr = Factory(use_abs=False)
        assert_matrix = fctr.GetInExterem(base_value_sr, value_df, [1, 2], [
                                          149, 151,401], compare=Compare.VolatilityHigher, use_first=False)

        self.assertEqual(len(assert_matrix.columns),
                         len(expect_matrix.columns))
        self.assertEqual(len(assert_matrix), len(expect_matrix))
        for col in assert_matrix:
            self.logger.info(f"Col:{col}")
            self.logger.info(assert_matrix[col])
            for idx in assert_matrix.index:
                if np.isnan(assert_matrix[col][idx]):
                    self.assertTrue(np.isnan(expect_matrix[col][idx]), f"{col} idx {idx}")
                else:
                    self.assertEqual(
                        assert_matrix[col][idx], expect_matrix[col][idx], f"{col} idx {idx}")


