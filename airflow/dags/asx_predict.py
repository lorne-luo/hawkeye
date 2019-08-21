from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator
from airflow import DAG

PYTHON = '/home/luotao/venv/hawkeye/bin/python'
BASE_DIR = '/opt/hawkeye'

default_args = {
    'owner': 'luotao',
    'depends_on_past': False,
    'start_date': datetime(2019, 5, 19, 15, 0),
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

dag = DAG('asx_predict', default_args=default_args, schedule_interval=timedelta(weeks=1))

asx_predict = BashOperator(
    task_id='asx_predict',
    bash_command=f'cd {{ var.value.HAWKEYE_DIR }}',  # && {{ var.value.HAWKEYE_PYTHON }} download.py all
    dag=dag)
