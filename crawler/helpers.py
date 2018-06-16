from datetime import datetime
from dateutil import tz

def convert_time_zone(time, date, from_tz, to_tz):
    curr_datetime = datetime.strptime('{} {}'.format(date, time), '%Y-%m-%d %H:%M:%S')
    from_zone = tz.gettz(from_tz)
    to_zone = tz.gettz(to_tz)
    curr_datetime = curr_datetime.replace(tzinfo=from_zone)
    new_datetime = curr_datetime.astimezone(to_zone)
    new_date = "{}-{}-{}".format(new_datetime.year, new_datetime.month, new_datetime.day)
    new_time = "{}:{}:00".format(new_datetime.hour, new_datetime.minute)
    return (new_time, new_date)
