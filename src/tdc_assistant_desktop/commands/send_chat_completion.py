from typing import Optional

from random import randint
from time import sleep

from tdc_assistant_client.client import TdcAssistantClient
from tdc_assistant_client.domain import ChatCompletion
from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2

from tasks import fetch_most_recent_chat_log


def send_chat_completion(
    client: TdcAssistantClient,
    controller: TdcAssistantGuiControllerV2,
):
    most_recent_chat_log = fetch_most_recent_chat_log(client)
    if most_recent_chat_log is None:
        raise Exception("No chat logs exist")

    chat_completion_to_send: Optional[ChatCompletion] = None
    for message in reversed(most_recent_chat_log["messages"]):
        for annotation in reversed(message["annotations"]):
            if annotation["type"] == "CHAT_COMPLETION":
                chat_completion = annotation["chatCompletion"]
                if chat_completion is None:
                    print("Awaiting chat completion")
                else:
                    chat_completion_to_send = chat_completion
                    break

    if chat_completion_to_send is None:
        print("Chat completion not found")
        return

    for part in chat_completion_to_send["parts"]:
        print(f'[{part["type"]}]')
        print(part["content"])
        print()

    should_send = input("Send chat completion (y/[N])? ").strip().lower() == "y"
    if not should_send:
        return

    for part in chat_completion_to_send["parts"]:
        if part["type"] == "CONVERSATION":
            controller.send_message(
                {"component": "code editor", "content": part["content"]}
            )
            sleep(randint(10, 25))
