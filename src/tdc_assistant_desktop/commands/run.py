from typing import Union

from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2
from tdc_assistant_client.client import TdcAssistantClient

from observers import (
    PublicChatObserver,
    ChatCompletionReadyObserver,
    CodeEditorsObserver,
    ScreenshareObserver,
    WordProcessorsObserver,
)
from event_handlers import (
    ChatUpdateEventHandler,
    ChatCompletionReadyEventHandler,
    ScreenshareUpdateEventHandler,
    CodeEditorsUpdateEventHandler,
    WordProcessorsUpdateEventHandler,
)


def run(client: TdcAssistantClient, controller: TdcAssistantGuiControllerV2) -> None:
    observers = [
        PublicChatObserver(client, controller),
        ChatCompletionReadyObserver(client, controller),
        CodeEditorsObserver(client, controller),
        ScreenshareObserver(client, controller),
        WordProcessorsObserver(client, controller),
    ]
    event_handlers: dict[
        str,
        list[
            Union[
                ChatUpdateEventHandler,
                ChatCompletionReadyEventHandler,
                ScreenshareUpdateEventHandler,
                CodeEditorsUpdateEventHandler,
                WordProcessorsUpdateEventHandler,
            ]
        ],
    ] = {
        "chat-update": [ChatUpdateEventHandler(client, controller)],
        "chat-completion-ready": [ChatCompletionReadyEventHandler(client, controller)],
        "screenshare-update": [ScreenshareUpdateEventHandler(client, controller)],
        "editors-update": [CodeEditorsUpdateEventHandler(client, controller)],
        "word-processors-update": [
            WordProcessorsUpdateEventHandler(client, controller)
        ],
    }

    while True:
        for observer in observers:
            event = observer.poll()
            if event is not None:
                for event_handler in event_handlers[event["name"]]:
                    event_handler.handle(event)
