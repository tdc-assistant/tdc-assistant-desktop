from observers import PublicChatObserver

from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2
from tdc_assistant_client.client import TdcAssistantClient


def run(client: TdcAssistantClient, controller: TdcAssistantGuiControllerV2) -> None:
    public_chat_observer = PublicChatObserver(client, controller)

    while True:
        public_chat_observer.poll()
