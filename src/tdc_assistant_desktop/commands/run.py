from observers import PublicChatObserver

from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2
from tdc_assistant_client.client import TdcAssistantClient

from events import Event


def run(client: TdcAssistantClient, controller: TdcAssistantGuiControllerV2) -> None:
    observers = [PublicChatObserver(client, controller)]
    events: list[Event] = []

    while True:
        for observer in observers:
            event = observer.poll()
            if event is not None:
                events.append(event)
