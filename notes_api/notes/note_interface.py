import time
import uuid
import json

from notes_api.exceptions import DecryptionError

# from .note_plain import NotePlain
# from .note_tick import NoteTick


class NoteInterface():
    def __init__(self, title="", content=None, tags={}, color="white",
                 history=[]):

        self.tags = set(tags)
        self.color = color

        self._title = title
        self._content = content
        self._history = history
        self._datetime = time.asctime()
        self._version = 1
        self._id = uuid.uuid4().hex
        self._type = None

    def __eq__(self, note):
        is_eq = self._title == note.title and \
                self._content == note.content and \
                self.tags == note.tags and \
                self.color == note.color

        return is_eq

    def __ne__(self, note):
        return not self.__eq__(note)

    @classmethod
    def from_file(cls, file_name, encrypter=None):
        """
        Loads a note from a json_encoded file.
        """
        read_mode = "r" if encrypter is None else "rb"
        with open(file_name, read_mode) as file_:
            note_ = file_.read()

        if encrypter is not None:
            note_ = encrypter.decrypt(note_)

        return Note._from_json_string(note_)


    @classmethod
    def _from_json_string(cls, string):
        """
        Loads a note from a json-encoded string.
        """
        raise NotImplementedError("_from_json_string method not implemented.")
        # note_ = json.JSONDecoder().decode(string)

        # if note_["type"] == "tick":
        #     from .note_tick import NoteTick
        #     note = NoteTick(note_["title"], note_["content"], note_["tags"],
        #                     note_["color"], note_["history"])
        # else:
        #     from .note_plain import NotePlain
        #     note = NotePlain(note_["title"], note_["content"], note_["tags"],
        #                      note_["color"], note_["history"])

        # note._id = note_["id"]
        # note._datetime = note_["datetime"]
        # note._version = note_["version"]
        # return note

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
        if isinstance(tags, list) or isinstance(tags, set):
            self.tags = self.tags.union(set(tags))
        else:
            self.tags.add(tags)

    def _increment_version(self):
        self._datetime = time.asctime()
        self._version += 1

    def display(self, displayer):
        displayer.display(self)

    def _to_object(self):
        note_object = {"title": self._title,
                       "content": self._content,
                       "tags": list(self.tags),
                       "datetime": self._datetime,
                       "version": self._version,
                       "color": self.color,
                       "id": self._id,
                       "history": self._history,
                       "type": self._type}
        return note_object

    def _to_json(self):
        note_object = self._to_object()
        return json.JSONEncoder().encode(note_object)

    def save(self, encrypter=None):
        if encrypter is not None:
            write_mode = "wb"
            to_save = encrypter.encrypt(self._to_json())
        else:
            write_mode = "w"
            to_save = json.JSONEncoder().encode(self._to_object())

        with open(self._id, write_mode) as file_:
            file_.write(to_save)

    def duplicate(self):
        raise NotImplementedError("duplicate method not implemented.")
        # if self._type == "tick":
        #     from .note_tick import NoteTick
        #     note = NoteTick(self._title, self._content, self.tags,
        #                     self.color, self._history)
        # else:
        #     from .note_plain import NotePlain
        #     note = NotePlain(self._title, self._content, self.tags,
        #                      self.color, self._history)

        # return note

    # def backup_previous_version(self, version=0):
    #     if version == 0: # default is the n-1 version
    #         self.
    #     pass

