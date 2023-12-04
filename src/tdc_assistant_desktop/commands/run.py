from typing import Union, List

from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2
from tdc_assistant_client.client import TdcAssistantClient
from tdc_assistant_session_request_controller.controller import (
    controller as session_request_controller,
)


from tasks import (
    CheckPublicChat,
    InitializeSession,
    fetch_most_recent_chat_log,
    CheckCodeEditorsTask,
    CheckScreenshareTask,
    CheckWordProcessorTask,
)

Task = Union[
    CheckPublicChat, CheckCodeEditorsTask, CheckScreenshareTask, CheckWordProcessorTask
]


def run(client: TdcAssistantClient, controller: TdcAssistantGuiControllerV2) -> None:
    initialize_session = InitializeSession(client, controller)

    tasks: List[Task] = [
        CheckPublicChat(client, controller),
        CheckCodeEditorsTask(client, controller, 30.0),
        CheckScreenshareTask(client, controller, 45.0),
        CheckWordProcessorTask(client, controller, 30.0),
    ]

    while not session_request_controller.should_terminate():
        session_request_controller.run()

    chat_log = initialize_session.execute(fetch_most_recent_chat_log(client))
    i = 0
    while True:
        chat_log = tasks[i].execute(chat_log)
        i = (i + 1) % len(tasks)
