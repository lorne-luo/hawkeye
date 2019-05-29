import sys

import csv
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from decimal import Decimal

import settings
from asx import get_asx_df, get_last_friday
from download import get_csv_path

ts = TimeSeries(key=settings.ALPHA_VANTAGE_API_KEY, output_format='pandas', indexing_type='date', retries=3)
friday = get_last_friday()
friday = friday.year * 10000 + friday.month * 100 + friday.day
base_path = os.path.join(os.getcwd(), 'data', str(friday))
pic_folder = os.path.join(base_path, 'pic')


def stock_monte_carlo(start_price, days, mu, sigma):
    ''' This function takes in starting stock price, days of simulation,mu,sigma, and returns simulated price array'''
    dt = 1 / days
    price = np.zeros(days)
    price[0] = start_price

    shock = np.zeros(days)
    drift = np.zeros(days)

    for x in range(1, days):
        shock[x] = np.random.normal(loc=mu * dt, scale=sigma * np.sqrt(dt))
        drift[x] = mu * dt
        price[x] = price[x - 1] + (price[x - 1] * (drift[x] + shock[x]))
    return price


def monte_carlo_simulations(start_price, days, mu, sigma, runs=10000):
    # Create an empty matrix to hold the end price data
    simulations = np.zeros(runs)

    # Set the print options of numpy to only display 0-5 points from an array to suppress output
    np.set_printoptions(threshold=5)

    for run in range(runs):
        # Set the simulation data point as the last stock price for that run
        simulations[run] = stock_monte_carlo(start_price, days, mu, sigma)[days - 1]

    return simulations


def get_csv(code, download=False):
    path = get_csv_path(code, friday)
    if os.path.exists(path):
        df = pd.read_csv(path, index_col='date')
    elif download:
        df, meta_data = ts.get_daily_adjusted(symbol=f'{code}.AUS')
        df.to_csv(path)
    else:
        df = None
    return df


def process_stock(code, name=None):
    name = name or code
    df = get_csv(code)

    if df is None or df.empty:
        print(f'{code} have no data, skipped.')
        return None

    df['return'] = df['5. adjusted close'].pct_change(1)
    df = df.dropna()
    if len(df) < 60:
        return None

    volume_mean = df['6. volume'].mean()
    return_mean = df['return'].mean()
    return_sigma = df['return'].std()
    start_price = df['4. close'][-1]
    # print(start_price, volume_mean, return_mean, return_sigma)

    days = 30
    simulations = monte_carlo_simulations(start_price, days, return_mean, return_sigma)

    percent99 = np.percentile(simulations, 1)
    percent90 = np.percentile(simulations, 10)
    percent80 = np.percentile(simulations, 20)
    percent70 = np.percentile(simulations, 30)
    percent60 = np.percentile(simulations, 40)

    sim_mean = simulations.mean()
    var = start_price - percent99

    # print(percent99, percent90, percent80, percent70, percent60)
    # print(sim_mean, var)

    # define q as the 1% empirical qunatile, this basically means that 99% of the values should fall between here

    # plot the distribution of the end prices
    plt.hist(simulations, bins=200)

    # Using plt.figtext to fill in some additional information onto the plot

    # Starting Price
    plt.figtext(0.6, 0.8, s="Start price: $%.2f" % start_price)
    # Mean ending price
    plt.figtext(0.6, 0.7, "Mean final price: $%.2f" % sim_mean)
    plt.figtext(0.6, 0.6, "VaR(0.99): $%.2f" % (var,))
    plt.figtext(0.15, 0.6, "q(0.99): $%.2f" % percent99)
    plt.axvline(x=percent99, linewidth=1, color='r')
    plt.axvline(x=percent90, linewidth=1, color='r')
    plt.axvline(x=percent80, linewidth=1, color='r')
    plt.axvline(x=percent70, linewidth=1, color='r')
    plt.axvline(x=percent60, linewidth=1, color='r')
    plt.title(f"Final price distribution for {name} Stock after %s {days}", weight='bold')

    plt.savefig(os.path.join(pic_folder, f'{code}.png'), format='png')
    plt.clf()
    plt.cla()
    plt.close()

    return df.index.max(), start_price, round(sim_mean, 2), sim_mean - start_price, \
           round(var, 4), round(var / start_price * 100, 4), \
           volume_mean, return_mean, return_sigma, percent99, percent90, percent80, percent70, percent60


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if (len(arg) == 3):
            code = arg.upper()
            friday = get_last_friday()
            friday = friday.year * 10000 + friday.month * 100 + friday.day
            friday = sys.argv[2] if len(sys.argv) > 2 else friday
            result = process_stock(code)
            print((code,) + result)
            exit(0)

    print('')
    print(f'############ {datetime.now()} ############')
    print(f'Result save to {base_path}')
    plt.figure(figsize=(16, 6))
    done = 0
    failure = 0

    if not os.path.isdir(pic_folder):
        os.makedirs(pic_folder)

    df = get_asx_df()
    result_path=os.path.join(base_path, 'result.csv')
    with open(result_path, 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            ['code', 'last_date', 'start price', 'sim_mean', 'sim_diff', 'VaR 99%', 'VaR 99% Percent', 'volume_mean',
             'return_mean', 'return_sigma', 'percent99', 'percent90', 'percent80', 'percent70', 'percent60'])

        for i in range(len(df)):
            code = df.iloc[i]['ASX code']
            name = df.iloc[i]['Company name']
            path = get_csv_path(code, friday)

            if not os.path.exists(path):
                failure += 1
                print(i, code, 'No data skipped.')
                continue

            try:
                result = process_stock(code, name)
                done += 1
            except Exception as ex:
                failure += 1
                print(f'{i}. {code} raise error: {ex}')
                continue

            if not result:
                failure += 1
                print(f'{i}. {code} got None')
                continue

            writer = csv.writer(csvfile)
            writer.writerow((code,) + result)
            csvfile.flush()
            print(i, code, result)

    print(f'Download finished, done = {done}, failure = {failure}')
    print(result_path)