import unittest
import logging
import pandas as pd
from NNTrade.common.candle_col_name import OPEN, HIGH, LOW, CLOSE
from src.future_profit_by_limits.get_profit_by_limits import get_profit_by_limit, direction
import src.future_profit_by_limits.constant.output_col_name as opcn
from src.future_profit_by_limits.constant.closing_types import ClosingType
from parameterized import parameterized

class ProfitForLongDirection_TestCase(unittest.TestCase):

  logger = logging.getLogger(__name__)
  logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                      datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
  direction = direction.Long
  
  @parameterized.expand([
        [9],
        [5]
    ])
  def test_WHEN_first_reach_loss_limit_THEN_exit_1(self, loss_value):
    # Array
    # 1-st candle reach loss
    # last candle reach income limit
    quote_df = pd.DataFrame({OPEN:[10,12,13], LOW:[loss_value,11,9], HIGH:[11,13,15], CLOSE:[10,12,13]}, index=[1,2,3])
    expected_sr = pd.Series({
      opcn.PROFIT:-0.1,
      opcn.CLOSE_PRICE:9, 
      opcn.SHIFT_TO_CLOSE:0,
      opcn.IDX_OF_CLOSE:1, 
      opcn.TYPE_OF_CLOSE: ClosingType.OnLossLimit
      }, name=1)
        
    # Act
    metric_df = get_profit_by_limit(quote_df, self.direction,0.5,0.1,3)
    asserted_sr = metric_df.iloc[0]
    # Assert
    self.logger.info(f"Metric DF:\n{metric_df}")
    self.logger.info(f"Expected SR:\n{expected_sr}")
    self.logger.info(f"Asserted SR:\n{asserted_sr}")
    
    self.assertTrue(expected_sr.equals(asserted_sr))
  
  @parameterized.expand([
        [9],
        [5]
    ])
  def test_WHEN_first_reach_loss_limit_THEN_exit_2(self, loss_value):
    # Array
    # 2-nd candle reach loss
    # last candle reach income limit
    quote_df = pd.DataFrame({OPEN:[10,12,13], LOW:[10,loss_value,10], HIGH:[11,13,15], CLOSE:[10,12,13]}, index=[1,2,3])
    expected_sr = pd.Series({
      opcn.PROFIT:-0.1,
      opcn.CLOSE_PRICE:9, 
      opcn.SHIFT_TO_CLOSE:1,
      opcn.IDX_OF_CLOSE:2, 
      opcn.TYPE_OF_CLOSE: ClosingType.OnLossLimit
      }, name=1)
        
    # Act
    metric_df = get_profit_by_limit(quote_df, self.direction,0.5,0.1,3)
    asserted_sr = metric_df.iloc[0]
    # Assert
    self.logger.info(f"Metric DF:\n{metric_df}")
    self.logger.info(f"Expected SR:\n{expected_sr}")
    self.logger.info(f"Asserted SR:\n{asserted_sr}")
    
    self.assertTrue(expected_sr.equals(asserted_sr))  
  
  @parameterized.expand([
        [9],
        [5]
    ])
  def test_WHEN_first_reach_loss_limit_THEN_exit_3(self, loss_value):
    # Array
    # 2-nd candle reach loss
    # no reach income limit
    quote_df = pd.DataFrame({OPEN:[10,12,13], LOW:[10,loss_value,10], HIGH:[11,13,14], CLOSE:[10,12,13]}, index=[1,2,3])
    expected_sr = pd.Series({
      opcn.PROFIT:-0.1,
      opcn.CLOSE_PRICE:9, 
      opcn.SHIFT_TO_CLOSE:1,
      opcn.IDX_OF_CLOSE:2, 
      opcn.TYPE_OF_CLOSE: ClosingType.OnLossLimit
      }, name=1)
        
    # Act
    metric_df = get_profit_by_limit(quote_df, self.direction,0.5,0.1,3)
    asserted_sr = metric_df.iloc[0]
    # Assert
    self.logger.info(f"Metric DF:\n{metric_df}")
    self.logger.info(f"Expected SR:\n{expected_sr}")
    self.logger.info(f"Asserted SR:\n{asserted_sr}")
    
    self.assertTrue(expected_sr.equals(asserted_sr))  
  
  @parameterized.expand([
        [15],
        [19]
    ])
  def test_WHEN_first_reach_income_limit_THEN_exit_1(self, income_value):
    # Array
    # 1-st candle reach income
    # last candle reach loss limit
    quote_df = pd.DataFrame({OPEN:[10,12,13], LOW:[10,11,9], HIGH:[income_value,13,15], CLOSE:[10,12,13]}, index=[1,2,3])
    expected_sr = pd.Series({
      opcn.PROFIT:0.5,
      opcn.CLOSE_PRICE:15, 
      opcn.SHIFT_TO_CLOSE:0,
      opcn.IDX_OF_CLOSE:1, 
      opcn.TYPE_OF_CLOSE: ClosingType.OnIncomeLimit
      }, name=1)
        
    # Act
    metric_df = get_profit_by_limit(quote_df, self.direction,0.5,0.1,3)
    asserted_sr = metric_df.iloc[0]
    # Assert
    self.logger.info(f"Metric DF:\n{metric_df}")
    self.logger.info(f"Expected SR:\n{expected_sr}")
    self.logger.info(f"Asserted SR:\n{asserted_sr}")
    
    self.assertTrue(expected_sr.equals(asserted_sr))
  
  @parameterized.expand([
        [15],
        [19]
    ])
  def test_WHEN_first_reach_income_limit_THEN_exit_2(self, income_value):
    # Array
    # 2-nd candle reach income
    # last candle reach loss limit
    quote_df = pd.DataFrame({OPEN:[10,12,13], LOW:[10,11,9], HIGH:[11,income_value,13], CLOSE:[10,12,13]}, index=[1,2,3])
    expected_sr = pd.Series({
      opcn.PROFIT:0.5,
      opcn.CLOSE_PRICE:15, 
      opcn.SHIFT_TO_CLOSE:1,
      opcn.IDX_OF_CLOSE:2, 
      opcn.TYPE_OF_CLOSE: ClosingType.OnIncomeLimit
      }, name=1)
        
    # Act
    metric_df = get_profit_by_limit(quote_df, self.direction,0.5,0.1,3)
    asserted_sr = metric_df.iloc[0]
    # Assert
    self.logger.info(f"Metric DF:\n{metric_df}")
    self.logger.info(f"Expected SR:\n{expected_sr}")
    self.logger.info(f"Asserted SR:\n{asserted_sr}")
    
    self.assertTrue(expected_sr.equals(asserted_sr))  
    
  @parameterized.expand([
        [15],
        [19]
    ])
  def test_WHEN_first_reach_income_limit_THEN_exit_3(self, income_value):
    # Array
    # 2-nd candle reach income
    # no reach loss limit
    quote_df = pd.DataFrame({OPEN:[10,12,13], LOW:[10,11,10], HIGH:[11,income_value,14], CLOSE:[10,12,13]}, index=[1,2,3])
    expected_sr = pd.Series({
      opcn.PROFIT:0.5,
      opcn.CLOSE_PRICE:15, 
      opcn.SHIFT_TO_CLOSE:1,
      opcn.IDX_OF_CLOSE:2, 
      opcn.TYPE_OF_CLOSE: ClosingType.OnIncomeLimit
      }, name=1)
        
    # Act
    metric_df = get_profit_by_limit(quote_df, self.direction,0.5,0.1,3)
    asserted_sr = metric_df.iloc[0]
    # Assert
    self.logger.info(f"Metric DF:\n{metric_df}")
    self.logger.info(f"Expected SR:\n{expected_sr}")
    self.logger.info(f"Asserted SR:\n{asserted_sr}")
    
    self.assertTrue(expected_sr.equals(asserted_sr))  
  
  @parameterized.expand([
        [9, 15],
        [5, 19],
        [9, 19],
        [5, 15],
    ])
  def test_WHEN_both_limits_has_been_reach_at_same_candle_THEN_exit_1(self, loss_value, income_value):
    # Array
    # 1-st candle reach
    quote_df = pd.DataFrame({OPEN:[10,12,13], LOW:[loss_value,11,9], HIGH:[income_value,13,15], CLOSE:[10,12,13]}, index=[1,2,3])
    expected_sr = pd.Series({
      opcn.PROFIT:-0.1,
      opcn.CLOSE_PRICE:9, 
      opcn.SHIFT_TO_CLOSE:0,
      opcn.IDX_OF_CLOSE:1, 
      opcn.TYPE_OF_CLOSE: ClosingType.OnLossLimit
      }, name=1)
        
    # Act
    metric_df = get_profit_by_limit(quote_df, self.direction,0.5,0.1,3)
    asserted_sr = metric_df.iloc[0]
    # Assert
    self.logger.info(f"Metric DF:\n{metric_df}")
    self.logger.info(f"Expected SR:\n{expected_sr}")
    self.logger.info(f"Asserted SR:\n{asserted_sr}")
    
    self.assertTrue(expected_sr.equals(asserted_sr))  
    
  @parameterized.expand([
        [9, 15],
        [5, 19],
        [9, 19],
        [5, 15],
    ])  
  def test_WHEN_both_limits_has_been_reach_at_same_candle_THEN_exit_2(self, loss_value, income_value):
    # Array
    # last candle reach
    quote_df = pd.DataFrame({OPEN:[10,12,13], LOW:[10,11,loss_value], HIGH:[12,13,income_value], CLOSE:[10,12,13]}, index=[1,2,3])
    expected_sr = pd.Series({
      opcn.PROFIT:-0.1,
      opcn.CLOSE_PRICE:9, 
      opcn.SHIFT_TO_CLOSE:2,
      opcn.IDX_OF_CLOSE:3, 
      opcn.TYPE_OF_CLOSE: ClosingType.OnLossLimit
      }, name=1)
        
    # Act
    metric_df = get_profit_by_limit(quote_df, self.direction,0.5,0.1,3)
    asserted_sr = metric_df.iloc[0]
    # Assert
    self.logger.info(f"Metric DF:\n{metric_df}")
    self.logger.info(f"Expected SR:\n{expected_sr}")
    self.logger.info(f"Asserted SR:\n{asserted_sr}")
    
    self.assertTrue(expected_sr.equals(asserted_sr))  
  
  def test_WHEN_does_not_reach_limit_THEN_exit(self):
    # Array
    quote_df = pd.DataFrame({OPEN:[10,12,13], LOW:[10,11,10], HIGH:[11,13,14], CLOSE:[10,12,13]}, index=[1,2,3])
    expected_sr = pd.Series({
      opcn.PROFIT:(13-10)/10,
      opcn.CLOSE_PRICE:13, 
      opcn.SHIFT_TO_CLOSE:2,
      opcn.IDX_OF_CLOSE:3, 
      opcn.TYPE_OF_CLOSE: ClosingType.OnClose
      }, name=1)
        
    # Act
    metric_df = get_profit_by_limit(quote_df, self.direction,0.5,0.1,3)
    asserted_sr = metric_df.iloc[0]
    # Assert
    self.logger.info(f"Metric DF:\n{metric_df}")
    self.logger.info(f"Expected SR:\n{expected_sr}")
    self.logger.info(f"Asserted SR:\n{asserted_sr}")
    
    self.assertTrue(expected_sr.equals(asserted_sr))  
    
    
class ProfitForShortDirection_TestCase(unittest.TestCase):

  logger = logging.getLogger(__name__)
  logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                      datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
  direction = direction.Short
  
  @parameterized.expand([
        [11],
        [15]
    ]) 
  def test_WHEN_first_reach_loss_limit_THEN_exit_1(self, loss_value):
    # Array
    # 1-st candle reach loss
    # last candle reach income limit
    quote_df = pd.DataFrame({OPEN:[10,12,13], LOW:[9,11,5], HIGH:[loss_value,13,15], CLOSE:[10,12,13]}, index=[1,2,3])
    expected_sr = pd.Series({
      opcn.PROFIT:-0.1,
      opcn.CLOSE_PRICE:11, 
      opcn.SHIFT_TO_CLOSE:0,
      opcn.IDX_OF_CLOSE:1, 
      opcn.TYPE_OF_CLOSE: ClosingType.OnLossLimit
      }, name=1)
        
    # Act
    metric_df = get_profit_by_limit(quote_df, self.direction,0.5,0.1,3)
    asserted_sr = metric_df.iloc[0]
    # Assert
    self.logger.info(f"Metric DF:\n{metric_df}")
    self.logger.info(f"Expected SR:\n{expected_sr}")
    self.logger.info(f"Asserted SR:\n{asserted_sr}")
    
    self.assertTrue(expected_sr.equals(asserted_sr))
  
  @parameterized.expand([
        [11],
        [15]
    ])
  def test_WHEN_first_reach_loss_limit_THEN_exit_2(self, loss_value):
    # Array
    # 2-nd candle reach loss
    # last candle reach income limit
    quote_df = pd.DataFrame({OPEN:[10,12,13], LOW:[10,9,5], HIGH:[10,loss_value,15], CLOSE:[10,12,13]}, index=[1,2,3])
    expected_sr = pd.Series({
      opcn.PROFIT:-0.1,
      opcn.CLOSE_PRICE:11, 
      opcn.SHIFT_TO_CLOSE:1,
      opcn.IDX_OF_CLOSE:2, 
      opcn.TYPE_OF_CLOSE: ClosingType.OnLossLimit
      }, name=1)
        
    # Act
    metric_df = get_profit_by_limit(quote_df, self.direction,0.5,0.1,3)
    asserted_sr = metric_df.iloc[0]
    # Assert
    self.logger.info(f"Metric DF:\n{metric_df}")
    self.logger.info(f"Expected SR:\n{expected_sr}")
    self.logger.info(f"Asserted SR:\n{asserted_sr}")
    
    self.assertTrue(expected_sr.equals(asserted_sr))  
  
  @parameterized.expand([
        [11],
        [15]
    ])
  def test_WHEN_first_reach_loss_limit_THEN_exit_3(self, loss_value):
    # Array
    # 2-nd candle reach loss
    # no reach income limit
    quote_df = pd.DataFrame({OPEN:[10,12,13], LOW:[10,9,10], HIGH:[10,loss_value,14], CLOSE:[10,12,13]}, index=[1,2,3])
    expected_sr = pd.Series({
      opcn.PROFIT:-0.1,
      opcn.CLOSE_PRICE:11, 
      opcn.SHIFT_TO_CLOSE:1,
      opcn.IDX_OF_CLOSE:2, 
      opcn.TYPE_OF_CLOSE: ClosingType.OnLossLimit
      }, name=1)
        
    # Act
    metric_df = get_profit_by_limit(quote_df, self.direction,0.5,0.1,3)
    asserted_sr = metric_df.iloc[0]
    # Assert
    self.logger.info(f"Metric DF:\n{metric_df}")
    self.logger.info(f"Expected SR:\n{expected_sr}")
    self.logger.info(f"Asserted SR:\n{asserted_sr}")
    
    self.assertTrue(expected_sr.equals(asserted_sr))  
  
  @parameterized.expand([
        [5],
        [1]
    ])
  def test_WHEN_first_reach_income_limit_THEN_exit_1(self, income_value):
    # Array
    # 1-st candle reach income
    # last candle reach loss limit
    quote_df = pd.DataFrame({OPEN:[10,12,13], LOW:[income_value,11,9], HIGH:[10,10,11], CLOSE:[10,12,13]}, index=[1,2,3])
    expected_sr = pd.Series({
      opcn.PROFIT:0.5,
      opcn.CLOSE_PRICE:5, 
      opcn.SHIFT_TO_CLOSE:0,
      opcn.IDX_OF_CLOSE:1, 
      opcn.TYPE_OF_CLOSE: ClosingType.OnIncomeLimit
      }, name=1)
        
    # Act
    metric_df = get_profit_by_limit(quote_df, self.direction,0.5,0.1,3)
    asserted_sr = metric_df.iloc[0]
    # Assert
    self.logger.info(f"Metric DF:\n{metric_df}")
    self.logger.info(f"Expected SR:\n{expected_sr}")
    self.logger.info(f"Asserted SR:\n{asserted_sr}")
    
    self.assertTrue(expected_sr.equals(asserted_sr))
  
  @parameterized.expand([
        [5],
        [1]
    ])
  def test_WHEN_first_reach_income_limit_THEN_exit_2(self, income_value):
    # Array
    # 2-nd candle reach income
    # last candle reach loss limit
    quote_df = pd.DataFrame({OPEN:[10,12,13], LOW:[10,income_value,9], HIGH:[10,10,15], CLOSE:[10,12,13]}, index=[1,2,3])
    expected_sr = pd.Series({
      opcn.PROFIT:0.5,
      opcn.CLOSE_PRICE:5, 
      opcn.SHIFT_TO_CLOSE:1,
      opcn.IDX_OF_CLOSE:2, 
      opcn.TYPE_OF_CLOSE: ClosingType.OnIncomeLimit
      }, name=1)
        
    # Act
    metric_df = get_profit_by_limit(quote_df, self.direction,0.5,0.1,3)
    asserted_sr = metric_df.iloc[0]
    # Assert
    self.logger.info(f"Metric DF:\n{metric_df}")
    self.logger.info(f"Expected SR:\n{expected_sr}")
    self.logger.info(f"Asserted SR:\n{asserted_sr}")
    
    self.assertTrue(expected_sr.equals(asserted_sr))  
  
  @parameterized.expand([
        [5],
        [1]
    ])
  def test_WHEN_first_reach_income_limit_THEN_exit_3(self, income_value):
    # Array
    # 2-nd candle reach income
    # no reach loss limit
    quote_df = pd.DataFrame({OPEN:[10,12,13], LOW:[10,income_value,10], HIGH:[10,10,10], CLOSE:[10,12,13]}, index=[1,2,3])
    expected_sr = pd.Series({
      opcn.PROFIT:0.5,
      opcn.CLOSE_PRICE:5, 
      opcn.SHIFT_TO_CLOSE:1,
      opcn.IDX_OF_CLOSE:2, 
      opcn.TYPE_OF_CLOSE: ClosingType.OnIncomeLimit
      }, name=1)
        
    # Act
    metric_df = get_profit_by_limit(quote_df, self.direction,0.5,0.1,3)
    asserted_sr = metric_df.iloc[0]
    # Assert
    self.logger.info(f"Metric DF:\n{metric_df}")
    self.logger.info(f"Expected SR:\n{expected_sr}")
    self.logger.info(f"Asserted SR:\n{asserted_sr}")
    
    self.assertTrue(expected_sr.equals(asserted_sr))  
  
  @parameterized.expand([
        [5, 11],
        [1, 19],
        [5, 19],
        [1, 11],
    ])  
  def test_WHEN_both_limits_has_been_reach_at_same_candle_THEN_exit_1(self, income_value, loss_value):
    # Array
    # 1-st candle reach
    quote_df = pd.DataFrame({OPEN:[10,12,13], LOW:[income_value,11,9], HIGH:[loss_value,13,15], CLOSE:[10,12,13]}, index=[1,2,3])
    expected_sr = pd.Series({
      opcn.PROFIT:-0.1,
      opcn.CLOSE_PRICE:11, 
      opcn.SHIFT_TO_CLOSE:0,
      opcn.IDX_OF_CLOSE:1, 
      opcn.TYPE_OF_CLOSE: ClosingType.OnLossLimit
      }, name=1)
        
    # Act
    metric_df = get_profit_by_limit(quote_df, self.direction,0.5,0.1,3)
    asserted_sr = metric_df.iloc[0]
    # Assert
    self.logger.info(f"Metric DF:\n{metric_df}")
    self.logger.info(f"Expected SR:\n{expected_sr}")
    self.logger.info(f"Asserted SR:\n{asserted_sr}")
    
    self.assertTrue(expected_sr.equals(asserted_sr))  
  
  @parameterized.expand([
        [5, 11],
        [1, 19],
        [5, 19],
        [1, 11],
    ])  
  def test_WHEN_both_limits_has_been_reach_at_same_candle_THEN_exit_2(self, income_value, loss_value):
    # Array
    # last candle reach
    quote_df = pd.DataFrame({OPEN:[10,12,13], LOW:[10,11,income_value], HIGH:[10,10,loss_value], CLOSE:[10,12,13]}, index=[1,2,3])
    expected_sr = pd.Series({
      opcn.PROFIT:-0.1,
      opcn.CLOSE_PRICE:11, 
      opcn.SHIFT_TO_CLOSE:2,
      opcn.IDX_OF_CLOSE:3, 
      opcn.TYPE_OF_CLOSE: ClosingType.OnLossLimit
      }, name=1)
        
    # Act
    metric_df = get_profit_by_limit(quote_df, self.direction,0.5,0.1,3)
    asserted_sr = metric_df.iloc[0]
    # Assert
    self.logger.info(f"Metric DF:\n{metric_df}")
    self.logger.info(f"Expected SR:\n{expected_sr}")
    self.logger.info(f"Asserted SR:\n{asserted_sr}")
    
    self.assertTrue(expected_sr.equals(asserted_sr))  
  
  def test_WHEN_does_not_reach_limit_THEN_exit(self):
    # Array
    quote_df = pd.DataFrame({OPEN:[10,12,13], LOW:[10,11,10], HIGH:[10,10,10], CLOSE:[10,12,13]}, index=[1,2,3])
    expected_sr = pd.Series({
      opcn.PROFIT:(10-13)/10,
      opcn.CLOSE_PRICE:13, 
      opcn.SHIFT_TO_CLOSE:2,
      opcn.IDX_OF_CLOSE:3, 
      opcn.TYPE_OF_CLOSE: ClosingType.OnClose
      }, name=1)
        
    # Act
    metric_df = get_profit_by_limit(quote_df, self.direction,0.5,0.1,3)
    asserted_sr = metric_df.iloc[0]
    # Assert
    self.logger.info(f"Metric DF:\n{metric_df}")
    self.logger.info(f"Expected SR:\n{expected_sr}")
    self.logger.info(f"Asserted SR:\n{asserted_sr}")
    
    self.assertTrue(expected_sr.equals(asserted_sr))  
    