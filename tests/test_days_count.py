import datetime

from days_count import __version__
from days_count.main import (
    calculate_days,
    get_days_count_from_date,
    get_days_str,
    get_hours_str,
    get_weeks_str,
    is_first_day_of_week,
)


def test_version():
    assert __version__ == "0.1.0"


def test_days_count_from_date():
    assert get_days_count_from_date(datetime.date.today()) == 0


def test_calculate_days():
    assert calculate_days(
        datetime.date.today(), 444
    ) == datetime.date.today() + datetime.timedelta(days=444)
    assert calculate_days(datetime.date.today(), 0) == datetime.date.today()


def test_get_hours_str():
    assert get_hours_str(1) == "24 часа"
    assert get_hours_str(2) == "48 часов"
    assert get_hours_str(5) == "120 часов"
    assert get_hours_str(11) == "264 часа"
    assert get_hours_str(21) == "504 часа"
    assert get_hours_str(22) == "528 часов"
    assert get_hours_str(25) == "600 часов"


def test_get_days_str():
    assert get_days_str(1) == "1 день"
    assert get_days_str(2) == "2 дня"
    assert get_days_str(5) == "5 дней"
    assert get_days_str(11) == "11 дней"
    assert get_days_str(21) == "21 день"
    assert get_days_str(22) == "22 дня"
    assert get_days_str(25) == "25 дней"


def test_get_weeks_str():
    assert get_weeks_str(1) == "1 неделя"
    assert get_weeks_str(2) == "2 недели"
    assert get_weeks_str(5) == "5 недель"
    assert get_weeks_str(11) == "11 недель"
    assert get_weeks_str(21) == "21 неделя"
    assert get_weeks_str(22) == "22 недели"
    assert get_weeks_str(25) == "25 недель"


def test_is_first_day_of_week():
    assert is_first_day_of_week(7) is True
    assert is_first_day_of_week(14) is True
    assert is_first_day_of_week(6) is False
