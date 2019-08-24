from datetime import datetime, timedelta

from airflow.operators.bash_operator import BashOperator
from dateutil.relativedelta import relativedelta, SU

from airflow import DAG

PYTHON = '/home/luotao/venv/hawkeye/bin/python'
BASE_DIR = '/opt/hawkeye'


def next_weekday(weekday):
    return datetime.now() + relativedelta(weekday=weekday(+1))


default_args = {
    'owner': 'luotao',
    'depends_on_past': False,
    'start_date': next_weekday(SU),
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

dag = DAG('asx_predict', default_args=default_args, schedule_interval='35 15 * * 7')

asx_predict = BashOperator(
    task_id='asx_predict',
    bash_command='cd {{ var.value.HAWKEYE_DIR }} && {{ var.value.HAWKEYE_PYTHON }} predict.py all',
    dag=dag)
