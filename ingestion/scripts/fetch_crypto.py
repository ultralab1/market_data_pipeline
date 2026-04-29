from typing import Any
import httpx
from dotenv import load_dotenv
import os
import json

from requests import RequestException

load_dotenv()
API_KEY=os.getenv('COINGECKO_API_KEY')

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


def main():
    print(json.dumps(fetch_crypto(), indent=4))

if __name__ == '__main__':
    main()