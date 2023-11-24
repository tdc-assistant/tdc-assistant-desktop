from typing import TypedDict

from tdc_assistant_client.domain import WordProcessor


class UpdateWordProcessorPayload(TypedDict):
    word_processor: WordProcessor
    new_content: str
