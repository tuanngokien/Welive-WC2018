from datetime import timedelta, date, datetime, time
from django.utils import timezone

DATE_FORMAT = "%Y-%m-%d"

def str_to_date(_date):
    return datetime.strptime(_date, DATE_FORMAT)

def date_to_str(_date):
    return _date.strftime(DATE_FORMAT)

def add_day(_date, day_to_add):
    if not isinstance(_date, date):
        _date = str_to_date(_date)
    return _date + timedelta(days = day_to_add)

def get_vi_datetime_now():
    return timezone.localtime()

def get_vi_today_date():
    datetime_now = get_vi_datetime_now()
    date_now = datetime_now.date()
    time_now = datetime_now.time()
    if time_now > time(6,0,0):
        return date_now
    else:
        return add_day(date_now, -1)