from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2
from tdc_assistant_client.client import TdcAssistantClient
from tdc_assistant_client.domain import Message

from tasks import fetch_most_recent_chat_log

from domain import Event


class ScreenshareUpdateEventHandler:
    _client: TdcAssistantClient
    _controller: TdcAssistantGuiControllerV2

    def __init__(
        self, client: TdcAssistantClient, controller: TdcAssistantGuiControllerV2
    ):
        self._client = client
        self._controller = controller

    def handle(self, event: Event):
        chat_log = fetch_most_recent_chat_log(self._client)

        if chat_log is None:
            return

        for message in reversed(chat_log["messages"]):
            if message["role"] == "user":
                self._create_image_capture_for_message(message)
                return

    def _create_image_capture_for_message(self, message: Message):
        screenshare = self._controller.scrape_screenshare()

        if screenshare is not None:
            self._client.create_image_capture_annotation(
                message=message, image_url=screenshare["image_url"]
            )