from typing import Optional

from tdc_assistant_client.client import TdcAssistantClient
from tdc_assistant_client.domain import ChatLog, MessageRole

from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2
from tdc_assistant_gui_controller_v2.public_chat import PublicChat, ParticipantType

from store import load_most_recent_chat_log, update_most_recent_chat_log


def persist_chat_log(
    client: TdcAssistantClient, controller: TdcAssistantGuiControllerV2
) -> ChatLog:
    public_chat = controller.scrape_public_chat()
    most_recent_chat_log = load_most_recent_chat_log()

    # Check if a `ChatLog` for this `PublicChat` already exists
    chat_log: Optional[ChatLog] = None
    if most_recent_chat_log is not None:
        # Why do this? Instead of fetching all the chat logs, using local storage
        # allows us to fetch just a single chat log to imporove performance
        if _is_same_chat(public_chat, most_recent_chat_log):
            # `ChatLog` already exists
            chat_log = client.get_chat_log(chat_log_id=most_recent_chat_log["id"])

    if chat_log is None:
        # Could not find an existing `ChatLog` so create a new one
        optional_customer_name = _get_customer_name_from_public_chat(public_chat)
        # TODO Should be able to create a chat log without a customer name
        chat_log = client.create_chat_log(customer_name=optional_customer_name or "")

    # Persist messages from `PublicChat` to `ChatLog`
    # TODO Should be able to create messges in bulk and send messges along with
    # initial request to create a `ChatLog`
    unsaved_public_chat_messages = public_chat["messages"][len(chat_log["messages"]) :]
    chat_log_id = chat_log["id"]
    for message in unsaved_public_chat_messages:
        participant = message["participant"]
        role = _participant_type_to_message_role_map[participant["type"]]
        content = message["content"]
        client.create_message(
            chat_log_id=chat_log_id,
            role=role,
            content=content,
        )

    updated_chat_log = client.get_chat_log(chat_log_id=chat_log_id)

    # After creating chat log persist back to local store
    update_most_recent_chat_log(updated_chat_log)

    return updated_chat_log


def _is_same_chat(public_chat: PublicChat, chat_log: ChatLog) -> bool:
    public_chat_messages = public_chat["messages"]
    chat_log_messages = chat_log["messages"]

    num_public_chat_messages = len(public_chat_messages)
    num_chat_log_messages = len(chat_log_messages)

    # If they are from the same chat, then the number of messages scraped from
    # the public chat will never exceed the number of messages saved to the chat log
    is_valid_message_count = num_public_chat_messages <= num_chat_log_messages
    if not is_valid_message_count:
        return False

    # Check that the content from each message saved in the chat log is the same
    # as the content scraped from the public chat
    for i in range(num_public_chat_messages):
        public_chat_message = public_chat_messages[i]
        chat_log_message = chat_log_messages[i]

        if public_chat_message["content"] != chat_log_message["content"]:
            return False

    return True


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
