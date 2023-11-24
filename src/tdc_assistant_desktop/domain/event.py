from typing import TypedDict, Literal, Union

from tdc_assistant_client.domain import ChatLog

from .update_editor_payload import UpdateCodeEditorPayload
from .create_code_editor_payload import CreateCodeEditorPayload


class ChatUpdateEvent(TypedDict):
    name: Literal["chat-update"]


class ChatCompletionReadyEvent(TypedDict):
    name: Literal["chat-completion-ready"]


class ScreenshareUpdateEvent(TypedDict):
    name: Literal["screenshare-update"]


class UpdateEditorsEventPayload(TypedDict):
    chat_log: ChatLog
    editors_to_update: list[UpdateCodeEditorPayload]
    editors_to_create: list[CreateCodeEditorPayload]


class UpdateEditorsEvent(TypedDict):
    name: Literal["editors-update"]
    payload: UpdateEditorsEventPayload


Event = Union[
    ChatUpdateEvent,
    ChatCompletionReadyEvent,
    ScreenshareUpdateEvent,
    UpdateEditorsEvent,
]
