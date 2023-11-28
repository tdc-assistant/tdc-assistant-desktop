from typing import Union

from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2
from tdc_assistant_client.client import TdcAssistantClient
from tdc_assistant_session_request_controller.controller import (
    controller as session_request_controller,
)

from observers import (
    PublicChatObserver,
    ChatCompletionReadyObserver,
    CodeEditorsObserver,
    ScreenshareObserver,
    WordProcessorsObserver,
)
from event_handlers import (
    ChatUpdateEventHandler,
    ChatCompletionReadyEventHandler,
    ScreenshareUpdateEventHandler,
    CodeEditorsUpdateEventHandler,
    WordProcessorsUpdateEventHandler,
)


def _scrape_classroom_for_updates(
    code_editors_observer: CodeEditorsObserver,
    code_editors_update_event_handler: CodeEditorsUpdateEventHandler,
    screenshare_observer: ScreenshareObserver,
    screenshare_update_event_handler: ScreenshareUpdateEventHandler,
    word_processor_observer: WordProcessorsObserver,
    word_processor_update_event_handler: WordProcessorsUpdateEventHandler,
) -> None:
    code_editors_update_event = code_editors_observer.poll()

    if code_editors_update_event is not None:
        code_editors_update_event_handler.handle(code_editors_update_event)

    screenshare_update_event = screenshare_observer.poll()

    if screenshare_update_event is not None:
        screenshare_update_event_handler.handle(screenshare_update_event)

    word_processor_update_event = word_processor_observer.poll()

    if word_processor_update_event is not None:
        word_processor_update_event_handler.handle(word_processor_update_event)


def run(client: TdcAssistantClient, controller: TdcAssistantGuiControllerV2) -> None:
    public_chat_observer = PublicChatObserver(client, controller)
    chat_update_event_handler = ChatUpdateEventHandler(client, controller)

    chat_completion_ready_observer = ChatCompletionReadyObserver(client, controller)
    chat_completion_ready_event_handler = ChatCompletionReadyEventHandler(
        client, controller
    )

    code_editors_observer = CodeEditorsObserver(client, controller)
    code_editors_update_event_handler = CodeEditorsUpdateEventHandler(
        client, controller
    )

    screenshare_observer = ScreenshareObserver(client, controller)
    screenshare_update_event_handler = ScreenshareUpdateEventHandler(client, controller)

    word_processor_observer = WordProcessorsObserver(client, controller)
    word_processor_update_event_handler = WordProcessorsUpdateEventHandler(
        client, controller
    )

    while not session_request_controller.should_terminate():
        session_request_controller.run()

    # TODO Chat completion ready observer should just send a single part not the entire thing
    #      in order to handle message between sending parts it would re-enter here

    while True:
        public_chat_event = public_chat_observer.poll()

        if public_chat_event is not None:
            if public_chat_event["name"] == "chat-update":
                _scrape_classroom_for_updates(
                    code_editors_observer,
                    code_editors_update_event_handler,
                    screenshare_observer,
                    screenshare_update_event_handler,
                    word_processor_observer,
                    word_processor_update_event_handler,
                )
                chat_update_event_handler.handle(public_chat_event)

                # Without this a message would never be sent to the student
                # TODO Debouncing should occur here .. so could add a wait and check
                # to see if another message has been sent ... although calling `chat_update_event_handler.handle`
                # above after scraping everything does serve as a debouncing step since there will be some
                # delay before the chat is scraped again
                while True:
                    chat_completion_event = chat_completion_ready_observer.poll()

                    if chat_completion_event is not None:
                        if chat_completion_event["name"] == "chat-completion-ready":
                            chat_completion_ready_event_handler.handle(
                                chat_completion_event
                            )
                        break
        else:
            chat_completion_event = chat_completion_ready_observer.poll()

            if chat_completion_event is not None:
                if chat_completion_event["name"] == "chat-completion-ready":
                    chat_completion_ready_event_handler.handle(chat_completion_event)
