from datetime import datetime

from dateutil.relativedelta import relativedelta, MO, TU, WE, TH, FR, SA, SU


def date_to_int(d):
    return d.year * 10000 + d.month * 100 + d.day


def date_to_str(d):
    return d.strftime('%Y-%m-%d')


def return_percent(current_price, previous_price):
    return round((current_price - previous_price) / previous_price * 100, 3)


def get_next_weekday(weekday):
    return datetime.now() + relativedelta(weekday=weekday(+1))


def get_next_saturday():
    return datetime.now() + relativedelta(weekday=SA(+1))


def get_next_sunday():
    return datetime.now() + relativedelta(weekday=SU(+1))


def get_next_sunday():
    return datetime.now() + relativedelta(weekday=SU(+1))
