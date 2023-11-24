from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2
from tdc_assistant_client.client import TdcAssistantClient
from domain import Event


class WordProcessorsUpdateEventHandler:
    _client: TdcAssistantClient
    _controller: TdcAssistantGuiControllerV2

    def __init__(
        self, client: TdcAssistantClient, controller: TdcAssistantGuiControllerV2
    ):
        self._client = client
        self._controller = controller

    def handle(self, event: Event):
        payload = event.get("payload")

        if payload is None or not isinstance(payload, dict):
            return None

        chat_log = payload["chat_log"]
        word_processors_to_create = payload["word_processors_to_create"]
        word_processors_to_update = payload["word_processors_to_update"]

        for word_processor_to_create in word_processors_to_create:
            self._client.create_word_processor(
                chat_log=chat_log,
                number=word_processor_to_create["number"],
                content=word_processor_to_create["content"],
            )

        for word_processor_to_update in word_processors_to_update:
            self._client.update_word_processor(
                word_processor=word_processor_to_update["word_processor"],
                content=word_processor_to_update["new_content"],
            )
