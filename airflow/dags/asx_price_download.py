import copy
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator
from airflow import DAG

PYTHON = '/home/luotao/venv/hawkeye/bin/python'
BASE_DIR = '/opt/hawkeye'

args_friday = {
    'owner': 'luotao',
    'depends_on_past': False,
    'start_date': datetime(2019, 5, 17, 19, 0),
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

dag_friday = DAG('asx_price_download_friday', default_args=args_friday, schedule_interval=timedelta(weeks=1))
# {{ ds_nodash }} the execution date as YYYYMMDD
asx_price_download_friday = BashOperator(
    task_id='asx_price_download_friday',
    bash_command=f'cd {{ var.value.HAWKEYE_DIR }}',  # && {{ var.value.HAWKEYE_PYTHON }} download.py all
    dag=dag_friday)

args_saturday = copy.deepcopy(args_friday)
args_saturday['start_date'] = datetime(2019, 5, 18, 10, 0)
dag_saturday = DAG('asx_price_download_saturday', default_args=args_saturday, schedule_interval=timedelta(weeks=1))

asx_price_download_saturday = BashOperator(
    task_id='asx_price_download_saturday',
    bash_command=f'cd {{ var.value.HAWKEYE_DIR }}',  # && {{ var.value.HAWKEYE_PYTHON }} download.py all
    dag=dag_saturday)

args_sunday = copy.deepcopy(args_friday)
args_sunday['start_date'] = datetime(2019, 5, 19, 10, 0)
dag_sunday = DAG('asx_price_download_sunday', default_args=args_sunday, schedule_interval=timedelta(weeks=1))

asx_price_download_sunday = BashOperator(
    task_id='asx_price_download_sunday',
    bash_command=f'cd {{ var.value.HAWKEYE_DIR }}',  # && {{ var.value.HAWKEYE_PYTHON }} download.py all
    dag=dag_sunday)
