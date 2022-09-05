import datetime
from rocketry import Rocketry
import logging
import pika
from days_count.config import read_config_from_env
import os
import sys

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


config = read_config_from_env()

app = Rocketry()


def days_count_from_date(date: datetime.date) -> int:
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
    channel.basic_publish(body=message, routing_key=rmq_config["routing_key"], exchange="")
    connection.close()


@app.task("daily between 08:00 and 10:00")
def send_days_to_queue() -> None:
    """Send message to queue"""
    from_date = datetime.datetime.strptime(config["meet_date"], "%Y-%m-%d").date()
    days = days_count_from_date(from_date)
    message = str({"days_since_first_meet": days})
    print(message)
    send_message_to_queue(message, config)


def main() -> None:
    """Main function"""
    app.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

