import yfinance as yf
from typing import List
from pandas.core.frame import DataFrame

# There is no reason to make a seperate file for the way it is used right now
# This is just for future proofing

def fetch_stock_data(tickers: List[str], *args, **kwargs):
    """Fetch stock data by tickers

    Args:
        tickers (List[str]): The tickers for the list of stocks to have data retrieved from
        *args, **kwargs: functions to be fed to the internal yf.download method 
    """
    all_stock_data: List[str] = [fetch_one_stock(ticker, args, kwargs) for ticker in tickers]
    return "\n".join(all_stock_data)
    
def fetch_one_stock(ticker: str, *args, **kwargs):
    """Fetching stock data of a single stock by it's tickers

    Args:
        ticker (str): Ticker for stock 
    """
    try:
        stock: DataFrame = yf.download(ticker, *args, **kwargs)
    except Exception as e:
        raise ValueError(f"Cannot fetch data for ticker: {ticker}, exception: {e}")
    stock_description: str = f"Stock data for {ticker} \n"
    stock_text: str = stock.to_markdown()
    return stock_description + stock_text
    
    