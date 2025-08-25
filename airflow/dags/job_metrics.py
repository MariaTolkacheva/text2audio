from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import psycopg2

DB_URL = os.getenv("AIRFLOW__DATABASE__SQL_ALCHEMY_CONN")
# Example: postgresql+psycopg2://app:app@db:5432/appdb
# psycopg2 wants: dbname=, user=, password=, host=, port=
# We'll parse crudely for the demo:
def _pg_conn_params():
    # Not robust parsing; OK for demo
    s = DB_URL.split("://", 1)[1]           # app:app@db:5432/appdb
    creds, right = s.split("@")
    user, pwd = creds.split(":")
    hostport, dbname = right.split("/")
    host, port = hostport.split(":")
    return dict(dbname=dbname, user=user, password=pwd, host=host, port=port)

def count_jobs():
    p = _pg_conn_params()
    conn = psycopg2.connect(**p)
    cur = conn.cursor()
    cur.execute("SELECT status, COUNT(*) FROM jobs GROUP BY status;")
    rows = cur.fetchall()
    print("Job counts by status:", rows)
    cur.close()
    conn.close()

with DAG(
    dag_id="job_metrics",
    start_date=datetime(2025, 1, 1),
    schedule_interval="@hourly",
    catchup=False,
    tags=["demo"]
) as dag:
    PythonOperator(
        task_id="count_jobs",
        python_callable=count_jobs
    )
