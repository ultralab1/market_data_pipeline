from ingestion.scripts.fetchers import *
from datetime import datetime
from sqlalchemy import func, true
from sqlmodel import Session, create_engine, select
from sqlalchemy.dialects.postgresql import insert
from dotenv import load_dotenv
import os
import psycopg
from ingestion.scripts.models import StockPrices, CryptoPrices

load_dotenv()
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
DB_NAME = os.getenv('DB_NAME')

url = f'postgresql+psycopg://{USER}:{PASSWORD}@localhost:5433/{DB_NAME}'
engine = create_engine(url=url, echo=False)

def check_stock_duplicates(ticker: str, data: pd.DataFrame, session: Session) -> bool:
    stmt = select(func.max(StockPrices.timestamp)).where(StockPrices.ticker == ticker)
    r = session.exec(stmt).first()
    if r:
        if r == data.index.max().tz_convert(None):
            print('Duplicate data! Skipping ticker')
            return True
    return False

def load_stocks(tickers: list, period, interval) -> None:
    try:
        with Session(engine) as session:
            stock_data = fetch_stocks(tickers=tickers,
                                      period=period,
                                      interval=interval)
            records_to_insert = []
            for ticker in tickers:
                data = stock_data.get(ticker)
                if data is None or data.empty:
                    print('No data to insert')
                    continue
                if check_stock_duplicates(ticker, data, session):
                    continue
                for index, row in data.iterrows():
                    try:
                        record = StockPrices(
                            ticker=ticker,
                            timestamp=datetime.fromisoformat(row.name), # By default, the timestamp was the index
                            open=row['Open'],
                            high=row['High'],
                            low=row['Low'],
                            close=row['Close'],
                            volume=int(row['Volume'])
                        )
                        records_to_insert.append(record)
                    except KeyError as e:
                        print(f'No data for {ticker}, skipping')
                        continue

            if records_to_insert:
                stmt = insert(StockPrices).values([r.model_dump() for r in records_to_insert]).on_conflict_do_nothing(
                    index_elements=['ticker', 'timestamp']
                )
                session.exec(stmt)
                session.commit()
            else:
                print('No records to insert!')
    except Exception as e:
        print(f'Unable to write to database: {e}')

def load_crypto() -> None:
    try:
        with Session(engine) as session:
            crypto_data = fetch_crypto()
            records_to_insert = []
            for coin in crypto_data:
                try:
                    record = CryptoPrices(
                        symbol=coin['symbol'],
                        timestamp=datetime.fromisoformat(coin['last_updated']),
                        price=coin['current_price'],
                        total_volume=coin['total_volume'],
                        market_cap=coin['market_cap'],
                        high_24h=coin['high_24h'],
                        low_24h=coin['low_24h']
                    )
                    records_to_insert.append(record)
                except KeyError as e:
                    print(f'Unable to fetch data for {coin['symbol']}')
            if records_to_insert:
                stmt = insert(CryptoPrices).values([r.model_dump() for r in records_to_insert]).on_conflict_do_nothing(
                    index_elements=['symbol','timestamp']
                )
                session.exec(stmt)
                session.commit()
            else:
                print('No records to insert!')
    except Exception as e:
        print(f'Unable to write to database: {e}')

def main():
    tickers = ['AMD','AAPL']
    load_stocks(tickers=tickers, period='1d',interval='1m')
    load_crypto()

if __name__ == '__main__':
    main()