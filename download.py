import sys
import time

import os
from datetime import datetime

import pandas as pd
from alpha_vantage.timeseries import TimeSeries

import settings
from asx import get_asx_df, codes1, codes2, get_last_friday

ts = TimeSeries(key=settings.ALPHA_VANTAGE_API_KEY, output_format='pandas', indexing_type='date', retries=3)
base_path = os.path.join(os.getcwd(), 'data')


def get_csv_path(code, date=None):
    date = date or 'price'
    folder = os.path.join(base_path, str(date), 'csv')
    if not os.path.isdir(folder):
        os.makedirs(folder)
    path = os.path.join(folder, f'{code}.csv')
    return path


def download_csv(code, path=None):
    path = path or get_csv_path(code)
    if os.path.exists(path):
        df = pd.read_csv(path, index_col='date')
    else:
        df, meta_data = ts.get_daily_adjusted(symbol=f'{code}.AUS')
        df.to_csv(path)
    return df


def get_codes():
    if datetime.now().weekday() == 5:
        # return high value stocks
        return codes1
    elif datetime.now().weekday() == 6:
        # return secondary value stocks
        return codes2
    else:
        # return all
        df = get_asx_df()
        return df['ASX code'].values


if __name__ == '__main__':
    date = get_last_friday()
    date = date.year * 10000 + date.month * 100 + date.day

    done = 0
    failure = 0

    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if (len(arg) == 3):
            code = arg.upper()
            download_csv(code)
            path = get_csv_path(code)
            print(f'Download {code} to {path}')
            exit(0)
        elif arg.isdigit():
            date = int(arg)

    codes = get_codes()
    folder = os.path.join(base_path, str(date))
    if not os.path.isdir(folder):
        os.makedirs(folder)

    print('')
    print(f'############ {datetime.now()} ############')
    print(f'Download to {folder}')
    print(f'Stock count = {len(codes)}')

    for i in range(len(codes)):
        code = codes[i]
        path = get_csv_path(code, date)

        if os.path.exists(path):
            continue

        try:
            res = download_csv(code, path)
            if res is None or res.empty:
                failure += 1
                print(i, code, path, 'Empty')
            else:
                done += 1
                print(i, code, path, 'Done')

        except Exception as ex:
            failure += 1
            print(f'{i}. {code} raise error: {ex}')
            time.sleep(15)
            continue

        if done > 490:
            break

        time.sleep(15)

    print(f'Download finished, done = {done}, failure = {failure}')
