# Future [profit][gl_profit] by limits
profit which could be atchived using limit

## Input
1. Time limit - amount of time while we holding position
2. [income][gl_income] limit - amount of [income][gl_income] which is signal for closing
3. [loss][gl_loss] limit - amount of [loss][gl_loss] which we can [loss][gl_loss] by one deal
4. Direction - Long or Short position direction

## Rules
### Open
Open position on open price

### Closing
1. IF [profit][gl_profit] reach **[loss][gl_loss]** limit by [negative extemum][gl_NE]
    1. before [profit][gl_profit] reach [income][gl_income] limit
    2. [profit][gl_profit] doesnot reach [income][gl_income] limit
    THEN exit by limit price
2. IF [profit][gl_profit] reach **[income][gl_income]** limit by [positive extremum][gl_PE] 
    1. before [profit][gl_profit] reach [loss][gl_loss] limit
    2. [profit][gl_profit] doesnot reach [loss][gl_loss] limit
    THEN exit by limit price
3. IF reach period but does not reach any limits 
    THEN exit by close price

## Output
Pandas DataFrame
[Columns](./constant/output_col_name.py):
- Profit
- ClosePrice
- Shift_to_close
- Idx_of_close
- [Type_of_close](./constant/closing_types.py)

[gl_profit]: ../../docs/Glossary.md#profit
[gl_NE]: ../../docs/Glossary.md#negative-extremum-ne
[gl_PE]: ../../docs/Glossary.md#positive-extremum-pe
[gl_loss]: ../../docs/Glossary.md#loss
[gl_income]: ../../docs/Glossary.md#income

## Using
```python
from NNTrade.source.market.quotes import QuoteSource, date
...
qs = QuoteSource(fcq, qsc)
quote_df = qs.get("EURUSD",TimeFrame.m1, from_date=date(2010,1,1), untill_date=date(2011,1,1))

from NNTrade.metric.future_profit_by_limits import get_profit_by_limit, direction

profit_df = get_profit_by_limit(quote_df, direction.Long, 0.5, 0.1, 10)

```