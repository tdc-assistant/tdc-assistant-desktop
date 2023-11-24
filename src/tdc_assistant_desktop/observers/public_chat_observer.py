from typing import Optional

from tdc_assistant_client.client import TdcAssistantClient
from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2

from utils import is_same_chat

from domain import Event

from .base_observer import BaseObserver


class PublicChatObserver(BaseObserver):
    _client: TdcAssistantClient
    _controller: TdcAssistantGuiControllerV2

    def __init__(
        self, client: TdcAssistantClient, controller: TdcAssistantGuiControllerV2
    ):
        super().__init__(client, controller)

    def poll(self) -> Optional[Event]:
        chat_log = self._fetch_most_recent_chat_log()

        if chat_log is None:
            return {"name": "chat-update"}

        scrape_public_chat_start = self._logger.log("Started scraping public chat")

        public_chat = self._controller.scrape_public_chat()

        scrape_public_chat_end = self._logger.log("Finished scraping public chat")
        self._logger.log_elapsed_time(scrape_public_chat_start, scrape_public_chat_end)

        # Only create a "chat-update" event if the last message was sent by the student
        messages = public_chat["messages"]
        if len(messages) == 0:
            return None

        most_recent_message = messages[-1]
        if most_recent_message["participant"]["type"] != "student":
            return None

        if not is_same_chat(public_chat, chat_log):
            return {"name": "chat-update"}

        return None
