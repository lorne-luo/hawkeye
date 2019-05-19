import sys
import time

import os
import pandas as pd
from alpha_vantage.timeseries import TimeSeries

import settings
from asx import get_asx_df

ts = TimeSeries(key=settings.ALPHA_VANTAGE_API_KEY, output_format='pandas', indexing_type='date', retries=3)
base_path = os.path.join(os.getcwd(), 'data')


def download_csv(code, local_priori=False):
    path = f'{base_path}/price/{code}.csv'
    if local_priori and os.path.exists(path):
        df = pd.read_csv(path, index_col='date')
    else:
        df, meta_data = ts.get_daily_adjusted(symbol=f'{code}.AUS')
        df.to_csv(path)
    return df


if __name__ == '__main__':
    if len(sys.argv) > 1:
        print(os.getcwd())
        exit(0)
        arg = sys.argv[1]
        if (len(arg) == 3):
            download_csv(arg)
            exit(0)
        else:
            base_path = os.path.join(base_path, arg)
            print(f'Output to {base_path}')

    df = get_asx_df()
    for i in range(len(df)):
        code = df.iloc[i]['ASX code']
        name = df.iloc[i]['Company name']
        path = f'{base_path}/price/{code}.csv'

        # if os.path.exists(path):
        #     continue

        try:
            download_csv(code, True)
        except Exception as ex:
            print(f'{i}. {code} raise error: {ex}')
            time.sleep(15)
            continue

        print(i, code)
        time.sleep(15)
