import time

import csv
import matplotlib.pyplot as plt
import numpy as np
import os
from alpha_vantage.timeseries import TimeSeries
from decimal import Decimal

from asx import get_asx_df
import pandas as pd

ts = TimeSeries(key=os.environ.get('ALPHA_VANTAGE_API_KEY'), output_format='pandas', indexing_type='date', retries=3)

result_path = './pic/'


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


def download_csv(code, local_priori=False):
    path = f'./price/{code}.csv'
    if local_priori and os.path.exists(path):
        df = pd.read_csv(path, index_col='date')
    else:
        df, meta_data = ts.get_daily_adjusted(symbol=f'{code}.AUS')
        df.to_csv(path)
    return df


def process_stock(code, name):
    df = download_csv(code)

    df['return'] = df['5. adjusted close'].pct_change(1)
    df = df.dropna()
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
    plt.figtext(0.6, 0.7, "Mean final price: $%.2f" % simulations.mean())
    plt.figtext(0.6, 0.6, "VaR(0.99): $%.2f" % (start_price - percent99,))
    plt.figtext(0.15, 0.6, "q(0.99): $%.2f" % percent99)
    plt.axvline(x=percent99, linewidth=1, color='r')
    plt.axvline(x=percent90, linewidth=1, color='r')
    plt.axvline(x=percent80, linewidth=1, color='r')
    plt.axvline(x=percent70, linewidth=1, color='r')
    plt.axvline(x=percent60, linewidth=1, color='r')
    plt.title(f"Final price distribution for {name} Stock after %s {days}", weight='bold')

    plt.savefig(f'{result_path}{code}.png', format='png')
    plt.clf()
    plt.cla()
    plt.close()

    # print(code, start_price, simulations.mean(), float(start_price - percent99))
    return start_price, simulations.mean(), Decimal(simulations.mean() - start_price).quantize(
        Decimal('0.000000000000001')), \
           Decimal(start_price - percent99).quantize(Decimal('0.000000000000001')), \
           Decimal((start_price - percent99) / start_price * 100).quantize(
               Decimal('0.001')), percent99, percent90, percent80, percent70, percent60


if __name__ == '__main__':
    df = get_asx_df()

    with open('{result_path}result.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            ['code', 'start price', 'mean', 'mean diff', 'VaR 99%', 'VaR 99% Percent', 'percent99', 'percent90',
             'percent80',
             'percent70',
             'percent60'])

    plt.figure(figsize=(16, 6))

    for i in range(len(df)):
        code = df.iloc[i]['ASX code']
        name = df.iloc[i]['Company name']
        if i < 1073:
            continue

        if os.path.exists(f'{result_path}{code}.png'):
            continue
        try:
            result = process_stock(code, name)
        except Exception as ex:
            print(f'{i}. {code} raise error: {ex}')
            time.sleep(31)
            continue
        with open(f'{result_path}result.csv', 'a') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow((code,) + result)

        print(i, code, result)
        time.sleep(31)
