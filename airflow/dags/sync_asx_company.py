from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator
from airflow import DAG

ENV_DIR = '/home/luotao/venv/hawkeye/bin/'
BASE_DIR = '/opt/hawkeye'

default_args = {
    'owner': 'luotao',
    'depends_on_past': False,
    'start_date': datetime(2019, 8, 16),
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

dag = DAG('sync_asx_company', default_args=default_args, schedule_interval=timedelta(weeks=1))

# {{ ds_nodash }} the execution date as YYYYMMDD
sync_asx_company = BashOperator(
    task_id='sync_asx_company',
    bash_command=f'cd {BASE_DIR} && {ENV_DIR}python manage.py sync_company',
    dag=dag)
