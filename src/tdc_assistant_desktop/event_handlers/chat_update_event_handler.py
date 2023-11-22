from time import sleep

from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2

from tdc_assistant_client.client import TdcAssistantClient

from tasks import (
    persist_chat_log,
    persist_code_editors,
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

        persist_code_editors_start = log_datetime(
            self, "Started persisting code editors"
        )

        persist_code_editors(self._client, self._controller, chat_log)

        persist_code_editors_end = log_datetime(
            self, "Finished persisting code editors"
        )
        log_timedelta(persist_code_editors_start, persist_code_editors_end)

        create_chat_completion_start = log_datetime(
            self, "Started creating chat completion"
        )

        chat_completion_annotation = create_chat_completion_annotation(
            self._client, chat_log
        )

        create_chat_completion_end = log_datetime(
            self, "Finished creating chat completion"
        )
        log_timedelta(create_chat_completion_start, create_chat_completion_end)

        if chat_completion_annotation is None:
            print("Failed to create chat completion creation")
            return None

        chat_completion = chat_completion_annotation["chatCompletion"]
        if chat_completion is None:
            return

        for part in chat_completion["parts"]:
            print(f'[{part["type"]}]')
            print(part["content"])
            print()

        # should_send = input("Send chat completion (y/[N])? ").strip().lower() == "y"
        # if not should_send:
        #     return None

        should_send = True
        sleep(3)

        approve_chat_completion_annotation_start = log_datetime(
            self, "Started approving chat completion annotation"
        )

        # TODO Add something here to prompt user to approve
        # Should be conditional based on env var

        self._client.update_chat_completion_annotation(
            chat_completion_annotation=chat_completion_annotation,
            sent_at=None,
            approval_status="APPROVED",
        )

        approve_chat_completion_annotation_end = log_datetime(
            self, "Finished approving chat completion annotation"
        )
        log_timedelta(
            approve_chat_completion_annotation_start,
            approve_chat_completion_annotation_end,
        )
