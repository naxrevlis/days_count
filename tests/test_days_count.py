from days_count import __version__
from days_count.main import days_count_from_date, calculate_days
import datetime


def test_version():
    assert __version__ == "0.1.0"


def test_days_count_from_date():
    assert days_count_from_date(datetime.date.today()) == 0


def test_calculate_days():
    assert calculate_days(
        datetime.date.today(), 444
    ) == datetime.date.today() + datetime.timedelta(days=444)
    assert calculate_days(datetime.date.today(), 0) == datetime.date.today()
