from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2
from tdc_assistant_client.client import TdcAssistantClient


def create_word_processor(
    client: TdcAssistantClient, controller: TdcAssistantGuiControllerV2
):
    chat_log_before = client.create_chat_log(customer_name="Demo")
    code_editor = client.create_code_editor(
        chat_log=chat_log_before,
        programming_language="Python",
        editor_number=1,
        content='print("Hello world")',
    )
    client.update_code_editor(code_editor=code_editor, content='print("hello earth")')
    word_processor = client.create_word_processor(
        chat_log=chat_log_before, number=1, content=""
    )
    client.update_word_processor(word_processor=word_processor, content="Hey there!")
    chat_log_after = client.get_chat_log(chat_log_id=chat_log_before["id"])
    print(chat_log_after)
