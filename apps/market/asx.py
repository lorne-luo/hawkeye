import io
from datetime import datetime

import pandas as pd
import requests
from alpha_vantage.timeseries import TimeSeries
from dateutil.relativedelta import relativedelta, FR

import config.settings.local as settings
from apps.company.models import ASXCompany, Industry
from aws import dynamodb_batch_push


def get_alpha_vantage_api_key():
    return settings.ALPHA_VANTAGE_API_KEY2 if datetime.now().weekday() % 2 else settings.ALPHA_VANTAGE_API_KEY


ts = TimeSeries(key=get_alpha_vantage_api_key(), output_format='pandas', indexing_type='date')


def get_asx_df():
    asx_url = 'https://www.asx.com.au/asx/research/ASXListedCompanies.csv'
    asx_data = requests.get(asx_url).content
    asx_df = pd.read_csv(io.StringIO(asx_data.decode('utf-8')), skiprows=1)

    return asx_df


def get_asx_200_df():
    # s = requests.session()
    # s.config['keep_alive'] = False
    requests.session().close()
    last_month = datetime.now() - relativedelta(months=1)
    month = last_month.strftime('%Y%m01')
    asx_url = f'https://www.asx200list.com/uploads/csv/{month}-asx200.csv'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    asx_data = requests.get(asx_url, headers=headers).content
    requests.session().close()
    asx_df = pd.read_csv(io.StringIO(asx_data.decode('utf-8')), skiprows=1, usecols=[
        'Code', 'Company', 'Sector', 'Market Cap', 'Weight(%)'
    ], index_col='Code')

    return asx_df


def get_asx_200_list():
    df = get_asx_200_df()
    return df.index.values


def get_asx_20_df():
    requests.session().close()
    last_month = datetime.now() - relativedelta(months=1)
    month = last_month.strftime('%Y%m01')
    asx_url = f'https://www.asx20list.com/uploads/csv/{month}-asx20.csv'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    asx_data = requests.get(asx_url, headers=headers).content
    requests.session().close()
    asx_df = pd.read_csv(io.StringIO(asx_data.decode('utf-8')), skiprows=1, usecols=[
        'Code', 'Company', 'Sector', 'Market Cap', 'Weight(%)'
    ], index_col='Code')

    return asx_df


def get_asx_20_list():
    df = get_asx_20_df()
    return df.index.values


def get_price(symbol, outputsize='compact'):
    aus_symbol = '%s.AUS' % symbol
    df, meta_data = ts.get_daily_adjusted(symbol=aus_symbol, outputsize=outputsize)
    df['Return'] = df['5. adjusted close'].pct_change(1)
    return df, meta_data


def get_last_friday():
    return datetime.now() + relativedelta(weekday=FR(-1))


def sync_asx():
    df = get_asx_df()
    counter = 0
    for i in range(len(df)):
        name, code, industry_name = df.iloc[i]['Company name'], df.iloc[i]['ASX code'], df.iloc[i][
            'GICS industry group']
        industry, create = Industry.objects.get_or_create(name=industry_name)
        ASXCompany.objects.update_or_create(code=code, name=name, defaults={'industry': industry, 'is_active': True})
        counter += 1

    inactived = ASXCompany.objects.exclude(code__in=list(df['ASX code'])).update(is_active=False)

    print(f'{counter} companies updated, {inactived} inacitived')
    asx_200 = get_asx_200_list()
    counter = ASXCompany.objects.filter(code__in=asx_200).update(asx_200=True)
    print(f'{counter} ASX 200 companies updated.')
