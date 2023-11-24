from typing import TypedDict, Literal, Union

from tdc_assistant_client.domain import ChatLog, CodeEditor, WordProcessor

from .update_editor_payload import UpdateCodeEditorPayload
from .update_word_processor_payload import UpdateWordProcessorPayload


class ChatUpdateEvent(TypedDict):
    name: Literal["chat-update"]


class ChatCompletionReadyEvent(TypedDict):
    name: Literal["chat-completion-ready"]


class ScreenshareUpdateEvent(TypedDict):
    name: Literal["screenshare-update"]


class UpdateEditorsEventPayload(TypedDict):
    chat_log: ChatLog
    editors_to_update: list[UpdateCodeEditorPayload]
    editors_to_create: list[CodeEditor]


class UpdateEditorsEvent(TypedDict):
    name: Literal["editors-update"]
    payload: UpdateEditorsEventPayload


class UpdateWordProcessorEventPayload(TypedDict):
    chat_log: ChatLog
    word_processors_to_update: list[UpdateWordProcessorPayload]
    word_processors_to_create: list[WordProcessor]


class UpdateWordProcessorsEvent(TypedDict):
    name: Literal["word-processors-update"]
    payload: UpdateWordProcessorEventPayload


Event = Union[
    ChatUpdateEvent,
    ChatCompletionReadyEvent,
    ScreenshareUpdateEvent,
    UpdateEditorsEvent,
    UpdateWordProcessorsEvent,
]
