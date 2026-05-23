import numpy as np
import pandas as pd
from src.data_loader import get_price_data
from src.backtester import Backtester
from src.metrics import sharpe, win_rate, max_drawdown, calmar_ratio, sortino_ratio

def run():
	prices = get_price_data(['RELIANCE.NS', 'TCS.NS', 'INFY.NS'],start = '2023-01-01',end = '2024-12-31');
	
	if prices is None:
		print(f"No prices returned");
		return 0;
		
	signals = pd.Series(0,index = prices.index);
	ma20 = prices["RELIANCE.NS"].rolling(20).mean();
	signals[prices["RELIANCE.NS"] > ma20] = 1;
	
	reliance_price = pd.DataFrame({"Open" : prices["RELIANCE.NS"],"Close" : prices["RELIANCE.NS"]});
	
	bt = Backtester(reliance_price,signals,holding_days = 40);
	bt.run();
	
	print(bt.results());


if __name__ == "__main__":
	run();
