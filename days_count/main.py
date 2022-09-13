import datetime
import logging
import os
import sys

import pika
from rocketry import Rocketry

from config import read_config_from_env

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


def get_hours_str(days: int) -> str:
    """Return hours in string format with correct pluralization in Russian according"""
    if days % 10 == 1 and days % 100 != 11:
        return f"{days} час"
    if days % 10 in [2, 3, 4] and days % 100 not in [12, 13, 14]:
        return f"{days} часа"
    return f"{days} часов"


def get_month_str(days: int) -> str:
    """Return month in string format with correct pluralization in Russian"""
    if days % 10 == 1 and days % 100 != 11:
        return f"{days} месяц"
    if days % 10 in [2, 3, 4] and days % 100 not in [12, 13, 14]:
        return f"{days} месяца"
    return f"{days} месяцев"


@app.task("daily on 10:00")
def send_days_to_queue() -> None:
    """Send message to queue"""
    from_date = datetime.datetime.strptime(config["meet_date"], "%Y-%m-%d").date()
    days = get_days_count_from_date(from_date)
    days_str = get_days_str(days)
    hours_str = get_hours_str(days)
    month_str = get_month_str(days)
    message = f"Прошло {days_str} с момента нашей первой встречи. А еще это {hours_str} и {month_str}!"
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
