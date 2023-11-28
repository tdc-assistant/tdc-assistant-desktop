from typing import Optional

from datetime import datetime, timezone, timedelta

from tdc_assistant_client.client import TdcAssistantClient
from tdc_assistant_client.domain import ImageCapture
from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2

from domain import Event

from .base_observer import BaseObserver


IMAGE_CAPTURE_INTERVAL_IN_MINUTES = 3


class ScreenshareObserver(BaseObserver):
    _client: TdcAssistantClient
    _controller: TdcAssistantGuiControllerV2

    def __init__(
        self, client: TdcAssistantClient, controller: TdcAssistantGuiControllerV2
    ):
        super().__init__(client, controller)

    def _fetch_most_recent_image_capture(
        self,
    ) -> Optional[ImageCapture]:
        chat_log = self._fetch_most_recent_chat_log()

        if chat_log is None:
            return None

        screenshare_image_captures = [
            ic for ic in chat_log["imageCaptures"] if ic["type"] == "SCREENSHARE"
        ]

        if len(screenshare_image_captures) > 0:
            return screenshare_image_captures[-1]

        return None

    def _poll(self) -> Optional[Event]:
        """
        Generates a "screenshare-update" event when either
        (1) The screenshare window is visible and no image capture exists
        (2) Enough time has passed between now and the last image capture that was created
        """
        if not self._controller.is_screenshare_window_open():
            return None

        most_recent_image_capture = self._fetch_most_recent_image_capture()

        if most_recent_image_capture is None:
            # Screenshare window is open but an image capture has not been created yet
            return {"name": "screenshare-update"}

        should_update_screenshare = most_recent_image_capture[
            "createdAt"
        ] < datetime.now(timezone.utc) - timedelta(
            minutes=IMAGE_CAPTURE_INTERVAL_IN_MINUTES
        )

        if should_update_screenshare:
            # Enough time has passed since the last image capture
            return {"name": "screenshare-update"}

        return None
