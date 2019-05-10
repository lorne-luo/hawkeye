import io
import os
import pandas as pd
import requests
from alpha_vantage.timeseries import TimeSeries
from datetime import datetime

import settings
from aws import dynamodb, dynamodb_batch_push

BATCH_LIMIT = 25


def get_asx_df():
    asx_url = 'https://www.asx.com.au/asx/research/ASXListedCompanies.csv'
    asx_data = requests.get(asx_url).content
    asx_df = pd.read_csv(io.StringIO(asx_data.decode('utf-8')), skiprows=1)

    return asx_df


ts = TimeSeries(key=settings.ALPHA_VANTAGE_API_KEY, output_format='pandas', indexing_type='date')


def get_price(symbol, outputsize='compact'):
    aus_symbol = '%s.AUS' % symbol
    df, meta_data = ts.get_daily_adjusted(symbol=aus_symbol, outputsize=outputsize)
    df['Return'] = df['5. adjusted close'].pct_change(1)
    return df, meta_data


def push_industry(df):
    industry_set = df['GICS industry group'].unique()
    items = [{'name': i} for i in industry_set]

    dynamodb_batch_push('industry', items)


def push_company(df):
    items = [{'code': df.iloc[i]['ASX code'],
              'name': df.iloc[i]['Company name'],
              'industry': df.iloc[i]['GICS industry group'],
              'last_active': datetime.now().strftime('%Y-%m-%d')}
             for i in range(len(df))]

    dynamodb_batch_push('industry', items)


if __name__ == '__main__':
    df = get_asx_df()
    push_industry(df)
    push_company(df)
