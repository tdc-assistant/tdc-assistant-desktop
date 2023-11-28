from tdc_assistant_client.domain import ChatLog
from tdc_assistant_gui_controller_v2.public_chat import PublicChat


def is_same_chat(public_chat: PublicChat, chat_log: ChatLog) -> bool:
    raw_text_controller = public_chat["raw_text"]
    raw_text_client = chat_log["rawText"]

    raw_text_client_len = len(raw_text_client)
    raw_text_controller_len = len(raw_text_controller)
    if raw_text_client_len > raw_text_controller_len:
        return False

    # Why? Because the messages added to the raw text are added at the front,
    # not at the end, which is the opposite of how you would expect it to work.
    return raw_text_client == raw_text_controller[-raw_text_client_len:]
