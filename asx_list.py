import io
import pandas as pd
import requests


def get_asx_list():
    asx_url = 'https://www.asx.com.au/asx/research/ASXListedCompanies.csv'
    asx_data = requests.get(asx_url).content
    asx_df = pd.read_csv(io.StringIO(asx_data.decode('utf-8')), skiprows=1)

    asx_list = asx_df['ASX code'].tolist()
    return asx_list