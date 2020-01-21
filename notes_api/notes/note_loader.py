import json

from .note_tick import NoteTick
from .note_plain import NotePlain

class NoteLoader():
    @staticmethod
    def load_from_json(file_name, encrypter=None):
        read_mode = "r" if encrypter is None else "rb"
        with open(file_name, read_mode) as file_:
            note_ = file_.read()

        if encrypter is not None:
            note_ = encrypter.decrypt(note_)

        note_ = json.JSONDecoder().decode(note_)

        note_class = NoteTick if note_["type"] == "tick" else NotePlain

        note = note_class(note_["title"], note_["content"], note_["tags"],
                          note_["color"], note_["history"])

        note._id = note_["id"]
        note._datetime = note_["datetime"]
        note._version = note_["version"]
        return note

