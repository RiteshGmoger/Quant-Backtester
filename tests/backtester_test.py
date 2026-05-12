import numpy as np

class Backtester:
    def __init__(self, prices, signals, holding_days = 40, initial_capital = 10000):
        self.prices = prices;
        self.signals = signals;
        self.holding_days = holding_days;
        self.capital = initial_capital;
        
        
    def run(self):
        self.trades = [];
        self.equity_curves = [self.capital];
        cap =  self.capital;
        
        dates = self.signals.index.tolist();
        for i, date in enumerate(dates):
            if(self.signals.iloc[i] != 1):
                continue;
            
            start_index = i + 1;
            end_index = i + 1 + self.holding_days;
            
            if(end_index >= len(dates)):
                break;
            
            start_date = dates[start_index];
            end_date = dates[end_index];
            
            start_price = self.prices.loc[start_date, 'Open'];
            end_price = self.prices.loc[end_date, 'Open'];
            
            start_price =  start_price * (1 + 0.0009);
            end_price = end_price * (1 - 0.0009);
            
            returns = (end_price - start_price) / start_price;
            self.trades.append(returns);
            
            cap = cap * (1 + returns);
            self.equity_curves.append(cap);
            
    
    def results(self):
        from .metrics import sharpe, max_drawdown, win_rate, calmar_ratio, sortino_ratio
        
        if(len(self.trades) == 0):
            return 0;
            
        return {
               'Sharpe'     :   sharpe(self.trades),
              'Sortino'     :   sortino_ratio(self.trades),
              'Win rate'    :   win_rate(self.trades),
              'Drawdown'    :   max_drawdown(self.equity_curves),
            'Calmar ratio'  :   calmar_ratio(np.mean(self.trades) * 252,max_drawdown(self.equity_curves)),
            'total trades'  :   len(self.trades)
        };
