from dotenv import load_dotenv
import os
import psycopg

load_dotenv()
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
DB_NAME = os.getenv('DB_NAME')


try:
    conn = psycopg.connect(
        host="localhost",
        port=5433,
        dbname=DB_NAME,
        user=USER,
        password=PASSWORD
    )
    print("Connection successful!")
    conn.close()
except Exception as e:
    print(f"Connection failed: {e}")