from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2
from tdc_assistant_client.client import TdcAssistantClient

from domain import EventName
from observers import PublicChatObserver
from event_handlers import ChatUpdateEventHandler


def run(client: TdcAssistantClient, controller: TdcAssistantGuiControllerV2) -> None:
    observers = [PublicChatObserver(client, controller)]
    event_handlers: dict[EventName, list[ChatUpdateEventHandler]] = {
        "chat-update": [ChatUpdateEventHandler(client, controller)]
    }

    while True:
        for observer in observers:
            event = observer.poll()
            if event is not None:
                for event_handler in event_handlers[event["name"]]:
                    event_handler.handle()
