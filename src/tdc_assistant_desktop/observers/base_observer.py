from typing import Optional

import abc

from tdc_assistant_client.client import TdcAssistantClient
from tdc_assistant_client.domain import ChatLog
from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2

from domain import Event
from tasks.fetch_most_recent_chat_log import fetch_most_recent_chat_log
from logger import Logger


class BaseObserver(metaclass=abc.ABCMeta):
    _client: TdcAssistantClient
    _controller: TdcAssistantGuiControllerV2
    _logger: Logger

    def __init__(
        self, client: TdcAssistantClient, controller: TdcAssistantGuiControllerV2
    ):
        self._client = client
        self._controller = controller
        self._logger = Logger(self)

    def _fetch_most_recent_chat_log(self) -> Optional[ChatLog]:
        fetch_chat_log_start = self._logger.log("Started fetching most recent chat log")

        chat_log = fetch_most_recent_chat_log(self._client)

        fetch_chat_log_end = self._logger.log("Finished fetching most recent chat log")
        self._logger.log_elapsed_time(fetch_chat_log_start, fetch_chat_log_end)

        return chat_log

    @abc.abstractmethod
    def _poll(self) -> Optional[Event]:
        pass

    def poll(self) -> Optional[Event]:
        start = self._logger.log("Started")
        result = self.poll()
        end = self._logger.log("Finished")
        self._logger.log_elapsed_time(start, end)
        return result
