from tdc_assistant_client.domain import ChatLog
from tdc_assistant_gui_controller_v2.public_chat import PublicChat


def is_same_chat(public_chat: PublicChat, chat_log: ChatLog) -> bool:
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
