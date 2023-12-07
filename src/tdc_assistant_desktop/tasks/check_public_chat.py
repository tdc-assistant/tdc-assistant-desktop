from typing import Optional

from datetime import datetime, timezone
from time import sleep

from tdc_assistant_client.client import TdcAssistantClient
from tdc_assistant_client.domain import ChatLog, MessageRole, ChatCompletion
from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2
from tdc_assistant_gui_controller_v2.public_chat import (
    PublicChat,
    PublicChatMessage,
    ParticipantType,
)

from utils import get_prescripted_message, PRESCRIPTED_MESSAGES

from .base_task import BaseTask


_participant_type_to_message_role_map: dict[ParticipantType, MessageRole] = {
    "student": "user",
    "classroom": "system",
    "tutor": "assistant",
}


class CheckPublicChat(BaseTask):
    def __init__(
        self, client: TdcAssistantClient, controller: TdcAssistantGuiControllerV2
    ):
        super().__init__(client, controller)

    def _get_time_since_last_update(self, chat_log: ChatLog) -> datetime:
        return datetime.now()

    def _is_last_message_from_student(self, public_chat: PublicChat) -> bool:
        messages = public_chat["messages"]

        if len(messages) == 0:
            return False

        return messages[-1]["participant"]["type"] == "student"

    def _find_most_recent_approved_chat_completion(
        self,
        chat_log: ChatLog,
    ) -> Optional[ChatCompletion]:
        chat_completions = chat_log["chatCompletions"]

        if len(chat_completions) > 0:
            last_chat_completion = chat_completions[-1]
            if last_chat_completion["approvalStatus"] != "APPROVED":
                return None
            unsent_chat_completion_parts = [
                p for p in last_chat_completion["parts"] if p["sentAt"] is None
            ]
            if len(unsent_chat_completion_parts) > 0:
                return last_chat_completion

        return None

    def _has_unsent_chat_completion_part(self, chat_log: ChatLog) -> bool:
        return self._find_most_recent_approved_chat_completion(chat_log) is not None

    def _persist_public_chat(
        self, chat_log: ChatLog, public_chat: PublicChat
    ) -> ChatLog:
        self._client.create_messages(
            messages=[
                {
                    "chat_log_id": chat_log["id"],
                    "content": message["content"],
                    "role": _participant_type_to_message_role_map[
                        message["participant"]["type"]
                    ],
                }
                for message in public_chat["messages"]
            ]
        )
        return self._client.get_chat_log(chat_log_id=chat_log["id"])

    def _create_chat_completion(self, chat_log: ChatLog) -> ChatCompletion:
        while True:
            chat_completion = self._client.create_chat_completion(chat_log=chat_log)

            if chat_completion is None:
                print("Failed to create chat completion")
                continue

            for part in chat_completion["parts"]:
                print(f'[{part["type"]}]')
                print(part["content"])
                print()

            while True:
                try:
                    chat_completion = self._client.request_chat_completion_approval(
                        chat_completion=chat_completion
                    )
                    approval_status = chat_completion["approvalStatus"]
                    if approval_status == "APPROVED":
                        return chat_completion
                    elif approval_status == "DECLINED":
                        break
                except:
                    print("Retrying chat completion approval....")
                    sleep(5)

    def _handle_chat_completion(self, chat_log: ChatLog) -> ChatLog:
        unsent_chat_completion_parts = [
            p for p in chat_log["chatCompletions"][-1]["parts"] if p["sentAt"] is None
        ]

        chat_completion_part = unsent_chat_completion_parts[0]

        active_code_language = "Java"
        active_code_editor_number = 1
        if chat_completion_part["type"] == "CODE":
            code_editors = [
                ce for ce in chat_log["workspaces"] if ce["type"] == "CODE_EDITOR"
            ]
            if len(code_editors) > 0:
                code_editors.sort(key=lambda x: x["createdAt"], reverse=True)
                active_code_language = code_editors[0]["programmingLanguage"]
                active_code_editor_number = code_editors[0]["editorNumber"]
            else:
                # TODO Have this add a language other than Java and `insert_code_editor` should return the language and number
                self._controller.insert_code_editor()

        if chat_completion_part["type"] == "CONVERSATION":
            self._controller.send_message(chat_completion_part["content"])

        else:
            self._controller.send_text_to_code_editor(
                editor_language=active_code_language,
                editor_number=active_code_editor_number,
                text=chat_completion_part["content"],
            )

        self._client.update_chat_completion_part(
            chat_completion_part=chat_completion_part,
            sent_at=datetime.now(timezone.utc),
            should_omit=None,
        )

        return self._client.get_chat_log(chat_log_id=chat_log["id"])

    def _get_tutor_messages_from_public_chat(
        self, public_chat: PublicChat
    ) -> list[PublicChatMessage]:
        return [
            m for m in public_chat["messages"] if m["participant"]["type"] == "tutor"
        ]

    def _should_send_prescripted_message(self, public_chat: PublicChat) -> bool:
        return len(self._get_tutor_messages_from_public_chat(public_chat)) < len(
            PRESCRIPTED_MESSAGES
        )

    def _send_prescripted_message(self, public_chat: PublicChat) -> None:
        self._controller.send_message(
            get_prescripted_message(
                len(self._get_tutor_messages_from_public_chat(public_chat))
            )
        )

    def _execute(self, chat_log: Optional[ChatLog]) -> ChatLog:
        if chat_log is None:
            raise Exception()

        public_chat = self._controller.scrape_public_chat()

        # Check for the following...
        # 1. Was the student the last person to send a message?
        # Important to do this first so that messages from a previous chat completion are no longer
        # sent in order to create a new chat completion that addresses the student's most previous message
        if (
            self._is_last_message_from_student(public_chat)
            or len(self._get_tutor_messages_from_public_chat(public_chat)) == 0
        ):
            if self._should_send_prescripted_message(public_chat):
                self._send_prescripted_message(public_chat)
            else:
                chat_log = self._persist_public_chat(chat_log, public_chat)
                self._create_chat_completion(chat_log)
                chat_log = self._client.get_chat_log(chat_log_id=chat_log["id"])

        # 2. Is there a chat completion part that has not been sent yet?
        if self._has_unsent_chat_completion_part(chat_log):
            chat_log = self._handle_chat_completion(chat_log)

        # TODO
        # 2. Has too much time past since the last message and the tutor should send a message
        #    to check on the student?
        # 3. Should randomly send a messsage from time to time to make it seem more human?

        return chat_log
