from typing import TypedDict, Callable

from tdc_assistant_client.client import TdcAssistantClient
from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2


class Command(TypedDict):
    label: str
    handler: Callable[[TdcAssistantClient, TdcAssistantGuiControllerV2], None]
