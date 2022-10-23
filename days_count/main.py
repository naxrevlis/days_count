import datetime
import logging
import os
import sys

import pika
from rocketry import Rocketry

from config import read_config_from_env

DATE_TO_MEET = datetime.date(2022, 11, 26)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

config = read_config_from_env()

app = Rocketry()


def get_days_count_from_date(date: datetime.date) -> int:
    """Return the number of days since the date."""

    today = datetime.date.today()
    return (today - date).days


def get_days_to_date(date: datetime.date) -> int:
    """Return days to date"""
    if date < datetime.date.today():
        return False
    today = datetime.date.today()
    return (date - today).days


def calculate_days(date: datetime.date, days: int) -> datetime.date:
    """Return date from date in future"""
    today = date
    return today + datetime.timedelta(days=days)


def send_message_to_queue(message: str, rmq_config) -> None:
    """Send message to queue"""
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=rmq_config["host"])
    )
    channel = connection.channel()
    channel.queue_declare(queue=rmq_config["queue"])
    channel.basic_publish(
        body=message, routing_key=rmq_config["routing_key"], exchange=""
    )
    connection.close()


def get_days_str(days: int) -> str:
    """Return days in string format with correct pluralization in Russian"""
    if days % 10 == 1 and days % 100 != 11:
        return f"{days} день"
    if days % 10 in [2, 3, 4] and days % 100 not in [12, 13, 14]:
        return f"{days} дня"
    return f"{days} дней"


def is_first_day_of_week(days: int) -> bool:
    """Return True if days is first day of week"""
    return days % 7 == 0


def get_weeks_str(weeks: int) -> str:
    """Return weeks in string format with correct pluralization in Russian"""
    if weeks % 10 == 1 and weeks % 100 != 11:
        return f"{weeks} неделя"
    if weeks % 10 in [2, 3, 4] and weeks % 100 not in [12, 13, 14]:
        return f"{weeks} недели"
    return f"{weeks} недель"


def get_hours_str(days: int) -> str:
    """Return hours in string format with correct pluralization in Russian according"""
    hours = days * 24
    if hours % 10 == 1 and hours % 100 != 11:
        return f"{hours} час"
    if hours % 10 in [2, 3, 4] and hours % 100 not in [12, 13, 14]:
        return f"{hours} часа"
    return f"{hours} часов"


@app.task("daily between 07:40 and 11:00")
def send_days_to_queue() -> None:
    """Send message to queue"""
    from_date = datetime.datetime.strptime(config["meet_date"], "%Y-%m-%d").date()
    # TODO: Поправить дату в конфиге
    days = get_days_count_from_date(from_date) - 1
    days_str = get_days_str(days)
    hours_str = get_hours_str(days)
    message = f"Уже {days_str} с момента нашей первой встречи. А ведь это {hours_str}!"
    message = str({"message": message})
    send_message_to_queue(message, config)


@app.task("daily between 07:40 and 11:00")
def send_weeks_to_queue() -> None:
    """Send message to queue"""
    from_date = datetime.datetime.strptime(config["meet_date"], "%Y-%m-%d").date()
    # TODO: Поправить дату в конфиге
    days = get_days_count_from_date(from_date) - 1
    if is_first_day_of_week(days):
        weeks = days // 7
        weeks_str = get_weeks_str(weeks)
        message = f"Сегодня +1 неделя) Мы вместе {weeks_str} !"
        message = str({"message": message})
        send_message_to_queue(message, config)


@app.task("daily between 07:40 and 11:00")
def send_days_to_meet_to_queue() -> None:
    """Send message to queue"""
    days = get_days_to_date(DATE_TO_MEET)
    if days:
        days_str = get_days_str(days)
        if days == 0:
            message = f"Я встречу тебя уже сегодня!!!"
        else:
            message = f"До встречи осталось {days_str} !"
        message = str({"message": message})
        send_message_to_queue(message, config)
    

def main() -> None:
    """Main function"""
    app.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
