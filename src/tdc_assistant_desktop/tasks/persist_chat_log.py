from typing import Optional

from tdc_assistant_client.client import TdcAssistantClient
from tdc_assistant_client.domain import ChatLog, MessageRole

from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2
from tdc_assistant_gui_controller_v2.public_chat import PublicChat, ParticipantType

from store import update_chat_log_ids
from .fetch_most_recent_chat_log import fetch_most_recent_chat_log

from utils import is_same_chat


def persist_chat_log_messages(
    client: TdcAssistantClient, controller: TdcAssistantGuiControllerV2
) -> ChatLog:
    public_chat = controller.scrape_public_chat()
    chat_log = fetch_most_recent_chat_log(client)

    if chat_log is None or not is_same_chat(public_chat, chat_log):
        # TODO Should be able to create a chat log without a customer name
        optional_customer_name = _get_customer_name_from_public_chat(public_chat)
        chat_log = client.create_chat_log(
            customer_name=optional_customer_name or "", raw_text=public_chat["raw_text"]
        )
        update_chat_log_ids(chat_log_id=chat_log["id"])

    client.create_messages(
        messages=[
            {
                "chat_log_id": chat_log["id"],
                "content": m["content"],
                "role": _participant_type_to_message_role_map[m["participant"]["type"]],
            }
            for m in public_chat["messages"]
        ]
    )

    return client.get_chat_log(chat_log_id=chat_log["id"])


def _get_customer_name_from_public_chat(public_chat: PublicChat) -> Optional[str]:
    for message in public_chat["messages"]:
        participant = message["participant"]
        if participant["type"] == "student":
            return participant["name"]

    return None


_participant_type_to_message_role_map: dict[ParticipantType, MessageRole] = {
    "student": "user",
    "classroom": "system",
    "tutor": "assistant",
}
