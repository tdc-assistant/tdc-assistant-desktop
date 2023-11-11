from typing import Optional

from tdc_assistant_client.client import TdcAssistantClient
from tdc_assistant_client.domain import ChatLog, MessageRole


def create_chat_completion_annotation(
    client: TdcAssistantClient, chat_log: ChatLog
) -> Optional[ChatLog]:
    chat_log_messages = chat_log["messages"]

    if len(chat_log_messages) == 0:
        return None

    client.create_chat_completion_annotation(message=chat_log["messages"][-1])
    return client.get_chat_log(chat_log_id=chat_log["id"])
