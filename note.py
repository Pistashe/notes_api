import time
import uuid
import json

class Note():
    def __init__(self, title="", content="", tags=[], color="white",
                 history=[]):

        self.tags = tags
        self.color = color

        self._title = title
        self._content = content
        self._history = history
        self._datetime = time.asctime()
        self._version = 1
        self._id = uuid.uuid4().hex

    @classmethod
    def from_json(cls, note_json):
        """
        Loads a note from a json-encoded string.
        """
        note_ = json.JSONDecoder().decode(note_json)
        note = Note(note_["title"], note_["content"], note_["tags"],
                    note_["color"], note_["history"])
        note._id = note_["id"]
        note._datetime = note_["datetime"]
        note._version = note_["version"]
        return note

    @classmethod
    def from_encrypted_json(cls, file_name, encrypter):
        """
        Loads a note from an encrypted json-encoded string.
        """
        decrypted = encrypter.decrypt(file_name)
        return Note.from_json(decrypted)

    @property
    def title(self):
        return self._title

    @property
    def content(self):
        return self._content

    @title.setter
    def title(self, title):
        self._update_history()
        self._increment_version()
        self._title = title

    @content.setter
    def content(self, content):
        self._update_history()
        self._increment_version()
        self._content = content

    def _update_history(self):
        self._history.append({"version": self._version,
                              "datetime": self._datetime,
                              "title": self.title,
                              "content": self._content})

    def add_tags(self, tags):
        if isinstance(tags, list):
            self.tags += tags
        else:
            self.tags.append(tags)

        self.tags = list(set(self.tags)) # assert unicity of tags

    def _increment_version(self):
        self._datetime = time.asctime()
        self._version += 1

    def display(self, displayer):
        displayer.display(self)

    def _to_object(self):
        note_object = {"title": self._title,
                     "content": self._content,
                     "tags": self.tags,
                     "datetime": self._datetime,
                     "version": self._version,
                     "color": self.color,
                     "id": self._id,
                     "history": self._history}
        return note_object

    def _to_json(self):
        note_object = self._to_object()
        return json.JSONEncoder().encode(note_object)

    def save(self, encrypter=None):
        if encrypter is not None:
            to_save = encrypter.encrypt(self._to_json())
        else:
            to_save = json.JSONEncoder().encode(self._to_object())

        with open(self._id, "wb") as file_:
            file_.write(to_save)
