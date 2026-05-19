from dateutil.relativedelta import relativedelta
from src.backtester import Backtester
import pandas as pd

class WalkForwardEngine:
    def __init__(self, prices_df, signals_df,
                 train_months=12, test_months=3):
        self.prices = prices_df
        self.signals = signals_df
        self.train_months = train_months
        self.test_months = test_months
        
    
    def run(self):
        results = []
        dates = self.prices.index
        start = dates[0]
        end = dates[-1]

        window_start = start
        window_num = 0

        while True:
            train_end = window_start + relativedelta(months=self.train_months)
            test_end = train_end + relativedelta(months=self.test_months)

            if test_end > end:
                break

            test_prices = self.prices[
                (self.prices.index >= train_end) &
                (self.prices.index < test_end)
            ]
            test_signals = self.signals[
                (self.signals.index >= train_end) &
                (self.signals.index < test_end)
            ]

            if len(test_prices) < 10:
                break

            bt = Backtester(test_prices, test_signals)
            bt.run()
            window_results = bt.results()

            window_results['window'] = window_num
            window_results['test_start'] = str(train_end.date())
            window_results['test_end'] = str(test_end.date())
            results.append(window_results)

            window_start += relativedelta(months=self.test_months)
            window_num += 1

        return pd.DataFrame(results)
