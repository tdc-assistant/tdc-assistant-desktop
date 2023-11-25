from typing import Optional

from tdc_assistant_client.client import TdcAssistantClient
from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2

from domain import Event
from utils import find_most_recent_approved_chat_completion

from .base_observer import BaseObserver


class ChatCompletionReadyObserver(BaseObserver):
    def __init__(
        self, client: TdcAssistantClient, controller: TdcAssistantGuiControllerV2
    ):
        super().__init__(client, controller)

    def _poll(self) -> Optional[Event]:
        # (1) Fetch most recent chat log
        chat_log = super()._fetch_most_recent_chat_log()

        if chat_log is None:
            return None

        # (2) Find most recently approved chat completion

        most_recent_chat_completion_start = self._logger.log(
            "Started finding most recent chat completion"
        )
        most_recent_approved_chat_completion = (
            find_most_recent_approved_chat_completion(chat_log)
        )
        most_recent_chat_completion_end = self._logger.log(
            "Finished finding most recent chat completion"
        )
        self._logger.log_elapsed_time(
            most_recent_chat_completion_start, most_recent_chat_completion_end
        )

        if most_recent_approved_chat_completion is None:
            return None

        if most_recent_approved_chat_completion["sentAt"] is None:
            return {"name": "chat-completion-ready"}

        return None
