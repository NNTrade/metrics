import unittest
import logging
import pandas as pd
from NNTrade.common.candle_col_name import HIGH, OPEN, LOW
from src.future_extrem_deviation import get_extrem_rel_of, ExtreamType
class GetExtremPercentOf_TestCase(unittest.TestCase):

  logger = logging.getLogger(__name__)
  logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                      datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

  def test_WHEN_request_extrem_rel_THEN_get_correct_values(self):
    # Array
    base_df = pd.DataFrame({OPEN: [1,10,100,1000], HIGH: [10,15,12,11]}, index=[1,2,3,4])
    excepted_df = pd.DataFrame({"Rel_of_High":[(15-1)/1, (15-10)/10, (12-100)/100, (11-1000)/1000], "Idx_of_High":[2.0,2.0,3.0,4.0],"Shift_to_High":[1,0,0,0] }, index=[1,2,3,4])
    
    # Act
    asserted_df = get_extrem_rel_of(base_df, 2, ExtreamType.High)
    
    # Assert
    self.logger.info("Expected DF")
    self.logger.info(excepted_df)
    self.logger.info("Asserted DF")
    self.logger.info(asserted_df)
    self.assertTrue(excepted_df.equals(asserted_df))
    
  def test_WHEN_request_extrem_rel_low_THEN_get_correct_values(self):
    # Array
    base_df = pd.DataFrame({OPEN: [1,10,100,1000], LOW: [10,15,12,11]}, index=[1,2,3,4])
    excepted_df = pd.DataFrame({"Rel_of_Low":[(10-1)/1, (12-10)/10, (11-100)/100, (11-1000)/1000], "Idx_of_Low":[1.0,3.,4.,4.],"Shift_to_Low":[0,1,1,0] }, index=[1,2,3,4])
    
    # Act
    asserted_df = get_extrem_rel_of(base_df, 2, ExtreamType.Low)
    
    # Assert
    self.logger.info("Expected DF")
    self.logger.info(excepted_df)
    self.logger.info("Asserted DF")
    self.logger.info(asserted_df)
    self.assertTrue(excepted_df.equals(asserted_df))
    
  def test_WHEN_request_extrem_rel_in_zero_period_THEN_get_correct_values(self):
    # Array
    base_df = pd.DataFrame({OPEN: [1,10,100,1000], HIGH: [10,15,12,11]}, index=[1,2,3,4])
    excepted_df = pd.DataFrame({"Rel_of_High":[(10-1)/1, (15-10)/10, (12-100)/100, (11-1000)/1000], "Idx_of_High":[1,2,3,4],"Shift_to_High":[0,0,0,0] }, index=[1,2,3,4])
    
    # Act
    asserted_df = get_extrem_rel_of(base_df, 1, ExtreamType.High)
    
    # Assert
    self.logger.info("Expected DF")
    self.logger.info(excepted_df)
    self.logger.info("Asserted DF")
    self.logger.info(asserted_df)
    self.assertTrue(excepted_df.equals(asserted_df))
    

  def test_WHEN_request_extrem_rel_with_limit_THEN_get_correct_values(self):
    # Array
    base_df = pd.DataFrame({OPEN: [1,10,100,1000], HIGH: [10,15,12,11]}, index=[1,2,3,4])
    
    excepted_df = pd.DataFrame({"Rel_of_High":[(10-1)/1, (15-10)/10, (12-100)/100, (11-1000)/1000], "Idx_of_High":[1.0,2.0,3.0,4.0],"Shift_to_High":[0,0,0,0] }, index=[1,2,3,4])
    
    # Act
    asserted_df = get_extrem_rel_of(base_df, 2, ExtreamType.High, 9)
    
    # Assert
    self.logger.info("First value must be 9 (10-1)/1, not 14 (15-1)/1")
    self.logger.info("Expected DF")
    self.logger.info(excepted_df)
    self.logger.info("Asserted DF")
    self.logger.info(asserted_df)
    self.assertTrue(excepted_df.equals(asserted_df))
    
  def test_WHEN_request_extrem_rel_with_limit_THEN_get_correct_first_reach_values(self):
    # Array
    base_df = pd.DataFrame({OPEN: [1,10,100,1000], HIGH: [10,15,12,11]}, index=[1,2,3,4])
    
    excepted_df = pd.DataFrame({"Rel_of_High":[(15-1)/1, (15-10)/10, (12-100)/100, (11-1000)/1000], "Idx_of_High":[2.0,2.0,3.0,4.0],"Shift_to_High":[1,0,0,0] }, index=[1,2,3,4])
    
    # Act
    asserted_df = get_extrem_rel_of(base_df, 3, ExtreamType.High, 10)
    
    # Assert
    self.logger.info("First value must be 14 (15-1)/1, not 11 (12-1)/1")
    self.logger.info("Expected DF")
    self.logger.info(excepted_df)
    self.logger.info("Asserted DF")
    self.logger.info(asserted_df)
    self.assertTrue(excepted_df.equals(asserted_df))
    
  def test_WHEN_request_extrem_rel_low_with_limit_THEN_get_correct_values(self):
    # Array
    base_df = pd.DataFrame({OPEN: [1,10,100,1000], LOW: [10,15,12,11]}, index=[1,2,3,4])
    excepted_df = pd.DataFrame({"Rel_of_Low":[(10-1)/1, (12-10)/10, (11-100)/100, (11-1000)/1000], "Idx_of_Low":[1.0,3.,4.,4.],"Shift_to_Low":[0,1,1,0] }, index=[1,2,3,4])
    
    # Act
    asserted_df = get_extrem_rel_of(base_df, 2, ExtreamType.Low, 9)
    
    # Assert
    self.logger.info("Expected DF")
    self.logger.info(excepted_df)
    self.logger.info("Asserted DF")
    self.logger.info(asserted_df)
    self.assertTrue(excepted_df.equals(asserted_df))
    
  def test_WHEN_give_negative_limit_THEN_get_error(self):
    # Array
    base_df = pd.DataFrame({OPEN: [1,10,100,1000], LOW: [10,15,12,11]}, index=[1,2,3,4])
    # Act

    # Assert
    self.assertRaises(AttributeError, lambda : get_extrem_rel_of(base_df, 2, ExtreamType.Low, -9))
  def test_WHEN_give_zero_limit_THEN_get_error(self):
    # Array
    base_df = pd.DataFrame({OPEN: [1,10,100,1000], LOW: [10,15,12,11]}, index=[1,2,3,4])
    # Act

    # Assert
    self.assertRaises(AttributeError, lambda : get_extrem_rel_of(base_df, 2, ExtreamType.Low, 0))