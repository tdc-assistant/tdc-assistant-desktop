from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2
from tdc_assistant_client.client import TdcAssistantClient

from config.env import env


from tasks import persist_chat_log


def main():
    controller = init_controller()
    client = init_client()
    persist_chat_log(client, controller)


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


if __name__ == "__main__":
    main()
