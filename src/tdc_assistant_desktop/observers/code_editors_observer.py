from typing import Optional, Any

from tdc_assistant_client.client import TdcAssistantClient
from tdc_assistant_client.domain import CodeEditor
from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2

from .base_observer import BaseObserver

from domain import UpdateEditorsEvent, UpdateCodeEditorPayload


class CodeEditorsObserver(BaseObserver):
    _client: TdcAssistantClient
    _controller: TdcAssistantGuiControllerV2

    def __init__(
        self, client: TdcAssistantClient, controller: TdcAssistantGuiControllerV2
    ):
        super().__init__(client, controller)

    def _poll(self) -> Optional[UpdateEditorsEvent]:
        chat_log = self._fetch_most_recent_chat_log()

        if chat_log is None:
            return None

        code_editors_from_controller = self._controller.scrape_editor()

        code_editors_from_client = [
            w for w in chat_log["workspaces"] if w["type"] == "CODE_EDITOR"
        ]

        editors_to_update: list[UpdateCodeEditorPayload] = []
        editors_to_create: list[Any] = []

        for ccef in code_editors_from_controller:
            for ccec in code_editors_from_client:
                found_editor = (
                    ccef["editor_language"] == ccec["programmingLanguage"]
                    and ccef["editor_number"] == ccec["editorNumber"]
                )
                if found_editor:
                    if ccef["content"] != ccec["content"]:
                        editors_to_update.append(
                            {"code_editor": ccec, "new_content": ccec["content"]}
                        )
                        break
            else:
                editors_to_create.append(
                    {
                        "editor_language": ccef["editor_language"],
                        "editor_number": ccef["editor_number"],
                        "content": ccef["content"],
                    }
                )

        if len(editors_to_update) > 0 or len(editors_to_create) > 0:
            return {
                "name": "editors-update",
                "payload": {
                    "chat_log": chat_log,
                    "editors_to_create": editors_to_create,
                    "editors_to_update": editors_to_update,
                },
            }

        return None
