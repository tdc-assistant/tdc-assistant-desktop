from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2
from tdc_assistant_client.client import TdcAssistantClient

from config.env import env

from tasks import persist_chat_log, create_chat_completion_annotation


def main():
    run_cli(init_client(), init_controller())


def run_cli(client: TdcAssistantClient, controller: TdcAssistantGuiControllerV2):
    while True:
        option = display_menu()
        if option == "1":
            scrape_public_chat_and_create_chat_completion(client, controller)
        elif option == "q":
            break
        else:
            print(f"Invalid option: '{option}'")


def init_controller() -> TdcAssistantGuiControllerV2:
    return TdcAssistantGuiControllerV2(
        {
            "tutor_profile": {
                "first_name": env["FIRST_NAME"],
                "last_initial": env["LAST_INITIAL"],
            }
        }
    )


def init_client() -> TdcAssistantClient:
    return TdcAssistantClient(url=env["TDC_ASSISTANT_URL"])


def scrape_public_chat_and_create_chat_completion(
    client: TdcAssistantClient, controller: TdcAssistantGuiControllerV2
):
    chat_log = persist_chat_log(client, controller)
    chat_log_with_annotation = create_chat_completion_annotation(client, chat_log)

    if chat_log_with_annotation is None:
        print("Failed to create annotation for `ChatLog`")
        return

    print(chat_log_with_annotation)


def display_menu() -> str:
    print("[1] Scrape public chat and create chat completion")
    print("[Q] Quit")
    return input("Enter option: ").strip().lower()


if __name__ == "__main__":
    main()
