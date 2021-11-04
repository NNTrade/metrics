import unittest
import logging
import pandas as pd
from src.misc.counter import Counter
import numpy as np


class CounterTestCase(unittest.TestCase):
    def test_counter__check(self):
        
        class asserter:
            def __init__(self, test_self) -> None:
                self.perc_range = np.arange(0, 101, 0.01)
                self.i = 1
                self.test_self = test_self
                pass
            def assert_var(self,perc):
                self.test_self.assertEqual(round(self.perc_range[self.i],2), perc)
                self.i=self.i+1


        range_list = range(20000)
        _asserter = asserter(self)
        counter = Counter(len(range_list),_asserter.assert_var)
        for i in range_list:
            counter.next()
