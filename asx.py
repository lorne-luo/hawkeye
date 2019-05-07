import io
import os
import pandas as pd
import requests
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.sectorperformance import SectorPerformances
from alpha_vantage.cryptocurrencies import CryptoCurrencies


def get_asx_list():
    asx_url = 'https://www.asx.com.au/asx/research/ASXListedCompanies.csv'
    asx_data = requests.get(asx_url).content
    dateparse = lambda x: pd.datetime.strptime(x, '%Y-%d-%m')

    asx_df = pd.read_csv(io.StringIO(asx_data.decode('utf-8')), skiprows=1)

    asx_list = asx_df['ASX code'].tolist()
    return asx_list


ts = TimeSeries(key=os.environ['ALPHA_VANTAGE_API_KEY'], output_format='pandas', indexing_type='date')


def get_price(symbol, outputsize='compact'):
    aus_symbol = '%s.AUS' % symbol
    df, meta_data = ts.get_daily_adjusted(symbol=aus_symbol, outputsize=outputsize)
    df['Return'] = df['5. adjusted close'].pct_change(1)
    return df, meta_data
