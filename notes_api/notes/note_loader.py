import json

from .note_tick import NoteTick
from .note_plain import NotePlain

class NoteLoader():
    @staticmethod
    def load(file_name, encrypter):

