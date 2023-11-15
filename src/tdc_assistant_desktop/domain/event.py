from typing import TypedDict, Literal

EventName = Literal["chat-update"]


class Event(TypedDict):
    name: EventName
