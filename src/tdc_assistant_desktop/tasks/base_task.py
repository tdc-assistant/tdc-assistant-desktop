from typing import Optional

import abc

from datetime import datetime, timezone, timedelta

from tdc_assistant_client.client import TdcAssistantClient
from tdc_assistant_client.domain import ChatLog
from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2

from domain import ChatLog
from logger import Logger


class BaseTask(metaclass=abc.ABCMeta):
    _client: TdcAssistantClient
    _controller: TdcAssistantGuiControllerV2
    _logger: Logger
    _interval_between_execution_in_seconds: Optional[float]

    def __init__(
        self,
        client: TdcAssistantClient,
        controller: TdcAssistantGuiControllerV2,
        interval_between_execution_in_seconds: Optional[float] = None,
    ):
        self._client = client
        self._controller = controller
        self._logger = Logger(self)
        self._interval_between_execution_in_seconds = (
            interval_between_execution_in_seconds
        )

    @abc.abstractmethod
    def _execute(self, chat_log: Optional[ChatLog]) -> ChatLog:
        pass

    @abc.abstractmethod
    def _get_time_since_last_update(self, chat_log: ChatLog) -> datetime:
        pass

    def execute(self, chat_log: Optional[ChatLog]) -> ChatLog:
        if (
            self._interval_between_execution_in_seconds is not None
            and chat_log is not None
        ):
            if self._get_time_since_last_update(chat_log) >= datetime.now(
                timezone.utc
            ) - timedelta(seconds=self._interval_between_execution_in_seconds):
                return chat_log  # type: ignore

        start = self._logger.log("Started")
        result = self._execute(chat_log)
        end = self._logger.log("Finished")
        self._logger.log_elapsed_time(start, end)
        return result
