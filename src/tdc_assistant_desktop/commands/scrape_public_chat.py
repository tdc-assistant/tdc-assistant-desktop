from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2
from tdc_assistant_client.client import TdcAssistantClient


def scrape_public_chat(
    client: TdcAssistantClient, controller: TdcAssistantGuiControllerV2
):
    result = controller.scrape_public_chat()
    print(result)
