import os
from django.conf import settings


def get_week_folder(week):
    return os.path.join(settings.BASE_DIR, 'data', str(week))


def get_result_path(week):
    return os.path.join(get_week_folder(week), 'result.csv')


def get_csv_folder(week):
    return os.path.join(get_week_folder(week), str(week), 'csv')
