import numpy as np

def sharpe(returns,risk_free_annual = 0.04):
    risk_free_per_day = risk_free_annual / 252;
    returns = np.array(returns);
    
    excess = returns - risk_free_per_day;
    
    if(np.std(excess,ddof = 1) == 0):
        return 0;
        
    return (np.mean(excess) * np.sqrt(252) /  np.std(excess,ddof = 1));
    
def max_drawdown(equity_curves):
    equity_curves = np.array(equity_curves);
    
    drawdown = 0;
    peak = equity_curves[0];
    
    for val in equity_curves:
        if(val > peak):
            peak = val;
            
        ans = (val - peak) / peak;
        
        if(drawdown > ans):
            drawdown = ans;
        
    return drawdown;
    
def win_rate(trade_pnls):
    trade_pnls = np.array(trade_pnls);
    if(len(trade_pnls) == 0):
        return 0;
    
    return (np.sum(trade_pnls > 0) / len(trade_pnls));
    
def calmar_ratio(returns, equity):
    annual_returns = np.mean(returns) * 252;
    max_dd = max_drawdown(equity);
    
    if(max_dd == 0):
        return 0;
    
    return annual_returns / abs(max_dd);
    
def sortino_ratio(returns, risk_free_annual=0.04):
    returns = np.array(returns)
    risk_free_per_day = risk_free_annual / 252;
    
    excess = returns - risk_free_per_day;
    downside = excess[excess < 0]
    if(len(downside) == 0):
        return 0;
    
    downside_std = np.std(downside,ddof = 1);
    if(downside_std == 0):
        return 0;
    
    return (np.mean(excess) / downside_std * np.sqrt(252));
    
    
returns = [0.001, -0.002, 0.003, 0.001, -0.001]
equity = [100, 110, 115, 90, 95, 120]
trades = [100, -50, 200, -30, 150]

print(f"Sharpe: {sharpe(returns)}");
print(f"Max DD: {max_drawdown(equity)}");
print(f"Win Rate: {win_rate(trades)}");
print(f"calmer ratio: {calmar_ratio(returns,equity)}")
print(f"sortino ratio: {sortino_ratio(returns)}")
