from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2

from tdc_assistant_client.client import TdcAssistantClient

from tasks import (
    persist_chat_log,
    persist_code_editors,
    create_chat_completion_annotation,
)

PERSIST_CODE_EDITOR_MSG = "Do you want to scrape the code editors (y/N)? "


def create_chat_completion(
    client: TdcAssistantClient,
    controller: TdcAssistantGuiControllerV2,
):
    should_persist_code_editors = input(PERSIST_CODE_EDITOR_MSG).lower().strip() == "y"
    chat_log = persist_chat_log(client, controller)

    if should_persist_code_editors:
        persist_code_editors(client, controller, chat_log)

    create_chat_completion_annotation(client, chat_log)
