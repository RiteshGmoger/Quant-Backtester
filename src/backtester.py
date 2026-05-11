import numpy as np

class Backtester:
    def __init__(self, prices_df, signals_df, hold_days=30, initial_capital=100000):
        self.prices = prices_df;
        self.signals = signals_df;
        self.hold_days = hold_days;
        self.initial_capital = initial_capital;
        # prices_df: DataFrame with Open, Close columns
        # signals_df: 1 = buy signal, 0 = no signal
        # hold_days: how many days to hold each position
        # initial_capital: starting money

    def run(self):
        self.trade_pnls = []
        self.equity_curve = [self.initial_capital]
        capital = self.initial_capital
        
        dates = self.signals.index.tolist()
        
        for i, date in enumerate(dates):
            # check if signal exists on this date
            if self.signals.iloc[i] != 1:
                continue
            
            # entry is next day open (D+1)
            entry_idx = i + 1
            exit_idx = i + 1 + self.hold_days
            
            # make sure we have enough future data
            if exit_idx >= len(dates):
                continue
            
            entry_date = dates[entry_idx]
            exit_date = dates[exit_idx]
            
            # get prices
            entry_price = self.prices.loc[entry_date, 'Open']
            exit_price = self.prices.loc[exit_date, 'Open']
            
            # apply transaction costs
            entry_price = entry_price * (1 + 0.0009)  # pay 0.09% more to buy
            exit_price = exit_price * (1 - 0.0009)    # receive 0.09% less on sell
            
            # calculate return
            trade_return = (exit_price - entry_price) / entry_price
            self.trade_pnls.append(trade_return)
            
            # update equity
            capital = capital * (1 + trade_return)
            self.equity_curve.append(capital)

    def get_results(self):
        from .metrics import sharpe, max_drawdown, win_rate, calmar_ratio, sortino_ratio
        
        if not self.trade_pnls:
            return {}
        
        return {
            'sharpe'        :  sharpe(self.trade_pnls),
            'max_drawdown'  :  max_drawdown(self.equity_curve),
            'win_rate'      :  win_rate(self.trade_pnls),
            'calmar'        :  calmar_ratio(np.mean(self.trade_pnls) * 252,max_drawdown(self.equity_curve)),
            'sortino'       :  sortino_ratio(self.trade_pnls),
            'total_trades'  :  len(self.trade_pnls)
        }
