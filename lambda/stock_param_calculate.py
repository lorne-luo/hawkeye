import boto3
import io
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from urllib.parse import unquote_plus

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
company_table = dynamodb.Table('company')
bucket = 'lorne'


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


def test():
    key = 'hawkeye/recent_price/MOQ.csv'
    csv_file = s3.get_object(Bucket=bucket, Key=key)

    df = pd.read_csv(csv_file['Body'], header=0, index_col='timestamp')
    df['return'] = df['adjusted_close'].pct_change(1)
    df = df.dropna()
    volume_mean = df['volume'].mean()
    return_mean = df['return'].mean()
    return_sigma = df['return'].std()
    start_price = df['close'][-1]
    print(start_price, volume_mean, return_mean, return_sigma)

    days = 30
    simulations = monte_carlo_simulations(start_price, days, return_mean, return_sigma)

    percent99 = np.percentile(simulations, 1)
    percent90 = np.percentile(simulations, 10)
    percent80 = np.percentile(simulations, 20)
    percent70 = np.percentile(simulations, 30)
    percent60 = np.percentile(simulations, 40)

    sim_mean = simulations.mean()
    var = start_price - percent99

    print(percent99, percent90, percent80, percent70, percent60)
    print(sim_mean, var)

    plt.figure(figsize=(16, 6))
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
    plt.title(u"Final price distribution for Woolworths Stock after %s days" % days, weight='bold')

    # save to S3
    img_data = io.BytesIO()
    plt.savefig(img_data, format='png')
    img_data.seek(0)
    s3.put_object(Body=img_data, ContentType='image/png', Bucket=bucket, Key='hawkeye/test.png')


def lambda_handler(event, context):
    test()
    return

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    csv_file = s3.get_object(Bucket=bucket, Key=key)

    path, filename = os.path.split(key)
    code, _ = os.path.splitext(filename)

    df = pd.read_csv(csv_file['Body'], header=0, index_col='timestamp')
    df['return'] = df['adjusted_close'].pct_change(1)
    df = df.dropna()

    volume_mean = df['volume'].mean()
    return_mean = df['return'].mean()
    return_sigma = df['return'].std()
    last_date = df.index[-1]
    start_price = df['close'][-1]
    simulations = monte_carlo_simulations(start_price, 30, return_mean, return_sigma)
    percent99 = np.percentile(simulations, 1)
    percent90 = np.percentile(simulations, 10)
    percent80 = np.percentile(simulations, 20)
    percent70 = np.percentile(simulations, 30)
    percent60 = np.percentile(simulations, 40)

    sim_mean = simulations.mean()
    var = start_price - percent99

    print(bucket)
    print(key)


if __name__ == '__main__':
    import time

    now = time.time()
    df = pd.read_csv('/tmp/MOQ.csv', header=0, index_col='timestamp')
    df['return'] = df['adjusted_close'].pct_change(1)
    df = df.dropna()

    volume_mean = df['volume'].mean()
    return_mean = df['return'].mean()
    return_sigma = df['return'].std()
    start_price = df['close'][-1]
    days = 30
    simulations = monte_carlo_simulations(start_price, days, return_mean, return_sigma, runs=10000)

    percent99 = np.percentile(simulations, 1)
    percent90 = np.percentile(simulations, 10)
    percent80 = np.percentile(simulations, 20)
    percent70 = np.percentile(simulations, 30)
    percent60 = np.percentile(simulations, 40)

    sim_mean = simulations.mean()
    var = start_price - percent99

    print(time.time() - now)
    print(percent99, percent90, percent80, percent70, percent60)
    print(sim_mean, var)

    plt.figure(figsize=(16, 6))
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
    plt.title(u"Final price distribution for Woolworths Stock after %s days" % days, weight='bold')

    # save to S3
    img_data = io.BytesIO()
    plt.savefig(img_data, format='png')
    img_data.seek(0)
    s3.put_object(Body=img_data, ContentType='image/png', Bucket=bucket, Key='hawkeye/test.png')
