import datetime

from days_count import __version__
from days_count.main import (calculate_days, get_days_count_from_date, get_days_str,
                             get_hours_str, get_month_str, send_message_to_queue)


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
    assert get_hours_str(1) == "1 час"
    assert get_hours_str(2) == "2 часа"
    assert get_hours_str(5) == "5 часов"
    assert get_hours_str(11) == "11 часов"
    assert get_hours_str(21) == "21 час"
    assert get_hours_str(22) == "22 часа"
    assert get_hours_str(25) == "25 часов"


def test_month_str():
    assert get_month_str(1) == "1 месяц"
    assert get_month_str(2) == "2 месяца"
    assert get_month_str(5) == "5 месяцев"
    assert get_month_str(11) == "11 месяцев"
    assert get_month_str(21) == "21 месяц"
    assert get_month_str(22) == "22 месяца"
    assert get_month_str(25) == "25 месяцев"


def test_days_str():
    assert get_days_str(1) == "1 день"
    assert get_days_str(2) == "2 дня"
    assert get_days_str(5) == "5 дней"
    assert get_days_str(11) == "11 дней"
    assert get_days_str(21) == "21 день"
    assert get_days_str(22) == "22 дня"
    assert get_days_str(25) == "25 дней"
