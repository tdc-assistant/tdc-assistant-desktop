from typing import Union

from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2
from tdc_assistant_client.client import TdcAssistantClient

from domain import EventName
from observers import PublicChatObserver, ChatCompletionReadyObserver
from event_handlers import ChatUpdateEventHandler, ChatCompletionReadyEventHandler


def run(client: TdcAssistantClient, controller: TdcAssistantGuiControllerV2) -> None:
    observers = [
        PublicChatObserver(client, controller),
        ChatCompletionReadyObserver(client, controller),
    ]
    event_handlers: dict[
        EventName, list[Union[ChatUpdateEventHandler, ChatCompletionReadyEventHandler]]
    ] = {
        "chat-update": [ChatUpdateEventHandler(client, controller)],
        "chat-completion-ready": [ChatCompletionReadyEventHandler(client, controller)],
    }

    while True:
        for observer in observers:
            event = observer.poll()
            if event is not None:
                for event_handler in event_handlers[event["name"]]:
                    event_handler.handle()
