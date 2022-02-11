from datetime import datetime


from datetime import datetime

def str_to_datetime(date_time_str):
    return datetime.strptime(date_time_str, '%Y-%m-%d')