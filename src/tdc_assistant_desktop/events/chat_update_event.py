from typing import TypedDict, Literal


class ChatUpdateEvent(TypedDict):
    name: Literal["chat_update_event"]
