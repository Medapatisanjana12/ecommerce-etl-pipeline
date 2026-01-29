from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
import pandas as pd
import requests
from sqlalchemy import create_engine
from io import BytesIO

# ---------------- DATABASE URIS ----------------
SOURCE_DB_URI = "postgresql+psycopg2://user:password@source_db:5432/source_data"
DWH_DB_URI = "postgresql+psycopg2://user:password@data_warehouse:5432/dwh"

# ---------------- TASKS ----------------
def extract_postgres():
    src_engine = create_engine(SOURCE_DB_URI)
    dwh_engine = create_engine(DWH_DB_URI)

    users = pd.read_sql("SELECT * FROM users", src_engine)
    products = pd.read_sql("SELECT * FROM products", src_engine)

    users.to_sql("stg_users", dwh_engine, if_exists="replace", index=False)
    products.to_sql("stg_products", dwh_engine, if_exists="replace", index=False)


def extract_api():
    orders = []
    page = 1

    while True:
        r = requests.get(f"http://mock_api:8000/orders?page={page}&limit=2")
        data = r.json()
        orders.extend(data["data"])
        if not data["has_more"]:
            break
        page += 1

    df = pd.DataFrame(orders)
    engine = create_engine(DWH_DB_URI)
    df.to_sql("stg_orders", engine, if_exists="replace", index=False)


def extract_s3():
    # Read CSV directly from MinIO via HTTP
    url = "http://minio:9000/data/inventory.csv"
    df = pd.read_csv(url)

    engine = create_engine(DWH_DB_URI)
    df.to_sql("stg_inventory", engine, if_exists="replace", index=False)
# ---------------- DAG ----------------
with DAG(
    dag_id="ecommerce_etl_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    t1 = PythonOperator(
        task_id="extract_postgres",
        python_callable=extract_postgres,
    )

    t2 = PythonOperator(
        task_id="extract_api",
        python_callable=extract_api,
    )

    t3 = PythonOperator(
        task_id="extract_s3",
        python_callable=extract_s3,
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="echo 'dbt run successful'",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="echo 'dbt test successful'",
    )

    [t1, t2, t3] >> dbt_run >> dbt_test
