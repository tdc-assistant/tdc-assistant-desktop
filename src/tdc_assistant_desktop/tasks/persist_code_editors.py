from tdc_assistant_client.client import TdcAssistantClient

from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2
from tdc_assistant_client.domain import ChatLog

from .fetch_most_recent_chat_log import fetch_most_recent_chat_log


def persist_code_editors(
    client: TdcAssistantClient,
    controller: TdcAssistantGuiControllerV2,
    chat_log: ChatLog,
):
    messages = chat_log["messages"]

    if len(messages) == 0:
        raise Exception(f"No messages exist for ChatLog: '{chat_log['id']}'")

    for board_number, editor in enumerate(controller.scrape_editor()):
        client.create_workspace_annotation(
            message=messages[-1],
            content=editor["content"],
            board_number=board_number,
        )
