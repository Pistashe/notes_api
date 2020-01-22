import os

from notes_api.notes.note_loader import NoteLoader
from notes_api.notes.note_plain import NotePlain
from notes_api.notes.note_tick import NoteTick

from notes_api.encrypters.encrypter import Encrypter

DIR = os.path.abspath(os.path.dirname(__file__))

def _get_loader():
    return NoteLoader()

def _get_encrypter():
    return Encrypter("test")

def test_load_plain_from_json_success():
    try:
        loader = _get_loader()
        result = loader.load_from_json(os.path.join(DIR, "note_plain_json"))
        expected = NotePlain("Test", "test", ["test"], color="yellow")
        assertion = result == expected
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test_load_tick_from_json_success():
    try:
        loader = _get_loader()
        result = loader.load_from_json(os.path.join(DIR, "note_tick_json"))
        expected = NoteTick("Test", [{"text": "Test1", "ticked": False},
                                     {"text": "Test2", "ticked": True},
                                     {"text": "Test3", "ticked": False}],
                            ["test"], color="yellow")
        assertion = result == expected
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test_load_from_encrypted_json_success():
    try:
        loader = _get_loader()
        encrypter = _get_encrypter()
        result = loader.load_from_json(os.path.join(DIR, "note_plain_json"),
                                       encrypter)
        assertion = False
    except NotImplementedError:
        assertion = True
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test_load_from_json_error_filename():
    try:
        loader = _get_loader()
        result = loader.load_from_json(
            os.path.join(DIR, "note_nonexisting_json"))
        assertion = False
    except FileNotFoundError:
        assertion = True
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

