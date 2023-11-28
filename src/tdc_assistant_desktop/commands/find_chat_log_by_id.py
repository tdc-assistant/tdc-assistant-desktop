from pprint import pprint

from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2
from tdc_assistant_client.client import TdcAssistantClient


def find_chat_log_by_id(
    client: TdcAssistantClient, controller: TdcAssistantGuiControllerV2
):
    chat_log_id = input("Enter chat log id: ")
    result = client.get_chat_log(chat_log_id=chat_log_id)
    pprint(result)
