import yfinance as yf
import pandas as pd
from typing import Any
import httpx
from dotenv import load_dotenv
import os
import json

from requests import RequestException

load_dotenv()
API_KEY=os.getenv('COINGECKO_API_KEY')

def fetch_stocks(tickers: list[str], period, interval) -> dict[str, pd.DataFrame]:
    data = {}
    for ticker in tickers:
        try:
            data[ticker] = yf.Ticker(ticker).history(period=period, interval=interval)
        except (ConnectionError, TimeoutError) as e:
            print('Unable to connect!')
            print(f'Ticker: {ticker}')
            print(f'{e}')
        except Exception as e:
            print(f'Unexpected error for ticker: {ticker} : {e}')
    return data

def fetch_crypto() -> Any | None:
    params = {'vs_currency':'usd',
              'order':'market_cap_desc',
              'per_page':10,
              'page':1}
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    try:
        r = httpx.get(url=url, params=params, timeout=20)
        return r.json()
    except RequestException as e:
        print('Unable to fetch!')
        print(f'{e}')
        return None
    except Exception as e:
        print(f'Unexpected error occurred : {e}')

def main():
    print(json.dumps(fetch_crypto(), indent=4))

if __name__ == '__main__':
    main()