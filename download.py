import os
import random
import sys
import time
from datetime import datetime

import pandas as pd
from alpha_vantage.timeseries import TimeSeries

from asx import get_asx_df, get_codes1, get_codes2, get_last_friday, get_all_codes, get_alpha_vantage_api_key
from core.sms.telstra_api_v2 import send_to_admin

ts = TimeSeries(key=get_alpha_vantage_api_key(), output_format='pandas', indexing_type='date', retries=3)
base_path = os.path.join(os.getcwd(), 'data')


def get_csv_path(code, date=None):
    date = date or 'price'
    folder = os.path.join(base_path, str(date), 'csv')
    if not os.path.isdir(folder):
        os.makedirs(folder)
    path = os.path.join(folder, f'{code}.csv')
    return path


def download_csv(code, path=None, force=False):
    path = path or get_csv_path(code)
    if os.path.exists(path) and not force:
        df = pd.read_csv(path, index_col='date')
    else:
        df, meta_data = ts.get_daily_adjusted(symbol=f'{code}.AUS')
        df.to_csv(path)
    return df


def get_codes(all=False):
    if all:
        df = get_asx_df()
        return df['ASX code'].values
    elif datetime.now().weekday() == 4:
        # return high value stocks
        return get_codes1()
    elif datetime.now().weekday() == 5:
        # return secondary value stocks
        return get_codes2()
    elif datetime.now().weekday() == 6:
        # return all stocks
        # return codes3
        return get_all_codes()
    else:
        # return all
        df = get_asx_df()
        return list(df['ASX code'].values)


if __name__ == '__main__':
    date = get_last_friday()
    date = date.year * 10000 + date.month * 100 + date.day
    sleep = 15
    done = 0
    failure = 0

    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if (len(arg) == 3 and arg != 'all'):
            code = arg.upper()
            download_csv(code, force=True)
            path = get_csv_path(code)
            print(f'Download {code} to {path}')
            exit(0)
        elif arg.isdigit():
            date = int(arg)

    codes = get_codes(all=True) if 'all' in sys.argv else get_codes()
    if 'reverse' in sys.argv:
        codes.reverse()

    folder = os.path.join(base_path, str(date))
    if not os.path.isdir(folder):
        os.makedirs(folder)

    force = '-f' in sys.argv

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
            res = download_csv(code, path, True)
            if res is None or res.empty:
                failure += 1
                print(i, code, path, 'Empty')
            else:
                done += 1
                print(i, code, path, 'Done')

        except Exception as ex:
            failure += 1
            print(f'{i}. {code} raise error: {ex}')
            time.sleep(sleep)
            continue

        if failure > 300:
            break

        time.sleep(sleep + random.randint(0, 5))

    print(f'Download finished, done = {done}, failure = {failure}')
    send_to_admin(f'[Hawkeye] Download finished, done = {done}, failure = {failure}')
