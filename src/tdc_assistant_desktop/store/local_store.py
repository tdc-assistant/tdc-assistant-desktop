from typing import Optional, Final

import os
from os.path import join, dirname
import json

from tdc_assistant_client.domain import ChatLog


FILENAME_LOCAL_STORE_CHAT_LOGS: Final[str] = "chat_logs.json"
LOGS_PATH = join(dirname(__file__), "..", "..", "..", "logs")
FILEPATH_LOCAL_STORE_CHAT_LOGS: Final[str] = os.path.join(
    LOGS_PATH, FILENAME_LOCAL_STORE_CHAT_LOGS
)


def load_chat_log_ids() -> list[str]:
    # TODO Need to check if file/path exists first
    chat_logs: list[str] = []
    if os.path.isfile(FILEPATH_LOCAL_STORE_CHAT_LOGS):
        with open(FILEPATH_LOCAL_STORE_CHAT_LOGS, "r") as f:
            chat_logs = json.loads(f.read())

    return chat_logs


def load_most_recent_chat_log_id() -> Optional[str]:
    chat_log_ids = load_chat_log_ids()

    if len(chat_log_ids) == 0:
        return None

    return chat_log_ids[-1]


def update_chat_log_ids(chat_log_id: str) -> None:
    os.makedirs(LOGS_PATH, exist_ok=True)

    chat_log_ids = load_chat_log_ids()

    with open(FILEPATH_LOCAL_STORE_CHAT_LOGS, "w") as f:
        f.write(
            json.dumps(
                chat_log_ids + [chat_log_id], indent=4, sort_keys=True, default=str
            )
        )
