from typing import Optional

from tdc_assistant_client.client import TdcAssistantClient
from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2

from tasks.fetch_most_recent_chat_log import fetch_most_recent_chat_log
from utils import is_same_chat

from utils import log_datetime, log_timedelta
from domain import Event


class PublicChatObserver:
    _client: TdcAssistantClient
    _controller: TdcAssistantGuiControllerV2

    def __init__(
        self, client: TdcAssistantClient, controller: TdcAssistantGuiControllerV2
    ):
        self._client = client
        self._controller = controller

    def poll(self) -> Optional[Event]:
        fetch_chat_log_start = log_datetime(
            self, "Started fetching most recent chat log"
        )

        chat_log = fetch_most_recent_chat_log(self._client)

        fetch_chat_log_end = log_datetime(
            self, "Finished fetching most recent chat log"
        )
        log_timedelta(fetch_chat_log_start, fetch_chat_log_end)

        if chat_log is None:
            return {"name": "chat-update"}

        scrape_public_chat_start = log_datetime(self, "Started scraping public chat")

        public_chat = self._controller.scrape_public_chat()

        scrape_public_chat_end = log_datetime(self, "Finished scraping public chat")
        log_timedelta(scrape_public_chat_start, scrape_public_chat_end)

        if not is_same_chat(public_chat, chat_log):
            return {"name": "chat-update"}

        return None
