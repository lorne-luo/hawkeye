from datetime import datetime

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
