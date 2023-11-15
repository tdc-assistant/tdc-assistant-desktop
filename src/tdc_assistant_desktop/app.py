from time import sleep

from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2
from tdc_assistant_client.client import TdcAssistantClient

from config import config, env

from commands import commands


def main():
    run_cli(init_client(), init_controller())


def run_cli(client: TdcAssistantClient, controller: TdcAssistantGuiControllerV2):
    while True:
        option = display_menu()

        if option < 0:
            print("Good-bye!")
            break

        sleep(config["DELAY_AFTER_OPTION_SELECT_IN_SECONDS"])
        commands[option]["handler"](client, controller)


def init_controller() -> TdcAssistantGuiControllerV2:
    public_chat_pop_out_coords = env["PUBLIC_CHAT_POP_OUT_COORDS"]
    public_chat_text_area_coords = env["PUBLIC_CHAT_TEXT_AREA_COORDS"]
    insert_code_editor_coord_path = env["INSERT_CODE_EDITOR_COORD_PATH"]

    return TdcAssistantGuiControllerV2(
        {
            "tutor_profile": {
                "first_name": str(env["FIRST_NAME"]),
                "last_initial": str(env["LAST_INITIAL"]),
            },
            "coords": {
                "public_chat_pop_out": {
                    "x": int(public_chat_pop_out_coords[0]),  # type: ignore
                    "y": int(public_chat_pop_out_coords[1]),  # type: ignore
                },
                "public_chat_text_area": {
                    "x": int(public_chat_text_area_coords[0]),  # type: ignore
                    "y": int(public_chat_text_area_coords[1]),  # type: ignore
                },
                "insert_code_editor_coord_path": (
                    {
                        "x": insert_code_editor_coord_path[0][0],  # type: ignore
                        "y": insert_code_editor_coord_path[0][1],  # type: ignore
                    },
                    {
                        "x": insert_code_editor_coord_path[1][0],  # type: ignore
                        "y": insert_code_editor_coord_path[1][1],  # type: ignore
                    },
                    {
                        "x": insert_code_editor_coord_path[2][0],  # type: ignore
                        "y": insert_code_editor_coord_path[2][1],  # type: ignore
                    },
                    {
                        "x": insert_code_editor_coord_path[3][0],  # type: ignore
                        "y": insert_code_editor_coord_path[3][1],  # type: ignore
                    },
                ),
                "public_chat_button_coords": {"x": 1200, "y": 170},
            },
            "scraped_editor_config": {
                "coords_left": (100, 170),
                "coords_right": (950, 170),
                "coords_pop_out_button": (940, 170),
                "text_editor_coords": (500, 500),
            },
        }
    )


def init_client() -> TdcAssistantClient:
    return TdcAssistantClient(url=str(env["TDC_ASSISTANT_URL"]))


def display_menu() -> int:
    user_input = ""
    while True:
        try:
            for i, command in enumerate(commands):
                print(f"[{i+1}] {command['label']}")
            print("[0] Quit")
            user_input = input("Enter option: ").strip().lower()
            print()
            option = int(user_input) - 1
            if option < len(commands):
                return option
            else:
                display_invalid_option_message(user_input)
        except ValueError:
            display_invalid_option_message(user_input)


def display_invalid_option_message(option: str):
    print(f"Invalid option: '{option}'")


if __name__ == "__main__":
    main()
