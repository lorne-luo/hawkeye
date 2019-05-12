import os
import time
from alpha_vantage.timeseries import TimeSeries

from asx import get_asx_df
import pandas as pd

ts = TimeSeries(key=os.environ.get('ALPHA_VANTAGE_API_KEY'), output_format='pandas', indexing_type='date', retries=3)

result_path = './pic/'


def download_csv(code, local_priori=False):
    path = f'./price/{code}.csv'
    if local_priori and os.path.exists(path):
        df = pd.read_csv(path, index_col='date')
    else:
        df, meta_data = ts.get_daily_adjusted(symbol=f'{code}.AUS')
        df.to_csv(path)
    return df


if __name__ == '__main__':
    df = get_asx_df()

    for i in range(len(df)):
        code = df.iloc[i]['ASX code']
        name = df.iloc[i]['Company name']
        if i < 1073:
            continue

        try:
            download_csv(code, True)
        except Exception as ex:
            print(f'{i}. {code} raise error: {ex}')
            time.sleep(31)
            continue

        print(i, code)
        time.sleep(31)
