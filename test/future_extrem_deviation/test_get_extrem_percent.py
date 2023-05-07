import unittest
import logging
import pandas as pd
from NNTrade.common.candle_col_name import HIGH, OPEN, LOW
from src.future_extrem_deviation import get_extrem_rel_of, ExtreamType
import src.future_extrem_deviation.constant.output_col_name as opcn
from parameterized import parameterized

class GetHighExtrem_no_limits_TestCase(unittest.TestCase):

  logger = logging.getLogger(__name__)
  logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                      datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
  extrem_type = ExtreamType.High
  def test_WHEN_extrem_first_THEN_return_first_value(self):
    # Array
    base_df = pd.DataFrame({OPEN: [1,2,3,4], HIGH: [15,10,12,11]}, index=[1,2,3,4])
    expected_sr = pd.Series({
      opcn.REL_OF_HIGH: (15-1)/1,
      opcn.EXTREM_OF_HIGH:15,
      opcn.IDX_OF_HIGH: 1,
      opcn.SHIFT_OF_HIGH: 0,      
    })
    
    # Act
    metric_df = get_extrem_rel_of(base_df, 4, self.extrem_type)
    asserted_sr = metric_df.iloc[0]
    
    # Assert
    self.logger.info(f"Metric DF:\n{metric_df}")
    self.logger.info(f"Expected SR:\n{expected_sr}")
    self.logger.info(f"Asserted SR:\n{asserted_sr}")
    
    self.assertTrue(expected_sr.equals(asserted_sr))

  def test_WHEN_extrem_second_THEN_return_first_value(self):
    # Array
    base_df = pd.DataFrame({OPEN: [1,2,3,4], HIGH: [11,15,12,11]}, index=[1,2,3,4])
    expected_sr = pd.Series({
      opcn.REL_OF_HIGH: (15-1)/1,
      opcn.EXTREM_OF_HIGH:15,
      opcn.IDX_OF_HIGH: 2,
      opcn.SHIFT_OF_HIGH: 1,      
    })
    
    # Act
    metric_df = get_extrem_rel_of(base_df, 4, self.extrem_type)
    asserted_sr = metric_df.iloc[0]
    
    # Assert
    self.logger.info(f"Metric DF:\n{metric_df}")
    self.logger.info(f"Expected SR:\n{expected_sr}")
    self.logger.info(f"Asserted SR:\n{asserted_sr}")
    
    self.assertTrue(expected_sr.equals(asserted_sr))
    
  def test_WHEN_extrem_after_big_fall_THEN_return_first_value(self):
    # Array
    base_df = pd.DataFrame({OPEN: [100,102,103,104], HIGH: [90,1,110,100]}, index=[1,2,3,4])
    expected_sr = pd.Series({
      opcn.REL_OF_HIGH: (110-100)/100,
      opcn.EXTREM_OF_HIGH:110,
      opcn.IDX_OF_HIGH: 3,
      opcn.SHIFT_OF_HIGH: 2,      
    })
    
    # Act
    metric_df = get_extrem_rel_of(base_df, 4, self.extrem_type)
    asserted_sr = metric_df.iloc[0]
    
    # Assert
    self.logger.info(f"Metric DF:\n{metric_df}")
    self.logger.info(f"Expected SR:\n{expected_sr}")
    self.logger.info(f"Asserted SR:\n{asserted_sr}")
    
    self.assertTrue(expected_sr.equals(asserted_sr))
    
class GetHighExtrem_with_limits_TestCase(unittest.TestCase):

  logger = logging.getLogger(__name__)
  logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                      datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
  extrem_type = ExtreamType.High
  
  @parameterized.expand([
        [110],
        [150]
    ]) 
  def test_WHEN_extrem_first_THEN_return_first_value(self, value):
    # Array
    base_df = pd.DataFrame({OPEN: [100,102,103,104], HIGH: [value,120,1,110]}, index=[1,2,3,4])
    expected_sr = pd.Series({
      opcn.REL_OF_HIGH: 0.1,
      opcn.EXTREM_OF_HIGH:110,
      opcn.IDX_OF_HIGH: 1,
      opcn.SHIFT_OF_HIGH: 0,      
    })
    
    # Act
    metric_df = get_extrem_rel_of(base_df, 4, self.extrem_type, 0.1)
    asserted_sr = metric_df.iloc[0]
    
    # Assert
    self.logger.info(f"Metric DF:\n{metric_df}")
    self.logger.info(f"Expected SR:\n{expected_sr}")
    self.logger.info(f"Asserted SR:\n{asserted_sr}")
    
    self.assertTrue(expected_sr.equals(asserted_sr.round(2)))

  @parameterized.expand([
        [110],
        [150]
    ]) 
  def test_WHEN_extrem_second_THEN_return_first_value(self, value):
    # Array
    base_df = pd.DataFrame({OPEN: [100,102,103,104], HIGH: [109,value,1,120]}, index=[1,2,3,4])
    expected_sr = pd.Series({
      opcn.REL_OF_HIGH: 0.1,
      opcn.EXTREM_OF_HIGH:110,
      opcn.IDX_OF_HIGH: 2,
      opcn.SHIFT_OF_HIGH: 1,      
    })
    
    # Act
    metric_df = get_extrem_rel_of(base_df, 4, self.extrem_type, 0.1)
    asserted_sr = metric_df.iloc[0]
    
    # Assert
    self.logger.info(f"Metric DF:\n{metric_df}")
    self.logger.info(f"Expected SR:\n{expected_sr}")
    self.logger.info(f"Asserted SR:\n{asserted_sr}")
    
    self.assertTrue(expected_sr.equals(asserted_sr.round(2)))
  
  @parameterized.expand([
        [110],
        [150]
    ]) 
  def test_WHEN_extrem_after_big_fall_THEN_return_first_value(self, value):
    # Array
    base_df = pd.DataFrame({OPEN: [100,102,103,104], HIGH: [1,1,value,120]}, index=[1,2,3,4])
    expected_sr = pd.Series({
      opcn.REL_OF_HIGH: 0.1,
      opcn.EXTREM_OF_HIGH:110,
      opcn.IDX_OF_HIGH: 3,
      opcn.SHIFT_OF_HIGH: 2,      
    })
    
    # Act
    metric_df = get_extrem_rel_of(base_df, 4, self.extrem_type, 0.1)
    asserted_sr = metric_df.iloc[0]
    
    # Assert
    self.logger.info(f"Metric DF:\n{metric_df}")
    self.logger.info(f"Expected SR:\n{expected_sr}")
    self.logger.info(f"Asserted SR:\n{asserted_sr}")
    
    self.assertTrue(expected_sr.equals(asserted_sr.round(2)))
    
  def test_WHEN_extrem_doesnot_reach_limit_THEN_return_first_value(self):
    # Array
    base_df = pd.DataFrame({OPEN: [100,102,103,104], HIGH: [1,1,105,106]}, index=[1,2,3,4])
    expected_sr = pd.Series({
      opcn.REL_OF_HIGH: (106-100)/100,
      opcn.EXTREM_OF_HIGH:106,
      opcn.IDX_OF_HIGH: 4,
      opcn.SHIFT_OF_HIGH: 3,      
    })
    
    # Act
    metric_df = get_extrem_rel_of(base_df, 4, self.extrem_type, 0.1)
    asserted_sr = metric_df.iloc[0]
    
    # Assert
    self.logger.info(f"Metric DF:\n{metric_df}")
    self.logger.info(f"Expected SR:\n{expected_sr}")
    self.logger.info(f"Asserted SR:\n{asserted_sr}")
    
    self.assertTrue(expected_sr.equals(asserted_sr))

class GetLowExtrem_no_limits_TestCase(unittest.TestCase):

  logger = logging.getLogger(__name__)
  logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                      datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
  extrem_type = ExtreamType.Low
  def test_WHEN_extrem_first_THEN_return_first_value(self):
    # Array
    base_df = pd.DataFrame({OPEN: [100,102,103,104], LOW: [80,90,120,110]}, index=[1,2,3,4])
    expected_sr = pd.Series({
      opcn.REL_OF_LOW: (80-100)/100,
      opcn.EXTREM_OF_LOW:80,
      opcn.IDX_OF_LOW: 1,
      opcn.SHIFT_OF_LOW: 0,      
    })
    
    # Act
    metric_df = get_extrem_rel_of(base_df, 4, self.extrem_type)
    asserted_sr = metric_df.iloc[0]
    
    # Assert
    self.logger.info(f"Metric DF:\n{metric_df}")
    self.logger.info(f"Expected SR:\n{expected_sr}")
    self.logger.info(f"Asserted SR:\n{asserted_sr}")
    
    self.assertTrue(expected_sr.equals(asserted_sr))

  def test_WHEN_extrem_second_THEN_return_first_value(self):
    # Array
    base_df = pd.DataFrame({OPEN: [100,102,103,104], LOW: [90,80,120,110]}, index=[1,2,3,4])
    expected_sr = pd.Series({
      opcn.REL_OF_LOW: (80-100)/100,
      opcn.EXTREM_OF_LOW:80,
      opcn.IDX_OF_LOW: 2,
      opcn.SHIFT_OF_LOW: 1,      
    })
    
    # Act
    metric_df = get_extrem_rel_of(base_df, 4, self.extrem_type)
    asserted_sr = metric_df.iloc[0]
    
    # Assert
    self.logger.info(f"Metric DF:\n{metric_df}")
    self.logger.info(f"Expected SR:\n{expected_sr}")
    self.logger.info(f"Asserted SR:\n{asserted_sr}")
    
    self.assertTrue(expected_sr.equals(asserted_sr))
    
  def test_WHEN_extrem_after_big_raise_THEN_return_first_value(self):
    # Array
    base_df = pd.DataFrame({OPEN: [100,102,103,104], LOW: [90,300,80,110]}, index=[1,2,3,4])
    expected_sr = pd.Series({
      opcn.REL_OF_LOW: (80-100)/100,
      opcn.EXTREM_OF_LOW:80,
      opcn.IDX_OF_LOW: 3,
      opcn.SHIFT_OF_LOW: 2,      
    })
    
    # Act
    metric_df = get_extrem_rel_of(base_df, 4, self.extrem_type)
    asserted_sr = metric_df.iloc[0]
    
    # Assert
    self.logger.info(f"Metric DF:\n{metric_df}")
    self.logger.info(f"Expected SR:\n{expected_sr}")
    self.logger.info(f"Asserted SR:\n{asserted_sr}")
    
    self.assertTrue(expected_sr.equals(asserted_sr))

class GetLowExtrem_with_limits_TestCase(unittest.TestCase):

  logger = logging.getLogger(__name__)
  logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                      datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
  extrem_type = ExtreamType.Low
  
  @parameterized.expand([
        [90],
        [50]
    ]) 
  def test_WHEN_extrem_first_THEN_return_first_value(self, value):
    # Array
    base_df = pd.DataFrame({OPEN: [100,102,103,104], LOW: [value,90,120,110]}, index=[1,2,3,4])
    expected_sr = pd.Series({
      opcn.REL_OF_LOW: -0.1,
      opcn.EXTREM_OF_LOW:90,
      opcn.IDX_OF_LOW: 1,
      opcn.SHIFT_OF_LOW: 0,      
    })
    
    # Act
    metric_df = get_extrem_rel_of(base_df, 4, self.extrem_type, 0.1)
    asserted_sr = metric_df.iloc[0]
    
    # Assert
    self.logger.info(f"Metric DF:\n{metric_df}")
    self.logger.info(f"Expected SR:\n{expected_sr}")
    self.logger.info(f"Asserted SR:\n{asserted_sr}")
    
    self.assertTrue(expected_sr.equals(asserted_sr))

  @parameterized.expand([
      [90],
      [50]
  ]) 
  def test_WHEN_extrem_second_THEN_return_first_value(self, value):
    # Array
    base_df = pd.DataFrame({OPEN: [100,102,103,104], LOW: [91,value,1200,110]}, index=[1,2,3,4])
    expected_sr = pd.Series({
      opcn.REL_OF_LOW: (90-100)/100,
      opcn.EXTREM_OF_LOW:90,
      opcn.IDX_OF_LOW: 2,
      opcn.SHIFT_OF_LOW: 1,      
    })
    
    # Act
    metric_df = get_extrem_rel_of(base_df, 4, self.extrem_type, 0.1)
    asserted_sr = metric_df.iloc[0]
    
    # Assert
    self.logger.info(f"Metric DF:\n{metric_df}")
    self.logger.info(f"Expected SR:\n{expected_sr}")
    self.logger.info(f"Asserted SR:\n{asserted_sr}")
    
    self.assertTrue(expected_sr.equals(asserted_sr))
  
  @parameterized.expand([
      [90],
      [50]
  ]) 
  def test_WHEN_extrem_after_big_raise_THEN_return_first_value(self, value):
    # Array
    base_df = pd.DataFrame({OPEN: [100,102,103,104], LOW: [91,1000,value,110]}, index=[1,2,3,4])
    expected_sr = pd.Series({
      opcn.REL_OF_LOW: -0.1,
      opcn.EXTREM_OF_LOW:90,
      opcn.IDX_OF_LOW: 3,
      opcn.SHIFT_OF_LOW: 2,      
    })
    
    # Act
    metric_df = get_extrem_rel_of(base_df, 4, self.extrem_type, 0.1)
    asserted_sr = metric_df.iloc[0]
    
    # Assert
    self.logger.info(f"Metric DF:\n{metric_df}")
    self.logger.info(f"Expected SR:\n{expected_sr}")
    self.logger.info(f"Asserted SR:\n{asserted_sr}")
    
    self.assertTrue(expected_sr.equals(asserted_sr))
    
  def test_WHEN_extrem_doesnot_reach_limit_THEN_return_first_value(self):
    # Array
    base_df = pd.DataFrame({OPEN: [100,102,103,104], LOW: [91,1000,91,110]}, index=[1,2,3,4])
    expected_sr = pd.Series({
      opcn.REL_OF_LOW: (91-100)/100,
      opcn.EXTREM_OF_LOW:91,
      opcn.IDX_OF_LOW: 1,
      opcn.SHIFT_OF_LOW: 0,      
    })
    
    # Act
    metric_df = get_extrem_rel_of(base_df, 4, self.extrem_type, 0.1)
    asserted_sr = metric_df.iloc[0]
    
    # Assert
    self.logger.info(f"Metric DF:\n{metric_df}")
    self.logger.info(f"Expected SR:\n{expected_sr}")
    self.logger.info(f"Asserted SR:\n{asserted_sr}")
    
    self.assertTrue(expected_sr.equals(asserted_sr))

class GetExtremPercentOf_TestCase(unittest.TestCase):

  logger = logging.getLogger(__name__)
  logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                      datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
    
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