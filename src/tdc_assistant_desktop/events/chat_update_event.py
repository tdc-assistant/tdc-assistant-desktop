from .base_event import BaseEvent, Literal


class ChatUpdateEvent(BaseEvent):
    name: Literal["chat_update_event"]
