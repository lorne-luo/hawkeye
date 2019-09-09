from datetime import datetime, timedelta

from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
from dateutil.relativedelta import relativedelta, FR

from airflow import DAG

PYTHON = '/home/luotao/venv/hawkeye/bin/python'
BASE_DIR = '/opt/hawkeye'


def next_weekday(weekday):
    return datetime.now() + relativedelta(weekday=weekday(+1))


default_args = {
    'owner': 'luotao',
    'depends_on_past': False,
    'start_date': days_ago(2),
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

dag = DAG('asx_load_predict', default_args=default_args, schedule_interval='30 10 * * 1')

asx_load_predict = BashOperator(
    task_id='asx_load_predict',
    bash_command=f'cd {BASE_DIR} && {PYTHON} manage.py load_predict',
    dag=dag)
