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

        # (2) Find most recent chat completion

        chat_completions = chat_log["chatCompletions"]

        if len(chat_completions) > 0:
            last_chat_completion = chat_completions[-1]
            unsent_chat_completion_parts = [
                p for p in last_chat_completion["parts"] if p["sentAt"] is None
            ]
            if len(unsent_chat_completion_parts) > 0:
                return {"name": "chat-completion-ready"}

        return None
