from typing import TypedDict

from tdc_assistant_client.domain import CodeEditor


class UpdateCodeEditorPayload(TypedDict):
    code_editor: CodeEditor
    new_content: str
