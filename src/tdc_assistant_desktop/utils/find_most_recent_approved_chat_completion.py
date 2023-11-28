from typing import Optional

from tdc_assistant_client.domain import ChatLog, ChatCompletion


def find_most_recent_approved_chat_completion(
    chat_log: ChatLog,
) -> Optional[ChatCompletion]:
    # TODO Need to add an approved field
    chat_completions = chat_log["chatCompletions"]

    if len(chat_completions) > 0:
        last_chat_completion = chat_completions[-1]
        last_chat_completion_has_been_sent = last_chat_completion["sentAt"] is not None
        if not last_chat_completion_has_been_sent:
            return last_chat_completion

    return None
