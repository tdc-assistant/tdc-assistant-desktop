from typing import Optional

from datetime import datetime, timezone

from tdc_assistant_client.client import TdcAssistantClient
from tdc_assistant_client.domain import ChatLog
from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2

from .base_task import BaseTask


class CheckWordProcessorTask(BaseTask):
    def __init__(
        self,
        client: TdcAssistantClient,
        controller: TdcAssistantGuiControllerV2,
        interval_between_execution_in_seconds: Optional[float] = None,
    ):
        super().__init__(client, controller, interval_between_execution_in_seconds)

    def _get_time_since_last_update(self, chat_log: ChatLog) -> datetime:
        times = [
            w["updatedAt"] or w["createdAt"]
            for w in chat_log["workspaces"]
            if w["type"] == "WORD_PROCESSOR"
        ]

        if len(times) == 0:
            return datetime.now()
        return min(times)

    def _execute(self, chat_log: Optional[ChatLog]) -> ChatLog:
        if chat_log is None:
            raise Exception()

        word_processors_from_controller = self._controller.scrape_word_processors()

        word_processors_from_client = [
            w for w in chat_log["workspaces"] if w["type"] == "WORD_PROCESSOR"
        ]

        for wp_controller in word_processors_from_controller:
            for wp_client in word_processors_from_client:
                found_editor = wp_controller["number"] == wp_client["number"]
                if found_editor:
                    if wp_controller["content"] != wp_client["content"]:
                        self._client.update_word_processor(
                            word_processor=wp_client, content=wp_controller["content"]
                        )
                        break
            else:
                self._client.create_word_processor(
                    chat_log=chat_log,
                    number=wp_controller["number"],
                    content=wp_controller["content"],
                )

        return self._client.get_chat_log(chat_log_id=chat_log["id"])
