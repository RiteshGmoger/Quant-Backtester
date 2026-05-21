from src.data_loader import get_price_data
from src.backtester import Backtester
from src.metrics import sharpe, max_drawdown, win_rate
import pandas as pd
import numpy as np

def run():
    prices = get_price_data(
        ['RELIANCE.NS', 'TCS.NS', 'INFY.NS'],
        start = '2023-01-01',
        end = '2024-12-31'
    )
    
    if prices is None:
        print("Data load failed")
        return
    
    signals = pd.Series(0, index = prices.index)
    ma20 = prices['RELIANCE.NS'].rolling(20).mean()
    signals[prices['RELIANCE.NS'] > ma20] = 1
    
    reliance_prices = pd.DataFrame({
        'Open': prices['RELIANCE.NS'],
        'Close': prices['RELIANCE.NS']
    })
    
    bt = Backtester(reliance_prices, signals, holding_days=30)
    bt.run()
    results = bt.results()

    print("\n" + "─" * 50)
    print("BACKTEST RESULTS".center(50))
    print("─" * 50)
    for key, val in results.items():
        print(f"{key : ^25}:{val : ^ 25}")


if __name__ == "__main__":
    run()
