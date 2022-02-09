import datetime as dt

current_time = dt.datetime.utcnow()
print(current_time)

ten_days_ago = current_time - dt.timedelta(days=10)
print(ten_days_ago)