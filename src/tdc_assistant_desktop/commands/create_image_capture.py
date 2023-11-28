from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2
from tdc_assistant_client.client import TdcAssistantClient


def create_image_capture(
    client: TdcAssistantClient, controller: TdcAssistantGuiControllerV2
):
    chat_log_before = client.create_chat_log(customer_name="Demo", raw_text="")
    image_capture = client.create_image_capture(
        chat_log=chat_log_before,
        image_url="DEMO IMAGE URL",
        type="SCREENSHARE",
    )
    print(image_capture)
    chat_log_after = client.get_chat_log(chat_log_id=chat_log_before["id"])
    print(chat_log_after)
