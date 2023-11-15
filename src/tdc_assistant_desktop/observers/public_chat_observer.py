from typing import Optional

from datetime import datetime

from tdc_assistant_client.client import TdcAssistantClient
from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2

from events import ChatUpdateEvent

from tasks.fetch_most_recent_chat_log import fetch_most_recent_chat_log
from utils import is_same_chat

from config import config
from .base_observer import BaseObserver


class PublicChatObserver(BaseObserver):
    _client: TdcAssistantClient
    _controller: TdcAssistantGuiControllerV2

    def __init__(
        self, client: TdcAssistantClient, controller: TdcAssistantGuiControllerV2
    ):
        self._client = client
        self._controller = controller

    def poll(self) -> Optional[ChatUpdateEvent]:
        fetch_chat_log_start = datetime.now()
        if config["LOG"]:
            self._log("Start fetching most recent chat log", fetch_chat_log_start)

        chat_log = fetch_most_recent_chat_log(self._client)

        fetch_chat_log_end = datetime.now()
        if config["LOG"]:
            self._log("Finished fetching most recent chat log", fetch_chat_log_end)
            print(f"Elapsed time: {fetch_chat_log_end - fetch_chat_log_start}")

        if chat_log is None:
            return {"name": "chat_update_event"}

        scrape_public_chat_start = datetime.now()
        if config["LOG"]:
            self._log("Start scraping public chat", scrape_public_chat_start)

        public_chat = self._controller.scrape_public_chat()

        scrape_public_chat_end = datetime.now()
        if config["LOG"]:
            self._log("Finished scraping public chat", scrape_public_chat_end)
            print(f"Elapsed time: {scrape_public_chat_end - scrape_public_chat_start}")

        if not is_same_chat(public_chat, chat_log):
            return {"name": "chat_update_event"}

        return None
