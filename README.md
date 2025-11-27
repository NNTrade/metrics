# Init steps
1. ```python -m venv .venv```
2. [Activate venv](https://docs.python.org/3/library/venv.html#how-venvs-work)
    - Windows Powershell: ```.venv\Scripts\activate.ps1```
    - Linux bash: ```source .venv/bin/activate```
3. ```pip install -r requirements.txt && pip install -r requirements.dev.txt```

# Metrics for trading
Framework with metrics for trading robots
- [Glossary](./docs/Glossary.md)

## Import to pip

```
NNTrade.metric @ git+https://git@github.com/NNTrade/metrics.git#egg=NNTrade.metric
```

## List of metrics
- [Future Extrem deviation](./docs/metrics/future_extrem_deviation.md)
- [Future profit by limit](./docs/metrics/future_profit_by_limits.md)
