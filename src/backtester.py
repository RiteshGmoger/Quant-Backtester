import numpy as np;

class Backtester:
    def __init__(self, prices, signals, holding_days = 40, initial_capital = 10000):
        self.prices = prices;
        self.signals = signals;
        self.holding_days = holding_days;
        self.capital = initial_capital;
        
    def run(self):
        self.trades = [];
        self.equity_curves = [self.capital];
        cap = self.capital;

        dates = self.signals.index.tolist();
        in_trade_until = -1; # track when current trade ends

        for i, date in enumerate(dates):
            # skip if signal is not 1
            if self.signals.iloc[i] != 1:
                continue;

            # without this, the strategy piles up hundreds of overlapping trades
            # and the equity curve blows up to unrealistic values
            if i <= in_trade_until:
                continue;

            start_index = i + 1;
            end_index   = i + 1 + self.holding_days;

            if end_index >= len(dates):
                break;

            start_date = dates[start_index];
            end_date = dates[end_index];

            start_price = self.prices.loc[start_date,'Open'];
            end_price = self.prices.loc[end_date,'Open'];

            # transaction costs: 0.09% round trip (buy side + sell side)
            start_price = start_price * (1 + 0.0009);
            end_price = end_price   * (1 - 0.0009);

            returns = (end_price - start_price) / start_price;
            self.trades.append(returns);

            cap = cap * (1 + returns);
            self.equity_curves.append(cap);

            # mark trade as active until end_index
            in_trade_until = end_index;
            
    def results(self):
        from src.metrics import sharpe, max_drawdown, win_rate, calmar_ratio, sortino_ratio;

        if len(self.trades) == 0:
            return {};

        periods_per_year = 252 / self.holding_days;
        annual_return = np.mean(self.trades) * periods_per_year;

        return {
            'Sharpe'        : sharpe(self.trades, periods_per_year = periods_per_year),
            'Sortino'       : sortino_ratio(self.trades, periods_per_year = periods_per_year),
            'Win Rate'      : win_rate(self.trades),
            'Max Drawdown'  : max_drawdown(self.equity_curves),
            'Calmar Ratio'  : calmar_ratio(annual_return, max_drawdown(self.equity_curves)),
            'Total Trades'  : len(self.trades),
            'Initial Cap'   : round(self.capital),
            'Final Cap'     : round(self.equity_curves[-1], 2)
        };
