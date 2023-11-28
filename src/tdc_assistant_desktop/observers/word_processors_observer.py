from typing import Any

from tdc_assistant_client.client import TdcAssistantClient
from tdc_assistant_client.domain import WordProcessor
from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2

from .base_observer import BaseObserver

from domain import UpdateWordProcessorPayload


class WordProcessorsObserver(BaseObserver):
    _client: TdcAssistantClient
    _controller: TdcAssistantGuiControllerV2

    def __init__(
        self, client: TdcAssistantClient, controller: TdcAssistantGuiControllerV2
    ):
        super().__init__(client, controller)

    def _poll(self):
        chat_log = self._fetch_most_recent_chat_log()

        if chat_log is None:
            return None

        word_processors_from_controller = self._controller.scrape_word_processors()

        word_processors_from_client = [
            w for w in chat_log["workspaces"] if w["type"] == "WORD_PROCESSOR"
        ]

        word_processors_to_update: list[UpdateWordProcessorPayload] = []
        word_processors_to_create: list[Any] = []

        for wp_controller in word_processors_from_controller:
            for wp_client in word_processors_from_client:
                found_editor = wp_controller["number"] == wp_client["number"]
                if found_editor:
                    if wp_controller["content"] != wp_client["content"]:
                        word_processors_to_update.append(
                            {
                                "word_processor": wp_client,
                                "new_content": wp_client["content"],
                            }
                        )
                        break
            else:
                word_processors_to_create.append(
                    {
                        "number": wp_controller["number"],
                        "content": wp_controller["content"],
                    }
                )

        if len(word_processors_to_update) > 0 or len(word_processors_to_create) > 0:
            return {
                "name": "word-processors-update",
                "payload": {
                    "chat_log": chat_log,
                    "editors_to_create": word_processors_to_create,
                    "editors_to_update": word_processors_to_update,
                },
            }

        return None
