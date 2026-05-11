import numpy as np

def sharpe(returns,risk_free_annual = 0.04):
	risk_free_per_day = risk_free_annual / 252;
	returns = np.array(returns);
	
	if(len(returns) == 0):
		return 0;
	
	excess = returns - risk_free_per_day;
	std = np.std(excess,ddof = 1);
	
	if(std == 0):
		return 0;
	
	return (np.mean(excess) / std * np.sqrt(252));
	
def drawdown(equity_curves):
	equity_curves = np.array(equity_curves);
	peak = equity_curves[0];
	max_dd = 0;
	
	for val in equity_curves:
		if(val > peak):
			peak = val;
		
		dd = (val - peak) / peak;
		
		if(dd < max_dd):
			max_dd = dd;
	
	return max_dd;
	
def win_rate(trades):
	trades = np.array(trades);
	if(len(trades) == 0):
		return 0;
	
	return (np.sum(trades > 0) / len(trades));
	
def calmar_ratio(annual_return,max_dd):
	if(max_dd == 0):
		return 0;
		
	return annual_return / abs(max_dd);
	
def sortino(returns,risk_free_annual = 0.04):
	returns = np.array(returns);
	risk_free_per_day = risk_free_annual / 252;
	excess = returns - risk_free_per_day;
	
	downside = excess[excess < 0];
	
	if(len(downside) == 0):
		return 0;
		
	downside_std = np.std(downside,ddof = 1);
	if(downside_std == 0):
		return 0;
		
	return (np.mean(excess) / downside_std * np.sqrt(252));
	
	

returns = [0.001, -0.002, 0.003, 0.001, -0.001]
equity = [100, 110, 115, 90, 95, 120]
trades = [100, -50, 200, -30, 150]

print(sharpe(returns))
print(drawdown(equity))
print(win_rate(trades))
print(calmar_ratio(0.15,drawdown(equity)))
print(sortino(returns))
