# Walk-forward Backtested Momentum Strategy — NSE Equities

Quantitative momentum strategy with walk-forward validation, built from scratch in Python
Runs on real NSE price data via `yfinance` and outputs metrics and charts.

---

## What this does

Most backtests are broken. They optimize on historical data, measure on the same data, and call it a strategy. That is not a backtest. That is memorization.

This project is structured for **walk-forward validation**: split the data into windows, work on one period, test on the next period the strategy has not touched, roll forward, repeat. That is the validation style used in serious systematic research.

**Signal logic:**
- universe: Nifty 50 stocks (`src/stock_list.py`; current list contains 49 tickers)
- signal: price is above the 20-day moving average
- entry: next-day open after the signal fires, never same-day close — this avoids look-ahead bias
- hold period: 40 trading days
- exit: open price after the holding period
- transaction costs: 0.09% round-trip (brokerage + slippage, both sides)
- concurrent trades: one at a time, no capital overlap

---

## Results

> Numbers below were produced by running the current code on the selected stock and date range.

| metric | value |
|--------|-------:|
| Sharpe ratio | 0.6118393055617044 |
| Sortino ratio | 1.4770448305896549 |
| Max drawdown | -0.10662040724015613 |
| Calmar ratio | 1.7231081759769789 |
| Win rate | 0.5555555555555556 |
| Initial capital | 10000.00 |
| Final capital | 12521.28 |

~12% CAGR-ish before realistic taxes

---

## Project structure

```text
quant-backtester/
├── run_backtest.py          runs the whole backtest
├── src/
│   ├── backtester.py        core engine - entry logic, trade loop, overlap rule
│   ├── metrics.py           Sharpe, Sortino, max drawdown, Calmar, win rate
│   ├── walk_forward.py      rolling train/test windows
│   ├── Visualizer.py        equity curve, drawdown chart, returns bar chart
│   ├── data_loader.py       yfinance wrapper with clean logging
│   └── stock_list.py        Nifty 50 + Nifty Next 50 tickers
├── results/
│   └── charts/              equity.png, drawdown.png, returns.png
├── tests/
├── requirements.txt
└── README.md
```

---

## How to run

```bash
# 1. activate environment
conda activate quant

# 2. install dependencies
pip install -r requirements.txt

# 3. run
python run_backtest.py
```

What happens when you run it:
- downloads price data for the configured tickers
- runs the backtest with the MA20 signal on the selected stock
- prints the results table in the terminal
- opens the equity curve, then the drawdown chart, then the returns chart
- saves all three charts to `results/charts/`

---

## Metrics explained

| metric | what it means |
|--------|---------------|
| Sharpe ratio | excess return per unit of total volatility. Above 1.0 is decent, above 2.0 is strong |
| Sortino ratio | like Sharpe but only counts downside volatility. Better for asymmetric strategies |
| Max drawdown | worst peak-to-trough loss in the period. The number you lose sleep over |
| Calmar ratio | annualized return divided by max drawdown. Return per unit of drawdown risk |
| Win rate | percentage of trades that closed green. 55%+ with decent payoff ratio is solid |

---

## Why no look-ahead bias

Signal fires on **close of day i**.
Entry happens at **open of day i+1**.

If you enter at the same close that generated the signal, you would need to know the close before the market closes. That is impossible in live trading. Next-day open is the implementable entry.

---

## Walk-forward methodology

```text
[──── 12 months train ────][── 3 months test ──]
                           [──── 12 months train ────][── 3 months test ──]
                                                      [──── 12 months train ────][── 3 months test ──]
```

Parameters are not fitted inside the test window. The current engine is structured for walk-forward evaluation, and the train window is reserved for future parameter fitting and selection.

Current behavior:
- the engine rolls forward through time
- each test window is evaluated on unseen data
- the code is set up for future optimization logic inside the training window

---

## Implementation notes

- The current signal in `run_backtest.py` is **price above the 20-day moving average**, not a strict crossover event.
- The current `walk_forward.py` performs rolling out-of-sample testing; it does not yet fit or optimize parameters inside the train window.
- The current ticker list under `NIFTY50` contains 49 tickers in code.

---

## Dependencies

```text
yfinance
pandas
numpy
matplotlib
python-dateutil
```

---

Built by Ritesh G Moger
