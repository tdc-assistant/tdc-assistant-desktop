from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2
from tdc_assistant_client.client import TdcAssistantClient


def end_session(client: TdcAssistantClient, controller: TdcAssistantGuiControllerV2):
    controller.end_session()
