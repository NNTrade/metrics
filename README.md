# Metrics for trading

Framework with metrics for trading robots

## Import to pip

```
NNTrade.metric @ git+https://git@github.com/NNTrade/metrics.git#egg=NNTrade.metric
```

## List of metrics
### Future Extrem Percent
Return max or min deviation from current open price in next N candles.

```python
from NNTrade.source.market.quotes import QuoteSource, date
...
qs = QuoteSource(fcq, qsc)
quote_df = qs.get("EURUSD",TimeFrame.m1, from_date=date(2010,1,1), untill_date=date(2011,1,1))

from NNTrade.metric.future_extrem_deviation import get_extrem_rel_of, ExtreamType, get_extrem_rel_matrix_of

ext_rel = get_extrem_rel_of(quote_df, 3, ExtreamType.High)

matrix_df = get_extrem_rel_matrix_of(quote_df, [4,8,12,16,40])
```
