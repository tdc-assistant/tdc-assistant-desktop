from typing import Optional

from datetime import datetime, timezone

from tdc_assistant_client.client import TdcAssistantClient
from tdc_assistant_client.domain import ChatLog
from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2

from .base_task import BaseTask


class CheckScreenshareTask(BaseTask):
    def __init__(
        self,
        client: TdcAssistantClient,
        controller: TdcAssistantGuiControllerV2,
        interval_between_execution_in_seconds: Optional[float] = None,
    ):
        super().__init__(client, controller, interval_between_execution_in_seconds)

    def _get_time_since_last_update(self, chat_log: ChatLog) -> datetime:
        times = [
            ic["updatedAt"] or ic["createdAt"]
            for ic in chat_log["imageCaptures"]
            if ic["type"] == "SCREENSHARE"
        ]

        if len(times) == 0:
            return datetime.now(timezone.utc)
        return max(times)

    def _execute(self, chat_log: Optional[ChatLog]) -> ChatLog:
        if chat_log is None:
            raise Exception()

        screenshare = self._controller.scrape_screenshare()
        if screenshare is not None:
            self._client.create_image_capture(
                chat_log=chat_log,
                type="SCREENSHARE",
                image_url=screenshare["image_url"],
            )

        return self._client.get_chat_log(chat_log_id=chat_log["id"])
