import pandas as pd
from src.data_loader import get_price_data
from src.backtester import Backtester
from src.visualizer import plot_equity_curve, plot_drawdown, plot_returns
from src.stock_list import NIFTY50

TICKER = "RELIANCE.NS"
START = "2023-01-01"
END = "2024-12-31"
HOLDING_DAYS = 40

def run():
	prices = get_price_data(NIFTY50, start = START, end = END);
	
	if prices is None:
		print(f"No prices returned");
		return;
		
	close = prices["close"];
	open_ = prices["open"];

	ma20 = close[TICKER].rolling(20).mean();
	signals = pd.Series(0, index = close.index);
	signals[close[TICKER] > ma20] = 1;
	
	reliance_price = pd.DataFrame({"Open": open_[TICKER],"Close": close[TICKER]});
	
	bt = Backtester(reliance_price, signals, holding_days = HOLDING_DAYS);
	bt.run();
	results = bt.results();

	print("\n" + "─" * 50);
	print("BACKTEST RESULTS".center(50));
	print("─" * 50);

	for key, val in results.items():
		print(f"{key : ^25}:{val : ^25}");

	print("─" * 50);
	print(f"  ticker : {TICKER}");
	print(f"  period : {START}  ->  {END}");
	print(f"  hold   : {HOLDING_DAYS} trading days");
	print("─" * 50);

	plot_equity_curve(bt.equity_curves);
	plot_drawdown(bt.equity_curves);
	plot_returns([r * 100 for r in bt.trades]);

	print("Charts saved to results/charts/");


if __name__ == "__main__":
	run();
