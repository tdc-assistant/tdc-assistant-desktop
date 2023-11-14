from typing import Optional

from tdc_assistant_client.client import TdcAssistantClient
from tdc_assistant_client.domain import ChatLog

from store import load_most_recent_chat_log_id


def fetch_most_recent_chat_log(client: TdcAssistantClient) -> Optional[ChatLog]:
    chat_log_id = load_most_recent_chat_log_id()

    if chat_log_id is not None:
        return client.get_chat_log(chat_log_id=chat_log_id)

    chat_logs = client.get_chat_logs()
    if len(chat_logs) > 0:
        return chat_logs[-1]

    return None
