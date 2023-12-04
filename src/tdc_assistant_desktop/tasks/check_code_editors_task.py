from typing import Optional

from datetime import datetime, timezone
from time import sleep

from tdc_assistant_client.client import TdcAssistantClient
from tdc_assistant_client.domain import ChatLog, MessageRole, ChatCompletion
from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2
from tdc_assistant_gui_controller_v2.public_chat import PublicChat, ParticipantType

from .base_task import BaseTask


class CheckCodeEditorsTask(BaseTask):
    def __init__(
        self,
        client: TdcAssistantClient,
        controller: TdcAssistantGuiControllerV2,
        interval_between_execution_in_seconds: Optional[float] = None,
    ):
        super().__init__(client, controller, interval_between_execution_in_seconds)

    def _get_time_since_last_update(self, chat_log: ChatLog) -> Optional[datetime]:
        times = [
            w["updatedAt"] or w["createdAt"]
            for w in chat_log["workspaces"]
            if w["type"] == "CODE_EDITOR"
        ]

        if len(times) == 0:
            return None
        return min(times)

    def _execute(self, chat_log: Optional[ChatLog]) -> ChatLog:
        if chat_log is None:
            raise Exception()

        code_editors_from_controller = self._controller.scrape_editor()

        code_editors_from_client = [
            w for w in chat_log["workspaces"] if w["type"] == "CODE_EDITOR"
        ]

        for ccef in code_editors_from_controller:
            for ccec in code_editors_from_client:
                found_editor = (
                    ccef["editor_language"] == ccec["programmingLanguage"]
                    and ccef["editor_number"] == ccec["editorNumber"]
                )
                if found_editor:
                    if ccef["content"] != ccec["content"]:
                        self._client.update_code_editor(
                            code_editor=ccec, content=ccec["content"]
                        )
                        break
            else:
                self._client.create_code_editor(
                    chat_log=chat_log,
                    programming_language=ccef["editor_language"],
                    editor_number=ccef["editor_number"],
                    content=ccef["content"],
                )

        return self._client.get_chat_log(chat_log_id=chat_log["id"])
