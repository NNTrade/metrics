# Future extrem deviation
Return max extream reached in future N candles

## Input
1. Period - amount of candles where searchs extremum
2. Extrem type - type of extremum that searchs 
3. Limit - deviation level, the achievement of which stops the searching

## Rules
1. Limits calculate as (end calue - open)/open

## Using
```python
from NNTrade.source.market.quotes import QuoteSource, date
...
qs = QuoteSource(fcq, qsc)
quote_df = qs.get("EURUSD",TimeFrame.m1, from_date=date(2010,1,1), untill_date=date(2011,1,1))

from NNTrade.metric.future_extrem_deviation import get_extrem_rel_of, ExtreamType, get_extrem_rel_matrix_of

ext_rel = get_extrem_rel_of(quote_df, 3, ExtreamType.High)

matrix_df = get_extrem_rel_matrix_of(quote_df, [4,8,12,16,40])
```