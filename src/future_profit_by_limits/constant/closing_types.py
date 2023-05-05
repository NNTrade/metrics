from enum import Enum

class ClosingType(Enum):
  OnClose = "OnClose"
  OnIncomeLimit = "OnIncomeLimit"
  OnLossLimit = "OnLossLimit"