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

    def poll(self) -> Optional[Event]:
        chat_log = super()._fetch_most_recent_chat_log()

        if chat_log is None:
            return None

        most_recent_approved_chat_completion = (
            find_most_recent_approved_chat_completion(chat_log)
        )

        if most_recent_approved_chat_completion is None:
            return None

        if most_recent_approved_chat_completion["sentAt"] is None:
            return {"name": "chat-completion-ready"}

        return None
