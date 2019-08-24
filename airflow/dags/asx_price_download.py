import copy
from datetime import datetime, timedelta

from airflow.operators.bash_operator import BashOperator
from dateutil.relativedelta import relativedelta, FR, SA, SU

from airflow import DAG

PYTHON = '/home/luotao/venv/hawkeye/bin/python'
BASE_DIR = '/opt/hawkeye'


def next_weekday(weekday):
    return datetime.now() + relativedelta(weekday=weekday(+1))


args_friday = {
    'owner': 'luotao',
    'depends_on_past': False,
    'start_date': next_weekday(FR),
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

download_cmd = f'cd {BASE_DIR} && {PYTHON} download.py all'

dag_friday = DAG('asx_price_download_friday', default_args=args_friday, schedule_interval='35 18 * * 5')
# {{ ds_nodash }} the execution date as YYYYMMDD
asx_price_download_friday = BashOperator(
    task_id='asx_price_download_friday',
    bash_command=download_cmd,
    dag=dag_friday)

args_saturday = copy.deepcopy(args_friday)
args_saturday['start_date'] = next_weekday(SA)
dag_saturday = DAG('asx_price_download_saturday', default_args=args_saturday, schedule_interval='5 10 * * 6')

asx_price_download_saturday = BashOperator(
    task_id='asx_price_download_saturday',
    bash_command=download_cmd,
    dag=dag_saturday)

args_sunday = copy.deepcopy(args_friday)
args_sunday['start_date'] = next_weekday(SU)
dag_sunday = DAG('asx_price_download_sunday', default_args=args_sunday, schedule_interval='35 10 * * 7')

asx_price_download_sunday = BashOperator(
    task_id='asx_price_download_sunday',
    bash_command=download_cmd,
    dag=dag_sunday)
