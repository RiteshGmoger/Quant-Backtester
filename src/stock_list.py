# nse tickers for use with yfinance (all with .NS)
# import whichever list you need in run_backtest.py


NIFTY50 = [
    "RELIANCE.NS",
    "TCS.NS",
    "HDFCBANK.NS",
    "INFY.NS",
    "ICICIBANK.NS",
    "HINDUNILVR.NS",
    "ITC.NS",
    "SBIN.NS",
    "BHARTIARTL.NS",
    "KOTAKBANK.NS",
    "LT.NS",
    "AXISBANK.NS",
    "ASIANPAINT.NS",
    "MARUTI.NS",
    "TITAN.NS",
    "SUNPHARMA.NS",
    "ULTRACEMCO.NS",
    "BAJFINANCE.NS",
    "NESTLEIND.NS",
    "WIPRO.NS",
    "HCLTECH.NS",
    "POWERGRID.NS",
    "NTPC.NS",
    "ONGC.NS",
    "JSWSTEEL.NS",
    "TATASTEEL.NS",
    "ADANIENT.NS",
    "ADANIPORTS.NS",
    "COALINDIA.NS",
    "DIVISLAB.NS",
    "DRREDDY.NS",
    "EICHERMOT.NS",
    "GRASIM.NS",
    "HEROMOTOCO.NS",
    "HINDALCO.NS",
    "INDUSINDBK.NS",
    "M&M.NS",
    "BAJAJFINSV.NS",
    "BPCL.NS",
    "BRITANNIA.NS",
    "CIPLA.NS",
    "TECHM.NS",
    "APOLLOHOSP.NS",
    "BAJAJ-AUTO.NS",
    "TRENT.NS",
    "SHRIRAMFIN.NS",
    "BEL.NS",
    "SBILIFE.NS",
    "HDFCLIFE.NS",
]


NIFTY_NEXT50 = [
    "ADANIGREEN.NS",
    "ADANITRANS.NS",
    "AMBUJACEM.NS",
    "AUROPHARMA.NS",
    "BANDHANBNK.NS",
    "BANKBARODA.NS",
    "BERGEPAINT.NS",
    "BIOCON.NS",
    "BOSCHLTD.NS",
    "CANBK.NS",
    "CHOLAFIN.NS",
    "COLPAL.NS",
    "CONCOR.NS",
    "DABUR.NS",
    "DLF.NS",
    "FEDERALBNK.NS",
    "GAIL.NS",
    "GODREJCP.NS",
    "GODREJPROP.NS",
    "HAVELLS.NS",
    "ICICIPRULI.NS",
    "IDEA.NS",
    "IDFCFIRSTB.NS",
    "IGL.NS",
    "INDUSTOWER.NS",
    "IRCTC.NS",
    "JINDALSTEL.NS",
    "LUPIN.NS",
    "MCDOWELL-N.NS",
    "MPHASIS.NS",
    "MUTHOOTFIN.NS",
    "NAUKRI.NS",
    "NMDC.NS",
    "OBEROIRLTY.NS",
    "OFSS.NS",
    "PAGEIND.NS",
    "PERSISTENT.NS",
    "PETRONET.NS",
    "PFC.NS",
    "PIIND.NS",
    "PIDILITIND.NS",
    "PNB.NS",
    "RECLTD.NS",
    "SAIL.NS",
    "SIEMENS.NS",
    "SRF.NS",
    "TORNTPHARM.NS",
    "UBL.NS",
    "VOLTAS.NS",
    "ZOMATO.NS",
]


NIFTY_BANK = [
    "HDFCBANK.NS",
    "ICICIBANK.NS",
    "KOTAKBANK.NS",
    "SBIN.NS",
    "AXISBANK.NS",
    "INDUSINDBK.NS",
    "BANDHANBNK.NS",
    "FEDERALBNK.NS",
    "IDFCFIRSTB.NS",
    "PNB.NS",
    "BANKBARODA.NS",
    "CANBK.NS",
]


NIFTY_IT = [
    "TCS.NS",
    "INFY.NS",
    "WIPRO.NS",
    "HCLTECH.NS",
    "TECHM.NS",
    "MPHASIS.NS",
    "PERSISTENT.NS",
    "OFSS.NS",
    "COFORGE.NS",
    "LTIM.NS",
]


NIFTY_PHARMA = [
    "SUNPHARMA.NS",
    "DRREDDY.NS",
    "CIPLA.NS",
    "DIVISLAB.NS",
    "AUROPHARMA.NS",
    "LUPIN.NS",
    "BIOCON.NS",
    "TORNTPHARM.NS",
    "ALKEM.NS",
    "IPCALAB.NS",
]


ALL = list(dict.fromkeys(NIFTY50 + NIFTY_NEXT50 + NIFTY_BANK + NIFTY_IT + NIFTY_PHARMA))


if __name__ == "__main__":
    print(f"nifty50     : {len(NIFTY50)} tickers")
    print(f"nifty next50: {len(NIFTY_NEXT50)} tickers")
    print(f"nifty bank  : {len(NIFTY_BANK)} tickers")
    print(f"nifty it    : {len(NIFTY_IT)} tickers")
    print(f"nifty pharma: {len(NIFTY_PHARMA)} tickers")
    print(f"all combined: {len(ALL)} tickers")
