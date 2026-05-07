import airflow.sdk.exceptions
from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import dag, task
from ingestion.scripts.load_raw import load_crypto, load_stocks
from datetime import datetime, timedelta

@dag(schedule='*/15 * * * *',start_date=datetime(2026, 5, 8), catchup=False)
def market_pipeline():
    @task
    def stocks():
        tickers = ['AAPL','AMD','MSFT']
        load_stocks(tickers=tickers,
                    period='1m',
                    interval='1m')
    @task
    def crypto():
        load_crypto()

    run_command = BashOperator(task_id='dbt_run',
                                bash_command='dbt run --project-dir dbt/market_data',
                               retries=3)
    test_command = BashOperator(task_id='dbt_test',
                                bash_command='dbt test --project-dir dbt/market_data',
                                retries=3)
    stocks_task = stocks()
    crypto_task = crypto()
    [stocks_task, crypto_task] >> run_command >> test_command

market_pipeline()
