from typing import Optional

from datetime import datetime, timezone, timedelta
from random import choice
from time import sleep

from tdc_assistant_client.client import TdcAssistantClient
from tdc_assistant_client.domain import ChatLog
from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2

from .base_task import BaseTask

from utils import (
    MAX_SESSION_LIMIT_IN_MINUTES,
    PRESCRIPTED_END_SESSION_PROMPTS,
    PRESCRIPTED_FAREWELL_MESSAGES,
)


class CheckSessionLimitExceeded(BaseTask):
    def __init__(
        self,
        client: TdcAssistantClient,
        controller: TdcAssistantGuiControllerV2,
        interval_between_execution_in_seconds: Optional[float] = None,
    ):
        super().__init__(client, controller, interval_between_execution_in_seconds)

    def _execute(self, chat_log: Optional[ChatLog]) -> ChatLog:
        if chat_log is None:
            raise Exception()

        session_start = chat_log["createdAt"]
        now = datetime.now(timezone.utc)

        is_session_limit_exceeded = session_start < now - timedelta(
            minutes=MAX_SESSION_LIMIT_IN_MINUTES
        )

        if is_session_limit_exceeded:
            # Send end-of-session message to student and click button to terminate session
            self._controller.send_message(choice(PRESCRIPTED_END_SESSION_PROMPTS))
            sleep(10)
            self._controller.send_message(choice(PRESCRIPTED_FAREWELL_MESSAGES))
            self._controller.end_session()

        return chat_log
