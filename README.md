# quant backtester

a momentum backtester for nse stocks, written from scratch in python. no backtrader, no vectorbt, no library doing the hard part for me. yfinance for data, pandas for the frames, everything else is mine.

built this because i wanted to actually understand what a backtest does instead of trusting a library's output.

## the strategy

dead simple on purpose:

- universe: the `NIFTY50` list in `src/stock_list.py` (49 tickers, one short of 50)
- signal: close price above the 20 day moving average
- entry: **next day's open**, never the same close
- hold: 40 trading days
- exit: open price after the hold
- costs: 0.09% on entry and 0.09% on exit
- one trade at a time, no overlapping positions

the "next day's open" bit is the whole point. if you enter at the same close that fired the signal, you needed tomorrow's information today. that is not a strategy, that is time travel. it is also the single most common way people fool themselves with a backtest.

the no-overlap rule matters too. without it the engine stacked hundreds of simultaneous trades on the same capital and the equity curve went to the moon. it looked amazing. it was fake.

## results

reliance.ns, jan 2023 to dec 2024, 40 day hold:

| metric | value |
|--------|------:|
| sharpe | 0.61 |
| sortino | 1.48 |
| max drawdown | -10.7% |
| calmar | 1.72 |
| win rate | 55.6% |
| starting capital | 10,000 |
| ending capital | 12,521 |

so roughly +25% over two years after costs. not a money printer. sharpe under 1 means the returns are not paying you much for the volatility you sat through. i am reporting it as it is instead of tuning parameters until the numbers looked good, because tuning until it looks good is how you build a strategy that only works on the past.

sortino being more than 2x sharpe is the interesting part. downside moves were smaller than upside moves, which is what you want from a momentum system.

## running it

```bash
conda activate quant
```

```bash
pip install -r requirements.txt
```

```bash
python run_backtest.py
```

what happens: downloads the nifty 50 price data, runs the ma20 signal on reliance, prints the metrics table, then opens three charts one at a time (equity curve, drawdown, trade returns). close each window to get the next one. all three also save to `results/charts/`.

if you are on a headless box the `plt.show()` calls will just no-op, the pngs still get written.

to change the ticker or dates, edit the constants at the top of [run_backtest.py](run_backtest.py):

```python
TICKER = "RELIANCE.NS"
START = "2023-01-01"
END = "2024-12-31"
HOLDING_DAYS = 40
```

## what's in here

```text
run_backtest.py          the entry point, wires everything together
src/
  backtester.py          the engine - trade loop, entry timing, no-overlap rule
  metrics.py             sharpe, sortino, max drawdown, calmar, win rate
  walk_forward.py        rolling train/test window splitter
  visualizer.py          the three charts
  data_loader.py         yfinance wrapper with logging that doesn't spam
  stock_list.py          nifty50, next50, bank, it, pharma - 103 tickers total
results/charts/          pngs land here
tests/                   scratch scripts i used while building each piece
```

## the metrics, in plain words

| metric | what it actually tells you |
|--------|---------------------------|
| sharpe | return per unit of total wobble. above 1 is decent, above 2 is genuinely good |
| sortino | same but it only counts the downside wobble. fairer to strategies that spike up |
| max drawdown | worst peak to trough fall. the number that decides whether you'd have quit |
| calmar | annual return divided by max drawdown. return per unit of pain |
| win rate | how many trades closed green. means nothing without knowing win size vs loss size |

win rate is the one everybody quotes and it is the least useful. you can win 80% of the time and still lose money if the 20% are big enough.

## walk forward

`walk_forward.py` splits the timeline into rolling windows:

```text
[---- 12mo train ----][-- 3mo test --]
                      [---- 12mo train ----][-- 3mo test --]
                                            [---- 12mo train ----][-- 3mo test --]
```

each test window is data the previous window never touched, and the whole thing rolls forward 3 months at a time.

being honest about the current state: the splitting and the rolling out of sample evaluation work. the train window is not yet used to fit parameters, so right now it is out of sample testing rather than full walk forward optimisation. the structure is there for it, the fitting step is the next thing i am building. `run_backtest.py` calls the single backtest path, not this one.

## what i'd fix next

- fit the ma window inside the train period instead of hardcoding 20
- run the backtest across the whole universe rather than one ticker at a time
- position sizing, right now every trade is all the capital
- a proper test suite, the stuff in `tests/` is scratch work not real tests

## stack

python, pandas, numpy, matplotlib, yfinance

built by ritesh g moger
