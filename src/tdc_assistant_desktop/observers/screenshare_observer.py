from typing import Optional

from datetime import datetime, timezone, timedelta

from tdc_assistant_client.client import TdcAssistantClient
from tdc_assistant_client.domain import ImageCaptureAnnotation
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

    def _fetch_most_recent_image_capture_annotation(
        self,
    ) -> Optional[ImageCaptureAnnotation]:
        chat_log = self._fetch_most_recent_chat_log()

        if chat_log is None:
            return None

        for message in reversed(chat_log["messages"]):
            for annotation in reversed(message["annotations"]):
                if annotation["type"] == "IMAGE_CAPTURE":
                    return annotation

        return None

    def _poll(self) -> Optional[Event]:
        """
        Generates a "screenshare-update" event when either
        (1) The screenshare window is visible and no image capture exists
        (2) Enough time has passed between now and the last image capture that was created
        """
        if not self._controller.is_screenshare_window_open():
            return None

        most_recent_image_capture_annotation = (
            self._fetch_most_recent_image_capture_annotation()
        )
        print(
            "most_recent_image_capture_annotation", most_recent_image_capture_annotation
        )

        if most_recent_image_capture_annotation is None:
            # Screenshare window is open but an image capture has not been created yet
            return {"name": "screenshare-update"}

        should_update_screenshare = most_recent_image_capture_annotation[
            "createdAt"
        ] < datetime.now(timezone.utc) - timedelta(
            minutes=IMAGE_CAPTURE_INTERVAL_IN_MINUTES
        )

        if should_update_screenshare:
            # Enough time has passed since the last image capture
            return {"name": "screenshare-update"}

        return None
