import time
import uuid

from .note import Note

class NotePlain(Note):
    def __init__(self, title="", content="", tags={}, color="white",
                 history=[]):
        Note.__init__(self, title, content, tags, color, history)
        self._type = "plain"

    def to_tick(self):
        from .note_tick import NoteTick
        content = [{"text": self._content, "ticked": False}]
        note = NotePlain(self._title, content, self.tags, self.color,
                         self._history)
        note._id = self._id
        note._version = self._version + 1
        return note
