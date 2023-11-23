from .types import *
from .create_chat_completion import *
from .insert_code_editor import *
from .send_chat_completion import *
from .run import *
from .scrape_public_chat import *
from .scrape_code_editors import *
from .scrape_screenshare import *
from .send_message import *
from .send_text_to_code_editor import *


commands: list[Command] = [
    {"label": "Run", "handler": run},
    {"label": "Create Chat Completion", "handler": create_chat_completion},
    {"label": "Send Chat Completion", "handler": send_chat_completion},
    {"label": "Insert Code Editor", "handler": insert_code_editor},
    {"label": "Scrape Public Chat", "handler": scrape_public_chat},
    {"label": "Scrape Code Editors", "handler": scrape_code_editors},
    {"label": "Scrape Screenshare", "handler": scrape_screenshare},
    {"label": "Send Message", "handler": send_message},
    {"label": "Send Text to Code Editor", "handler": send_text_to_code_editor},
]
