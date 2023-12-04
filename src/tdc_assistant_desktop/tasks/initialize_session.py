from typing import Optional

from datetime import datetime

from tdc_assistant_client.client import TdcAssistantClient
from tdc_assistant_client.domain import ChatLog
from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2
from tdc_assistant_gui_controller_v2.public_chat import PublicChat

from utils import is_same_chat

from .base_task import BaseTask


class InitializeSession(BaseTask):
    def __init__(
        self, client: TdcAssistantClient, controller: TdcAssistantGuiControllerV2
    ):
        super().__init__(client, controller)

    def _get_time_since_last_update(self, chat_log: ChatLog) -> datetime:
        return datetime.now()

    def _get_customer_name_from_public_chat(
        self, public_chat: PublicChat
    ) -> Optional[str]:
        for message in public_chat["messages"]:
            participant = message["participant"]
            if participant["type"] == "student":
                return participant["name"]

        return None

    def _execute(self, chat_log: Optional[ChatLog]) -> ChatLog:
        public_chat = self._controller.scrape_public_chat()
        if chat_log is not None and is_same_chat(public_chat, chat_log):
            return chat_log

        customer_name = self._get_customer_name_from_public_chat(public_chat)
        return self._client.create_chat_log(
            customer_name=customer_name or "", raw_text=public_chat["raw_text"]
        )
