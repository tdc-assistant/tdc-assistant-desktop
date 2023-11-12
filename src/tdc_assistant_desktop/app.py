from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2
from tdc_assistant_gui_controller_v2.send_message import Message
from tdc_assistant_client.client import TdcAssistantClient

from config.env import env

from tasks import persist_chat_log, create_chat_completion_annotation
from store import load_most_recent_chat_log


def main():
    run_cli(init_client(), init_controller())


def run_cli(client: TdcAssistantClient, controller: TdcAssistantGuiControllerV2):
    while True:
        option = display_menu()
        if option == "1":
            scrape_public_chat_and_create_chat_completion(client, controller)
        elif option == "2":
            get_chat_completion_for_last_chat_log(client)
        elif option == "3":
            message_content = input("Enter message text: ")
            send_message(
                controller, {"component": "public chat", "content": message_content}
            )
        elif option == "q":
            break
        else:
            print(f"Invalid option: '{option}'")


def init_controller() -> TdcAssistantGuiControllerV2:
    public_chat_pop_out_coords = env["PUBLIC_CHAT_POP_OUT_COORDS"]
    public_chat_text_area_coords = env["PUBLIC_CHAT_TEXT_AREA_COORDS"]
    return TdcAssistantGuiControllerV2(
        {
            "tutor_profile": {
                "first_name": str(env["FIRST_NAME"]),
                "last_initial": str(env["LAST_INITIAL"]),
            },
            "coords": {
                "public_chat_pop_out": {
                    "x": int(public_chat_pop_out_coords[0]),
                    "y": int(public_chat_pop_out_coords[1]),
                },
                "public_chat_text_area": {
                    "x": int(public_chat_text_area_coords[0]),
                    "y": int(public_chat_text_area_coords[1]),
                },
            },
        }
    )


def init_client() -> TdcAssistantClient:
    return TdcAssistantClient(url=str(env["TDC_ASSISTANT_URL"]))


def scrape_public_chat_and_create_chat_completion(
    client: TdcAssistantClient, controller: TdcAssistantGuiControllerV2
):
    chat_log = persist_chat_log(client, controller)
    chat_log_with_annotation = create_chat_completion_annotation(client, chat_log)

    if chat_log_with_annotation is None:
        print("Failed to create annotation for `ChatLog`")
        return

    for message in chat_log_with_annotation["messages"]:
        for annotation in message["annotations"]:
            if annotation["type"] == "CHAT_COMPLETION":
                chat_completion = annotation["chatCompletion"]
                if chat_completion is None:
                    continue

                parts = chat_completion["parts"]
                if parts is None:
                    continue
                for part in parts:
                    part_type = part["type"]
                    print(f"[{part_type}]")
                    print(part["content"])
                    print()


def get_chat_completion_for_last_chat_log(client: TdcAssistantClient):
    chat_log = load_most_recent_chat_log()

    if chat_log is None:
        return

    if len(chat_log["messages"]) == 0:
        return

    chat_log_completion = client.create_chat_completion_annotation(
        message=chat_log["messages"][-1]
    )

    print(chat_log_completion)


def send_message(controller: TdcAssistantGuiControllerV2, message: Message):
    controller.send_message(message)


def display_menu() -> str:
    print("[1] Scrape public chat and create chat completion")
    print("[2] Generate chat completion for last message")
    print("[3] Send message")
    print("[Q] Quit")
    return input("Enter option: ").strip().lower()


if __name__ == "__main__":
    main()
