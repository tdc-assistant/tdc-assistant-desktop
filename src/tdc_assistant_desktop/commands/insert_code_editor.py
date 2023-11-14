from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2
from tdc_assistant_client.client import TdcAssistantClient


def insert_code_editor(
    client: TdcAssistantClient, controller: TdcAssistantGuiControllerV2
):
    controller.insert_code_editor()
