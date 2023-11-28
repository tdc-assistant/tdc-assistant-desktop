from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2
from tdc_assistant_client.client import TdcAssistantClient


def create_chat_completion_mock_controller(
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
    client.create_chat_completion(chat_log=chat_log_before)
    chat_log_after = client.get_chat_log(chat_log_id=chat_log_before["id"])
    print(chat_log_after)
