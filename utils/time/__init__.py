from django.utils import timezone
import calendar
from datetime import datetime, timedelta


def current_time():
    return timezone.now()

def get_last_week_of_month(year, month):
    """
    Get the last week of the given month.
    @param year:
    @param month:
    @return:
    """
    last_day_of_month = datetime(year, month, calendar.monthrange(year, month)[1])
    start_of_last_week = last_day_of_month - timedelta(days=6)
    return start_of_last_week, last_day_of_month

def get_last_time_range(month=6):
    """
    Get a list of the last time ranges for the given number of months from the current date.
    @return: list of tuples (year, month)
    """
    today = current_time()
    last_time_range = [(today.year, today.month)]

    for _ in range(month - 1):
        today = today.replace(day=1) - timedelta(days=1)
        last_time_range.append((today.year, today.month))

    return last_time_range[::-1]

__all__ = [
    'current_time',
    'get_last_week_of_month',
    'get_last_time_range'
]
