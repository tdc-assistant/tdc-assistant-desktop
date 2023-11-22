from typing import Optional

import abc

from tdc_assistant_client.client import TdcAssistantClient
from tdc_assistant_client.domain import ChatLog
from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2

from domain import Event
from tasks.fetch_most_recent_chat_log import fetch_most_recent_chat_log
from utils import log_datetime, log_timedelta


class BaseObserver(metaclass=abc.ABCMeta):
    _client: TdcAssistantClient
    _controller: TdcAssistantGuiControllerV2

    def __init__(
        self, client: TdcAssistantClient, controller: TdcAssistantGuiControllerV2
    ):
        self._client = client
        self._controller = controller

    def _fetch_most_recent_chat_log(self) -> Optional[ChatLog]:
        fetch_chat_log_start = log_datetime(
            self, "Started fetching most recent chat log"
        )

        chat_log = fetch_most_recent_chat_log(self._client)

        fetch_chat_log_end = log_datetime(
            self, "Finished fetching most recent chat log"
        )
        log_timedelta(fetch_chat_log_start, fetch_chat_log_end)

        return chat_log

    @abc.abstractmethod
    def poll(self) -> Optional[Event]:
        pass
