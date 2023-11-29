from pprint import pprint

from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2
from tdc_assistant_client.client import TdcAssistantClient


def request_chat_completion_approval(
    client: TdcAssistantClient, controller: TdcAssistantGuiControllerV2
):
    chat_log_before = client.create_chat_log(customer_name="Demo", raw_text="")
    client.create_messages(
        messages=[
            {
                "chat_log_id": chat_log_before["id"],
                "content": "Hello there!",
                "role": "user",
            }
        ]
    )
    chat_completion = client.create_chat_completion(chat_log=chat_log_before)
    pprint(chat_completion)
    client.request_chat_completion_approval(chat_completion=chat_completion)
    chat_log_after = client.get_chat_log(chat_log_id=chat_log_before["id"])
    pprint(chat_log_after)
