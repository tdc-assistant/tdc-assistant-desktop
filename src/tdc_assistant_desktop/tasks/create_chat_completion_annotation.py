from typing import Optional

from tdc_assistant_client.client import TdcAssistantClient
from tdc_assistant_client.domain import ChatLog, ChatCompletionAnnotation


def create_chat_completion_annotation(
    client: TdcAssistantClient, chat_log: ChatLog
) -> Optional[ChatCompletionAnnotation]:
    chat_log_messages = chat_log["messages"]

    if len(chat_log_messages) == 0:
        return None

    return client.create_chat_completion(chat_log=chat_log)
