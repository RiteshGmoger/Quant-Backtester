"""
    data_loader.py

    handles all price data downloading for the backtester
    right now just yfinance, might add more sources later

    everything here is pure data - no indicators, no signals
    just get the prices and return them clean
"""

import logging
import sys
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

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

    # let people pass a single string, not just a list
    if isinstance(tickers, str):
        tickers = [tickers]

    logger.info("─"*71)
    logger.info("│" + "DOWNLOADING PRICE DATA".center(69) + "│")
    logger.info("─"*71)
    logger.info("│" + ("Tickers".center(35) + ":" + "%d".center(34) % len(tickers)) + "│")
    logger.info("│" + ("From".center(35) + ":" + "%s".center(25) % start) + "│")
    logger.info("│" + ("To".center(35) + ":" + "%s".center(25) % end) + "│")
    logger.info("─"*71)

    try:
        raw = yf.download(
            tickers,
            start=start,
            end=end,
            progress=False,
            auto_adjust=True
        )

        if raw.empty:
            logger.warning("no data returned — check tickers and date range")
            return None

        # yf.download returns MultiIndex columns when multiple tickers
        # we only need Close prices
        if isinstance(raw.columns, pd.MultiIndex):
            df = raw["Close"]
        else:
            # single ticker comes back as flat columns(when passed single ticker)
            df = raw[["Close"]]
            df.columns = tickers

        df = df.dropna(how="all")
        """
            WHY dropna(how="all") and NOT dropna()

            Example data:
            Date        RELIANCE   TCS   INFY
            Day1         100       200    300
            Day2         NaN       210    310
            Day3         105       NaN    315
            Day4         NaN       NaN    NaN

            Using dropna() (default: how="any"):
                removes Day2, Day3, Day4

            Result:
            Date        RELIANCE   TCS   INFY
            Day1         100       200    300

            PROBLEM:
            Valid data (TCS, INFY) got deleted just because one stock was NaN.
            This destroys data in multi-stock systems.

            Using dropna(how="all"):
                removes only Day4

            Result:
            Date        RELIANCE   TCS   INFY
            Day1         100       200    300
            Day2         NaN       210    310
            Day3         105       NaN    315

            We preserve time continuity even if some stocks are missing.
        """

        logger.info("│" + ("got %d rows, %d tickers" % (len(df), len(df.columns))).center(69) + "│")
        logger.info("─"*71 + "\n")

        return df

    except Exception as e:
        logger.error("download failed: %s", e)
        return None


if __name__ == "__main__":
    # quick test - download reliance for 2024 and print first 5 rows
    df = get_price_data("RELIANCE.NS", start="2024-01-01", end="2024-12-31")

    if df is not None:
        print(df.head())
