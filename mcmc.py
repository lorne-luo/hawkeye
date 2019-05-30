from datetime import datetime
import numpy as np
from dateutil.relativedelta import relativedelta


def get_sigma(df, train_day):
    start_date = datetime.now() - relativedelta(days=180)
    start_date = start_date.strftime('%Y-%m-%d')

    # Now let's grab our mu (drift) from the expected return data we got for AAPL
    mu = df[start_date:].mean()['Return']

    # Now let's grab the volatility of the stock from the std() of the average return
    sigma = df.std()['Return']
    return mu, sigma


def predict(df, train_days=180, sim_days=30):
    # Now our delta
    dt = 1 / sim_days

    mu, sigma = get_sigma(df, train_days)


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
