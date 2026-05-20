from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys

# Access scripts folder
sys.path.append('/opt/airflow/scripts')

from extract import extract_news
from transform import transform_data
from load import load_to_mysql

default_args = {
    "owner": "viveena",
    "start_date": datetime(2025, 1, 1),
    "retries": 2,
    "retry_delay": timedelta(minutes=2)
}

with DAG(

    dag_id="news_etl_pipeline",

    description="Automated News ETL Pipeline using Airflow",

    default_args=default_args,

    schedule="@daily",

    catchup=False

) as dag:

    extract_task = PythonOperator(
        task_id="extract_news",
        python_callable=extract_news
    )

    transform_task = PythonOperator(
        task_id="transform_news",
        python_callable=transform_data
    )

    load_task = PythonOperator(
        task_id="load_news",
        python_callable=load_to_mysql
    )

    extract_task >> transform_task >> load_task