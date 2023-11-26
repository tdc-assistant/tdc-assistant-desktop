from time import sleep
from datetime import datetime, timezone

from random import randint

from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2

from tdc_assistant_client.client import TdcAssistantClient

from utils import find_most_recent_approved_chat_completion
from tasks import fetch_most_recent_chat_log

from domain import Event

from .base_event_handler import BaseEventHandler


class ChatCompletionReadyEventHandler(BaseEventHandler):
    def __init__(
        self, client: TdcAssistantClient, controller: TdcAssistantGuiControllerV2
    ):
        super().__init__(client, controller)

    def _handle(self, event: Event):
        chat_log = fetch_most_recent_chat_log(self._client)

        if chat_log is None:
            return

        chat_completion_annotation = find_most_recent_approved_chat_completion(chat_log)

        if chat_completion_annotation is None:
            return

        chat_completion = chat_completion_annotation["chatCompletion"]
        if chat_completion is None:
            return None

        # Before responding check if any code part is present if so then check if there is an available code editor
        # to write in .. if there is not then add a new code editor and use that

        is_code_part_present = (
            len([p for p in chat_completion["parts"] if p["type"] == "CODE"]) > 0
        )

        active_code_language = "Java"
        active_code_editor_number = 1
        if is_code_part_present:
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

        for part in chat_completion["parts"]:
            if part["type"] == "CONVERSATION":
                self._controller.send_message(part["content"])

            else:
                self._controller.send_text_to_code_editor(
                    editor_language=active_code_language,
                    editor_number=active_code_editor_number,
                    text=part["content"],
                )
            sleep(randint(10, 25))

        self._client.update_chat_completion_annotation(
            chat_completion_annotation=chat_completion_annotation,
            sent_at=datetime.now(timezone.utc),
            approval_status="APPROVED",
        )
