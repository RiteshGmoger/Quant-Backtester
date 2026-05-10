import yfinance as yf
import pandas as pd

def get_prize_data(ticker,start,end):
	df = yf.download(ticker,start = start,end = end)
	
	if df.empty:
		return None
	
	return df['Close']
	
if __name__ == "__main__":
	data = get_prize_data("RELIANCE.NS",start = "2024-01-01",end = "2024-12-31")
	
	if data is not None:
		print(data)
