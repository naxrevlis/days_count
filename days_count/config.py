import os
from dotenv import load_dotenv


def read_config_from_env():
    """Read .env file to json"""
    load_dotenv()
    return {
        "host": os.getenv("RMQ_HOST"),
        "port": os.getenv("RMQ_PORT"),
        "user": os.getenv("RMQ_USER"),
        "password": os.getenv("RMQ_PASSWORD"),
        "exchange": os.getenv("RMQ_EXCHANGE"),
        "queue": os.getenv("RMQ_QUEUE"),
        "routing_key": os.getenv("RMQ_ROUTING_KEY"),
        "first_date": os.getenv("FIRST_DATE"),
        "meet_date": os.getenv("MEET_DATE"),
    }


def main():
    print(read_config_from_env())


if __name__ == "__main__":
    main()
