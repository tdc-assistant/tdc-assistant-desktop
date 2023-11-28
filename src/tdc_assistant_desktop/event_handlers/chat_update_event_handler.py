from typing import List

from time import sleep

from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2

from tdc_assistant_client.client import TdcAssistantClient
from tdc_assistant_client.domain import ChatLog, Message

from tasks import (
    persist_chat_log_messages,
    persist_code_editors,
    create_chat_completion_annotation,
)

from logger import Logger
from domain import Event

from .base_event_handler import BaseEventHandler
from utils import get_prescripted_message, PRESCRIPTED_MESSAGES


class ChatUpdateEventHandler(BaseEventHandler):
    def __init__(
        self, client: TdcAssistantClient, controller: TdcAssistantGuiControllerV2
    ):
        super().__init__(client, controller)

    def _get_tutor_messages_from_chat_log(self, chat_log: ChatLog) -> List[Message]:
        return [m for m in chat_log["messages"] if m["role"] == "assistant"]

    def _create_chat_completion(self, chat_log: ChatLog):
        create_chat_completion_start = self._logger.log(
            "Started creating chat completion"
        )

        chat_completion = self._client.create_chat_completion(chat_log=chat_log)

        create_chat_completion_end = self._logger.log(
            "Finished creating chat completion"
        )
        self._logger.log_elapsed_time(
            create_chat_completion_start, create_chat_completion_end
        )

        if chat_completion is None:
            print("Failed to create chat completion")
            return None

        for part in chat_completion["parts"]:
            print(f'[{part["type"]}]')
            print(part["content"])
            print()

        # should_send = input("Send chat completion (y/[N])? ").strip().lower() == "y"
        # if not should_send:
        #     return None

        # should_send = True
        # sleep(3)

        # approve_chat_completion_annotation_start = self._logger.log(
        #     "Started approving chat completion annotation"
        # )

        # TODO Need to add something like this back in to approve the chat completion

        # self._client.update_chat_completion_annotation(
        #     chat_completion_annotation=chat_completion_annotation,
        #     sent_at=None,
        #     approval_status="APPROVED",
        # )

        # approve_chat_completion_annotation_end = self._logger.log(
        #     "Finished approving chat completion annotation"
        # )
        # self._logger.log_elapsed_time(
        #     approve_chat_completion_annotation_start,
        #     approve_chat_completion_annotation_end,
        # )

    def _handle(self, event: Event):
        persist_chat_log_start = self._logger.log("Started persisting chat log")

        chat_log = persist_chat_log_messages(self._client, self._controller)

        persist_chat_log_end = self._logger.log("Finished persisting chat log")
        self._logger.log_elapsed_time(persist_chat_log_start, persist_chat_log_end)

        persist_code_editors_start = self._logger.log("Started persisting code editors")

        persist_code_editors(self._client, self._controller, chat_log)

        persist_code_editors_end = self._logger.log("Finished persisting code editors")
        self._logger.log_elapsed_time(
            persist_code_editors_start, persist_code_editors_end
        )

        num_tutor_messages = len(self._get_tutor_messages_from_chat_log(chat_log))
        should_send_prescripted_message = num_tutor_messages < len(PRESCRIPTED_MESSAGES)

        if should_send_prescripted_message:
            self._controller.send_message(get_prescripted_message(num_tutor_messages))
        else:
            self._create_chat_completion(chat_log)
