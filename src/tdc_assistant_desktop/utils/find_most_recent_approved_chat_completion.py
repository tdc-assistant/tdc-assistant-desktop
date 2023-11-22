from typing import Optional

from tdc_assistant_client.domain import ChatLog, ChatCompletionAnnotation


def find_most_recent_approved_chat_completion(
    chat_log: ChatLog,
) -> Optional[ChatCompletionAnnotation]:
    for message in reversed(chat_log["messages"]):
        for annotation in reversed(message["annotations"]):
            if annotation["type"] == "CHAT_COMPLETION":
                if annotation["approvalStatus"] == "APPROVED":
                    return annotation
                    # Only send the last approved chat completion
                return None
    return None
