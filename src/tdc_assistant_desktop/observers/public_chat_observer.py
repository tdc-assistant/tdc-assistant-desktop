from typing import Optional

from tdc_assistant_client.client import TdcAssistantClient
from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2

from events import ChatUpdateEvent

from tasks.fetch_most_recent_chat_log import fetch_most_recent_chat_log
from utils import is_same_chat


class PublicChatObserver:
    _client: TdcAssistantClient
    _controller: TdcAssistantGuiControllerV2

    def __init__(
        self, client: TdcAssistantClient, controller: TdcAssistantGuiControllerV2
    ):
        self._client = client
        self._controller = controller

    def poll(self) -> Optional[ChatUpdateEvent]:
        chat_log = fetch_most_recent_chat_log(self._client)

        if chat_log is None or not is_same_chat(
            self._controller.scrape_public_chat(), chat_log
        ):
            return {"name": "chat_update_event"}

        return None
