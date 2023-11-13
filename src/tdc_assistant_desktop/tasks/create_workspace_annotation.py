from tdc_assistant_client.client import TdcAssistantClient
from tdc_assistant_client.domain import ChatLog

from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2
from tdc_assistant_gui_controller_v2.scrape_editors import Editor

from store import load_most_recent_chat_log, update_most_recent_chat_log


def create_workspace_annotation(
    client: TdcAssistantClient,
    controller: TdcAssistantGuiControllerV2,
    editor_cache: list[Editor],
):
    most_recent_chat_log = load_most_recent_chat_log()

    if most_recent_chat_log is None:
        return

    if len(most_recent_chat_log["messages"]) == 0:
        return

    messages = most_recent_chat_log["messages"]

    controller.scrape_editor(editor_cache)

    for i, editor in enumerate(editor_cache):
        client.create_workspace_annotation(
            message=messages[-1],
            content=editor["content"],
            board_number=i + 1,
        )

    update_most_recent_chat_log(most_recent_chat_log)
