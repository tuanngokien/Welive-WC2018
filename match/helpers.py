from datetime import timedelta, date, datetime

DATE_FORMAT = "%Y-%m-%d"

def str_to_date(_date):
    return datetime.strptime(_date, DATE_FORMAT)

def date_to_str(_date):
    return _date.strftime(DATE_FORMAT)

def add_day(_date, day_to_add):
    if not isinstance(_date, date):
        _date = str_to_date(_date)
    return _date + timedelta(days = day_to_add)