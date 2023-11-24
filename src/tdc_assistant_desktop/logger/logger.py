from datetime import datetime

from termcolor import colored

from utils.constants import DATETIME_TIME_FORMAT


class Logger:
    def __init__(self, o: object):
        self._o = o

    def _get_class_field(self) -> str:
        return colored("{:30s}".format(f"[{self._o.__class__.__name__}]"), "green")

    def _get_message_field(self, message: str) -> str:
        return colored("{:50s}".format(message), "white")

    def _get_datetime_field(self, dt: datetime) -> str:
        return colored(
            "({})".format(dt.strftime(DATETIME_TIME_FORMAT)),
            "yellow",
        )

    def _get_warning_message(self, message: str) -> str:
        return colored("{:50s}".format(message), "red")

    def _get_fields(self, message: str, dt: datetime) -> list[str]:
        return [
            self._get_class_field(),
            self._get_message_field(message),
            self._get_datetime_field(dt),
        ]

    def log(self, message: str):
        dt = datetime.now()
        print(" ".join(self._get_fields(message, dt)))
        return dt

    def log_elapsed_time(self, start: datetime, end: datetime):
        elapsed_time = end - start
        print(
            colored(
                f"Elapsed time: {elapsed_time.total_seconds()}",
                "cyan",
            ),
        )

    def log_warning(self, message: str):
        print(" ".join([self._get_class_field(), self._get_warning_message(message)]))
