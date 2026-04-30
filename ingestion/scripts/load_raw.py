from fetchers import *
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, create_engine, select
from sqlalchemy import exists
from dotenv import load_dotenv
import os
import psycopg

load_dotenv()
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
DB_NAME = os.getenv('DB_NAME')

url = f'postgresql+psycopg://{USER}:{PASSWORD}@localhost:5433/{DB_NAME}'
engine = create_engine(url=url, echo=False)

def load_stocks(tickers: list) -> None:
    try:
        with Session(engine) as session:
            