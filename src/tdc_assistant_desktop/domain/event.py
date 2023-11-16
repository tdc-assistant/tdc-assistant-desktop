from typing import TypedDict, Literal, Union

EventName = Union[Literal["chat-update"], Literal["chat-completion-ready"]]


class Event(TypedDict):
    name: EventName
