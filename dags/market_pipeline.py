import airflow.sdk.exceptions
from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import dag, task
from ingestion.scripts.load_raw import load_crypto, load_stocks
from datetime import datetime, timedelta

@dag(start_date=datetime(2026, 5, 8), catchup=False):
def market_pipeline():
    @task
    def load_data():
        tickers = ['AAPL','AMD','MSFT']
        load_stocks(tickers=tickers,
                    period='1m',
                    interval='1m')
        load_crypto()
    @task
    def run_dbt():
        try:
            run_command = BashOperator(task_id='dbt_run',
                                        bash_command='dbt run --project-dir dbt/market_data')
            test_command = BashOperator(task_id='dbt_test',
                                        bash_command='dbt test --project-dir dbt/market_data')
        except airflow.sdk.exceptions.AirflowSkipException as e:
            print('Command failed, skipping')
            print(f'{e}')
        except airflow.sdk.exceptions.AirflowException as e:
            print('Command failed')
            print(f'{e}')