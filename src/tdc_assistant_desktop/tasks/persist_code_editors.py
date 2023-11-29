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

    code_editors_from_client = [
        w for w in chat_log["workspaces"] if w["type"] == "CODE_EDITOR"
    ]

    for controller_editor in controller.scrape_editor():
        for client_editor in code_editors_from_client:
            if (
                client_editor["programmingLanguage"]
                == controller_editor["editor_language"]
                and client_editor["editorNumber"]
                == controller_editor["editor_language"]
            ):
                # FIXME This should only update editors whose content differs
                client.update_code_editor(
                    code_editor=client_editor, content=controller_editor["content"]
                )

        else:
            client.create_code_editor(
                chat_log=chat_log,
                editor_number=controller_editor["editor_number"],
                programming_language=controller_editor["editor_language"],
                content=controller_editor["content"],
            )
