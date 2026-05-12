import pandas as pd
import numpy as np
from src.backtester import Backtester

# fake price data — 100 days
dates = pd.date_range('2024-01-01', periods = 100, freq = 'B') # store all 100 busssiness days
prices = pd.DataFrame({'Open': np.random.uniform(100, 200, 100),'Close': np.random.uniform(100, 200, 100)}, index = dates)

# fake signals — buy every 10 days
signals = pd.Series(0, index = dates) # make all dates signals 0
signals.iloc[::10] = 1 # every 10th element is 1

bt = Backtester(prices, signals, hold_days = 5)
bt.run()
print(bt.get_results())
