from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator
from airflow import DAG

PYTHON = '/home/luotao/venv/hawkeye/bin/python'
BASE_DIR = '/opt/hawkeye'

default_args = {
    'owner': 'luotao',
    'depends_on_past': False,
    'start_date': datetime(2019, 8, 16, 18, 40),
    'email': ['dev@luotao.net'],
    'email_on_failure': False,
    'email_on_retry': False,
    # 'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

dag = DAG('asx_sync_company', default_args=default_args, schedule_interval=timedelta(weeks=1))

sync_asx_company = BashOperator(
    task_id='asx_sync_company',
    bash_command='cd {{ var.value.HAWKEYE_DIR }} && {{ var.value.HAWKEYE_PYTHON }} manage.py sync_company',
    dag=dag)
