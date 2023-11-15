from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2

from tdc_assistant_client.client import TdcAssistantClient

from tasks import (
    persist_chat_log,
    create_chat_completion_annotation,
)

from utils import log_datetime, log_timedelta


class ChatUpdateEventHandler:
    _client: TdcAssistantClient
    _controller: TdcAssistantGuiControllerV2

    def __init__(
        self, client: TdcAssistantClient, controller: TdcAssistantGuiControllerV2
    ):
        self._client = client
        self._controller = controller

    def handle(self):
        persist_chat_log_start = log_datetime(self, "Started persisting chat log")

        chat_log = persist_chat_log(self._client, self._controller)

        persist_chat_log_end = log_datetime(self, "Finished persisting chat log")
        log_timedelta(persist_chat_log_start, persist_chat_log_end)

        create_chat_completion_start = log_datetime(
            self, "Started creating chat completion"
        )

        create_chat_completion_annotation(self._client, chat_log)

        create_chat_completion_end = log_datetime(
            self, "Finished creating chat completion"
        )
        log_timedelta(create_chat_completion_start, create_chat_completion_end)
