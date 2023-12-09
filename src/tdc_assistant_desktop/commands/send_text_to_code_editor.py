from tdc_assistant_gui_controller_v2.controller import TdcAssistantGuiControllerV2
from tdc_assistant_client.client import TdcAssistantClient

java_program_text: str = """
public class Counter {

    // Private components:
    private int count; // The current count.

    public Counter () {
        this.count = 0;
    }

    public void incrementCount () {
        this.count++;
    }

    public int getCount () {
        return this.count;
    }
}
"""

python_program_text = """
class Counter:
    def __init__(self):
        self.count = 0

    def increment_count(self):
        self.count += 1

    def get_count(self):
        return self.count
"""


def send_text_to_code_editor(
    client: TdcAssistantClient, controller: TdcAssistantGuiControllerV2
):
    # controller.send_text_to_code_editor("Python", 1, python_program_text)
    controller.send_text_to_code_editor("Java", 1, java_program_text)
