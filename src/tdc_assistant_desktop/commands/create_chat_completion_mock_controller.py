from pprint import pprint

from time import sleep

from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2
from tdc_assistant_client.client import TdcAssistantClient


def create_chat_completion_mock_controller(
    client: TdcAssistantClient, controller: TdcAssistantGuiControllerV2
):
    chat_log_before = client.create_chat_log(customer_name="Demo", raw_text="")
    chat_log_before = client.get_chat_log(
        chat_log_id="0d1ef06a-7db4-4197-bcb0-4306c8059dca"
    )
    # client.create_messages(
    #     messages=[
    #         {
    #             "chat_log_id": chat_log_before["id"],
    #             "content": "Hello there!",
    #             "role": "user",
    #         }
    #     ]
    # )
    chat_completion = client.create_chat_completion(chat_log=chat_log_before)
    print(chat_completion)
    chat_completion = client.get_chat_log(chat_log_id=chat_log_before["id"])[
        "chatCompletions"
    ][-1]

    while True:
        try:
            result = client.request_chat_completion_approval(
                chat_completion=chat_completion
            )
            break
        except:
            print("Retrying....")
            sleep(5)
    pprint(result)
