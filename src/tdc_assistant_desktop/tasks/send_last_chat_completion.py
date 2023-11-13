from random import randint
from time import sleep

from tdc_assistant_client.client import TdcAssistantClient
from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2

from store import load_most_recent_chat_log


def send_last_chat_completion(
    client: TdcAssistantClient,
    controller: TdcAssistantGuiControllerV2,
):
    most_recent_chat_log = load_most_recent_chat_log()
    if most_recent_chat_log is None:
        return

    messages = most_recent_chat_log["messages"]
    most_recent_message = messages[-1]
    chat_completions = [
        annotation["chatCompletion"]
        for annotation in most_recent_message["annotations"]
        if annotation["type"] == "CHAT_COMPLETION"
        and annotation["chatCompletion"] is not None
    ]

    if len(chat_completions) == 0:
        print("No chat completions found")
        return

    last_chat_completion = chat_completions[-1]

    for part in last_chat_completion["parts"]:
        print(f'[{part["type"]}]')
        print(part["content"])
        print()

    should_send = input("Send chat completion (y/[N])? ").strip().lower() == "y"

    if not should_send:
        return

    for part in last_chat_completion["parts"]:
        if part["type"] == "CONVERSATION":
            sleep(randint(15, 30))
            controller.send_message(
                {"component": "code editor", "content": part["content"]}
            )
