import httpx
from dotenv import load_dotenv
import os
import json

load_dotenv()
API_KEY=os.getenv('COINGECKO_API_KEY')

def fetch_crypto() -> str:
    params = {'vs_currency':'usd',
              'order':'market_cap_desc',
              'per_page':10,
              'page':1}
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    r = httpx.get(url=url, params=params)
    return r.json()

def main():
    print(json.dumps(fetch_crypto(), indent=4))

if __name__ == '__main__':
    main()