import sys
import time

import os
import pandas as pd
from alpha_vantage.timeseries import TimeSeries

import settings
from asx import get_asx_df

ts = TimeSeries(key=settings.ALPHA_VANTAGE_API_KEY, output_format='pandas', indexing_type='date', retries=3)
folder = './data'


def download_csv(code, local_priori=False):
    path = f'{folder}/price/{code}.csv'
    if local_priori and os.path.exists(path):
        df = pd.read_csv(path, index_col='date')
    else:
        df, meta_data = ts.get_daily_adjusted(symbol=f'{code}.AUS')
        df.to_csv(path)
    return df


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if (len(arg) == 3):
            download_csv(arg)
            exit(0)
        else:
            folder = os.path.join(folder, arg)
            print(f'Output to {folder}')

    df = get_asx_df()
    for i in range(len(df)):
        code = df.iloc[i]['ASX code']
        name = df.iloc[i]['Company name']
        path = f'{folder}/price/{code}.csv'

        # if os.path.exists(path):
        #     continue

        try:
            download_csv(code, True)
        except Exception as ex:
            print(f'{i}. {code} raise error: {ex}')
            time.sleep(21)
            continue

        print(i, code)
        time.sleep(21)
