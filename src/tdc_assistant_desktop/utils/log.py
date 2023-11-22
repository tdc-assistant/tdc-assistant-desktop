from datetime import datetime

from termcolor import colored

from config import config
from utils.constants import DATETIME_TIME_FORMAT


def log_datetime(o: object, message: str) -> datetime:
    dt = datetime.now()
    if config["LOG"]:
        print(
            " ".join(
                [
                    colored("{:30s}".format(f"[{o.__class__.__name__}]"), "green"),
                    colored("{:50s}".format(message), "white"),
                    colored(
                        "({})".format(dt.strftime(DATETIME_TIME_FORMAT)),
                        "yellow",
                    ),
                ]
            )
        )
    return dt


def log_timedelta(start: datetime, end: datetime):
    if config["LOG"]:
        elapsed_time = end - start
        print(
            colored(
                f"Elapsed time: {elapsed_time.total_seconds()}",
                "cyan",
            ),
        )
