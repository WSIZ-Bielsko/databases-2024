from croniter import croniter
from datetime import datetime, timedelta


def get_next_cron_timestamp(cron_expression: str, start_time=None) -> datetime:
    if start_time is None:
        start_time = datetime.now()

    cron = croniter(cron_expression, start_time)
    next_timestamp = cron.get_next(datetime)

    return next_timestamp




def test_next_sunday():
    now = datetime(year=2024, month=9, day=14, hour=12, minute=59, second=59)
    sunday_cron = '0 2 * * 0'
    x = get_next_cron_timestamp(sunday_cron, start_time=now)
    assert x.day == 15 and x.month == 9 and x.hour == 2


def test_end_quarter_september():
    now = datetime(year=2024, month=9, day=14, hour=12, minute=59, second=59)
    day_before_quatrter_end = '0 2 L 3,6,9,12 *'
    x = get_next_cron_timestamp(day_before_quatrter_end, start_time=now)
    x -= timedelta(days=1)
    assert x.day == 29 and x.month == 9

def test_midnight_daily():
    now = datetime(year=2024, month=9, day=14, hour=23, minute=59, second=59)
    daily_cron = '0 0 * * *'
    x = get_next_cron_timestamp(daily_cron, start_time=now)
    assert x.day == 15 and x.month == 9 and x.hour == 0 and x.minute == 0

def test_weekday_morning():
    now = datetime(year=2024, month=9, day=14, hour=12, minute=0, second=0)
    weekday_morning_cron = '0 9 * * 1-5'
    x = get_next_cron_timestamp(weekday_morning_cron, start_time=now)
    assert x.day == 16 and x.month == 9 and x.hour == 9

def test_monthly_first_day():
    now = datetime(year=2024, month=9, day=14, hour=12, minute=0, second=0)
    first_day_month_cron = '0 0 1 * *'
    x = get_next_cron_timestamp(first_day_month_cron, start_time=now)
    assert x.day == 1 and x.month == 10 and x.hour == 0

def test_every_hour():
    now = datetime(year=2024, month=9, day=14, hour=12, minute=59, second=59)
    hourly_cron = '0 * * * *'
    x = get_next_cron_timestamp(hourly_cron, start_time=now)
    assert x.day == 14 and x.month == 9 and x.hour == 13 and x.minute == 0

def test_every_five_minutes():
    now = datetime(year=2024, month=9, day=14, hour=12, minute=5, second=0)
    every_five_minutes_cron = '*/5 * * * *'
    x = get_next_cron_timestamp(every_five_minutes_cron, start_time=now)
    assert x.day == 14 and x.month == 9 and x.hour == 12 and x.minute == 10

def test_specific_date_time():
    # fixme: fails
    now = datetime(year=2024, month=9, day=14, hour=12, minute=0, second=0)
    specific_date_time_cron = '0 15 10 15 9 *'
    x = get_next_cron_timestamp(specific_date_time_cron, start_time=now)
    assert x.day == 15 and x.month == 9 and x.hour == 10 and x.minute == 15

def test_last_friday_of_month():
    # fixme: fails
    now = datetime(year=2024, month=9, day=14, hour=12, minute=0, second=0)
    last_friday_cron = '0 0 * * 5L'
    x = get_next_cron_timestamp(last_friday_cron, start_time=now)
    assert x.day == 27 and x.month == 9 and x.hour == 0

def test_quarterly_on_15th():
    now = datetime(year=2024, month=9, day=14, hour=12, minute=0, second=0)
    quarterly_cron = '0 0 15 1,4,7,10 *'
    x = get_next_cron_timestamp(quarterly_cron, start_time=now)
    assert x.day == 15 and x.month == 10 and x.hour == 0

def test_weekly_on_monday():
    now = datetime(year=2024, month=9, day=14, hour=12, minute=0, second=0)
    weekly_monday_cron = '0 0 * * 1'
    x = get_next_cron_timestamp(weekly_monday_cron, start_time=now)
    assert x.day == 16 and x.month == 9 and x.hour == 0

def test_yearly_on_new_year():
    now = datetime(year=2024, month=9, day=14, hour=12, minute=0, second=0)
    new_year_cron = '0 0 1 1 *'
    x = get_next_cron_timestamp(new_year_cron, start_time=now)
    assert x.day == 1 and x.month == 1 and x.year == 2025 and x.hour == 0



if __name__ == '__main__':
    # Example usage
    cron_expression = "*/10 9-17 1 * *"  # Every 10 minutes between 9 AM and 5 PM on the 1st of every month
    next_time = get_next_cron_timestamp(cron_expression)
    print(f"Next execution time: {next_time}")
    zz = next_time.date()
    print(type(zz))