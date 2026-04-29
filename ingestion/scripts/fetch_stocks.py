import yfinance as yf
import pandas as pd

def fetch_stocks(tickers: list[str], period, interval) -> dict[str, pd.DataFrame]:
    data = {}
    for ticker in tickers:
        data[ticker] = yf.Ticker(ticker).history(period=period, interval=interval)
    return data