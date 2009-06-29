from datetime import datetime, timedelta

def thirty_days_range():
    now = datetime.now()
    delta = timedelta(days=30)
    return now - delta