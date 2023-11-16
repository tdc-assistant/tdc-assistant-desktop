from tdc_assistant_client.client import TdcAssistantClient

from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2
from tdc_assistant_client.domain import ChatLog


def persist_code_editors(
    client: TdcAssistantClient,
    controller: TdcAssistantGuiControllerV2,
    chat_log: ChatLog,
):
    messages = chat_log["messages"]

    if len(messages) == 0:
        raise Exception(f"No messages exist for ChatLog: '{chat_log['id']}'")

    workspaces = chat_log["workspaces"]

    for board_number, editor in enumerate(controller.scrape_editor()):
        if board_number > len(workspaces):
            client.create_workspace(
                chat_log=chat_log,
                board_number=board_number,
                content=editor["content"],
                # FIXME
                workspace_type="CODE_EDITOR",
            )
        else:
            client.update_workspace(
                workspace=workspaces[board_number],
                content=editor["content"],
            )
