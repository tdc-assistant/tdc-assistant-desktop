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


def load_chat_logs() -> list[ChatLog]:
    # TODO Need to check if file/path exists first
    chat_logs: list[ChatLog] = []
    if os.path.isfile(FILEPATH_LOCAL_STORE_CHAT_LOGS):
        with open(FILEPATH_LOCAL_STORE_CHAT_LOGS, "r") as f:
            chat_logs = json.loads(f.read())

    return chat_logs


def load_most_recent_chat_log() -> Optional[ChatLog]:
    chat_logs = load_chat_logs()

    if len(chat_logs) == 0:
        return None

    return chat_logs[-1]


def update_chat_logs(chat_logs: list[ChatLog]) -> None:
    os.makedirs(LOGS_PATH, exist_ok=True)

    with open(FILEPATH_LOCAL_STORE_CHAT_LOGS, "w") as f:
        f.write(json.dumps(chat_logs, indent=4, sort_keys=True, default=str))


def update_most_recent_chat_log(chat_log: ChatLog) -> None:
    chat_logs = load_chat_logs()
    most_recent_chat_log = chat_logs[-1]

    if most_recent_chat_log["id"] != chat_log["id"]:
        update_chat_logs(chat_logs + [chat_log])
    else:
        update_chat_logs(chat_logs[:-1] + [chat_log])
