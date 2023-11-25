from typing import Optional

import abc

from tdc_assistant_client.client import TdcAssistantClient
from tdc_assistant_client.domain import ChatLog
from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2

from domain import Event
from logger import Logger


class BaseEventHandler(metaclass=abc.ABCMeta):
    _client: TdcAssistantClient
    _controller: TdcAssistantGuiControllerV2
    _logger: Logger

    def __init__(
        self, client: TdcAssistantClient, controller: TdcAssistantGuiControllerV2
    ):
        self._client = client
        self._controller = controller
        self._logger = Logger(self)

    @abc.abstractmethod
    def _handle(self, event: Event) -> None:
        pass

    def handle(self, event: Event) -> None:
        start = self._logger.log("Started")
        result = self._handle(event)
        end = self._logger.log("Finished")
        self._logger.log_elapsed_time(start, end)
        return result
