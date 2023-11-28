from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2
from tdc_assistant_client.client import TdcAssistantClient

from tasks import fetch_most_recent_chat_log

from domain import Event

from .base_event_handler import BaseEventHandler


class ScreenshareUpdateEventHandler(BaseEventHandler):
    def __init__(
        self, client: TdcAssistantClient, controller: TdcAssistantGuiControllerV2
    ):
        super().__init__(client, controller)

    def _handle(self, event: Event):
        chat_log = fetch_most_recent_chat_log(self._client)

        if chat_log is None:
            return

        # TODO Should do something here so a new screenshare capture is generate for every message

        screenshare = self._controller.scrape_screenshare()
        if screenshare is not None:
            self._client.create_image_capture(
                chat_log=chat_log,
                type="SCREENSHARE",
                image_url=screenshare["image_url"],
            )
