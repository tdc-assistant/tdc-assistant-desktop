from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2
from tdc_assistant_client.client import TdcAssistantClient
from domain import Event

from .base_event_handler import BaseEventHandler


class CodeEditorsUpdateEventHandler(BaseEventHandler):
    def __init__(
        self, client: TdcAssistantClient, controller: TdcAssistantGuiControllerV2
    ):
        super().__init__(client, controller)

    def handle(self, event: Event):
        payload = event.get("payload")

        if payload is None or not isinstance(payload, dict):
            return None

        chat_log = payload["chat_log"]
        editors_to_create = payload["editors_to_create"]
        editors_to_update = payload["editors_to_update"]

        for editor_to_create in editors_to_create:
            self._client.create_code_editor(
                chat_log=chat_log,
                programming_language=editor_to_create["editor_language"],
                editor_number=editor_to_create["editor_number"],
                content=editor_to_create["content"],
            )

        for editor_to_update in editors_to_update:
            self._client.update_code_editor(
                code_editor=editor_to_update["code_editor"],
                content=editor_to_update["new_content"],
            )
