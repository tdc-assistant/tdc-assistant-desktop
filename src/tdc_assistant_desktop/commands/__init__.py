from .types import *
from .create_chat_completion import *
from .insert_code_editor import *
from .send_chat_completion import *


commands: list[Command] = [
    {"label": "Create Chat Completion", "handler": create_chat_completion},
    {"label": "Send Chat Completion", "handler": send_chat_completion},
    {"label": "Insert Code Editor", "handler": insert_code_editor},
]
