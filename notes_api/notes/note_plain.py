import time
import uuid

# from .note_interface import NoteInterface
from .note import Note

class NotePlain(Note):
    def __init__(self, title="", content="", tags={}, color="white",
                 history=[]):

        self.tags = set(tags)
        self.color = color

        self._title = title
        self._content = content
        self._history = history
        self._datetime = time.asctime()
        self._version = 1
        self._id = uuid.uuid4().hex
        self._type = "plain"

#     @classmethod
#     def _from_json_string(cls, string):
#         """
#         Loads a note from a json-encoded string.
#         """
#         note_ = json.JSONDecoder().decode(string)
#         note = NotePlain(note_["title"], note_["content"], note_["tags"],
#                          note_["color"], note_["history"])

#         note._id = note_["id"]
#         note._datetime = note_["datetime"]
#         note._version = note_["version"]
#         return note

#     def duplicate(self):
#         note = NotePlain(self._title, self._content, self.tags,
#                          self.color, self._history)

#         return note

