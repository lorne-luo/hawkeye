def date_to_int(d):
    return d.year * 10000 + d.month * 100 + d.day


def date_to_str(d):
    return d.strftime('%Y-%m-%d')


def return_percent(current_price, previous_price):
    return round((current_price - previous_price) / previous_price * 100, 3)
