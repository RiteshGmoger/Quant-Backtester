import logging
import sys
import warnings
warnings.filterwarnings("ignore", category = FutureWarning)

import pandas as pd
import yfinance as yf

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s ││   %(levelname)s   ││    %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ]
)
logger = logging.getLogger(__name__)


def get_price_data(tickers, start, end):
    """
        Download OHLCV price data for a list of tickers
        start and end are strings like "2024-01-01"

        returns a DataFrame with Close prices for each ticker
        index is dates, columns are ticker names

        if a single ticker string is passed instead of a list,
        it wraps it in a list automatically

        returns None if download fails or no data comes back
    """
    # keeps tickers always list
    if isinstance(tickers, str):
        tickers = [tickers];
        
    logger.info("─"*71);
    logger.info("│" + "DOWNLOADING PRICE DATA".center(69) + "│");
    logger.info("─"*71);
    logger.info("│" + "Tickers".center(34) + ":" + f"{len(tickers)}".center(34) + "│");
    logger.info("│" + "From".center(34) + ":" + f"{start}".center(34) + "│");
    logger.info("│" + "To".center(34) + ":" + f"{end}".center(34) + "│");
    logger.info("─"*71);
    
    try:
        df = yf.download(tickers,start = start,end = end,progress = False,auto_adjust = True);

        if df.empty:
            logger.warning("no data returned - check tickers and date range");
            return None;
            
        if isinstance(df.columns, pd.MultiIndex):
            open_df  = df['Open']
            close_df = df['Close']
        else:
            open_df  = df[['Open']];
            open_df.columns = tickers;
            close_df = df[['Close']];
            close_df.columns = tickers;
            
        open_df = open_df.dropna(how = "all")
        close_df = close_df.dropna(how = "all")
        """
            WHY dropna(how = "all") and not just dropna()

            Example data:
            Date        RELIANCE   TCS   INFY
            Day1         100       200    300
            Day2         NaN       210    310
            Day3         105       NaN    315
            Day4         NaN       NaN    NaN

            Using dropna() (default: how = "any"):
                removes Day2, Day3, Day4

            Result:
            Date        RELIANCE   TCS   INFY
            Day1         100       200    300

            PROBLEM:
            Valid data (TCS, INFY) got deleted just because one stock was NaN
            This destroys data in multi-stock systems

            Using dropna(how = "all"):
                removes only Day4

            Result:
            Date        RELIANCE   TCS   INFY
            Day1         100       200    300
            Day2         NaN       210    310
            Day3         105       NaN    315

            preserved continuity even if some stocks are missing
        """

        logger.info("│" + ("got %d rows, %d tickers" % (len(close_df), len(close_df.columns))).center(69) + "│");
        logger.info("─"*71 + "\n");

        return {"open": open_df, "close": close_df};

    except Exception as e:
        logger.error("download failed: %s", e);
        return None;


if __name__ == "__main__":
    from src.stock_list import NIFTY50
    df = get_price_data(NIFTY50, start = "2024-01-01", end = "2024-12-31");

    if df is not None:
        print(df["close"].head());
