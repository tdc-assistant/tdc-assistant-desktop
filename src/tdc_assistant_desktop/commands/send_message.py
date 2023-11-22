from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2
from tdc_assistant_client.client import TdcAssistantClient


def send_message(client: TdcAssistantClient, controller: TdcAssistantGuiControllerV2):
    controller.send_message("Hello world!")
