from enum import Enum

class ClosingType(Enum):
  OnClose = 0
  OnIncomeLimit = 1
  OnLossLimit = -1