from datetime import datetime, timedelta, date
from dateutil.tz import tzlocal

def epoch_time(x=datetime.now(tzlocal())):
  if type(x) == date:
    x = datetime.combine(x, datetime.min.time())
  return x.timestamp()

def time_in_past(weeks=0, days=0, hours=0, minutes=0):
  now = datetime.now(tzlocal())
  time = now - timedelta(weeks=weeks, days=days, hours=minutes, minutes=minutes)
  return time