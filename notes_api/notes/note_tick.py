import time
import uuid

from .note import Note

class NoteTick(Note):
    def __init__(self, title="", content=[], tags={}, color="white",
                 history=[]):
        Note.__init__(self, title, content, tags, color, history)
        self._type = "tick"

    def add_item(self, content="", ticked=False):
        self.content.append({"text": content, "ticked": ticked})

    def remove_item(self, item_id):
        self.content.pop(item_id)

    def tick_item(self, item_id):
        self.content[item_id]["ticked"] = not self.content[item_id]["ticked"]

    def is_item_ticked(self, item_id):
        return self.content[item_id]["ticked"]

    def sort_by_ticked(self, unticked_first=True):
        sorted_content = [item for item in self._content if not item["ticked"]]
        sorted_content += [item for item in self._content if item["ticked"]]
        if not unticked_first:
            sorted_content = list(reversed(sorted_content))

        self.content = sorted_content
