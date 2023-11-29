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
from .create_code_editor import *
from .scrape_word_processors import *
from .create_word_processor import *
from .create_image_capture import *
from .create_chat_completion_mock_controller import *
from .find_chat_log_by_id import *
from .request_chat_completion_approval import *


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
    {"label": "Create Code Editor", "handler": create_code_editor},
    {"label": "Scrape Word Processors", "handler": scrape_word_processors},
    {"label": "Create Word Processors", "handler": create_word_processor},
    {"label": "Create Image Capture", "handler": create_image_capture},
    {
        "label": "Create Chat Completion Mock Controller",
        "handler": create_chat_completion_mock_controller,
    },
    {"label": "Find Chat Log by ID", "handler": find_chat_log_by_id},
    {
        "label": "Request chat completion approval",
        "handler": request_chat_completion_approval,
    },
]
