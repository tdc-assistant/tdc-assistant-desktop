from typing import Optional

from tdc_assistant_client.domain import ChatLog, ChatCompletion


def find_most_recent_approved_chat_completion(
    chat_log: ChatLog,
) -> Optional[ChatCompletion]:
    # TODO Need to add an approved field
    chat_completions = chat_log["chatCompletions"]

    if len(chat_completions) > 0:
        last_chat_completion = chat_completions[-1]
        unsent_chat_completion_parts = [
            p for p in last_chat_completion["parts"] if p["sentAt"] is None
        ]
        if len(unsent_chat_completion_parts) > 0:
            return last_chat_completion

    return None
