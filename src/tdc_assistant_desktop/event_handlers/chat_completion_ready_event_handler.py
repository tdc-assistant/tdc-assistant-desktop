from time import sleep
from datetime import datetime, timezone

from random import randint

from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2

from tdc_assistant_client.client import TdcAssistantClient

from utils import find_most_recent_approved_chat_completion
from tasks import fetch_most_recent_chat_log


class ChatCompletionReadyEventHandler:
    _client: TdcAssistantClient
    _controller: TdcAssistantGuiControllerV2

    def __init__(
        self, client: TdcAssistantClient, controller: TdcAssistantGuiControllerV2
    ):
        self._client = client
        self._controller = controller

    def handle(self):
        chat_log = fetch_most_recent_chat_log(self._client)

        if chat_log is None:
            return

        chat_completion_annotation = find_most_recent_approved_chat_completion(chat_log)

        if chat_completion_annotation is None:
            return

        chat_completion = chat_completion_annotation["chatCompletion"]
        if chat_completion is None:
            return None

        for part in chat_completion["parts"]:
            if part["type"] == "CONVERSATION":
                self._controller.send_message(
                    {"component": "code editor", "content": part["content"]}
                )
                sleep(randint(10, 25))

        self._client.update_chat_completion_annotation(
            chat_completion_annotation=chat_completion_annotation,
            sent_at=datetime.now(timezone.utc),
            approval_status="APPROVED",
        )
