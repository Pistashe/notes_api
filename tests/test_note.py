import os
from pathlib import Path
import json
from cryptography.fernet import Fernet

from notes_api.note import Note
from notes_api.displayers.displayer import Displayer
from notes_api.encrypters.encrypter_symmetric import EncrypterSymmetric

DIR = os.path.abspath(os.path.dirname(__file__))

def _get_note():
    note = Note("Test", "test", ["test"], color="yellow")
    return note

def _get_encrypter():
    return EncrypterSymmetric(Fernet.generate_key())



def test_duplicate_success():
    try:
        note = _get_note()
        result = note.duplicate()
        expected = _get_note()
        assertion = result == expected
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test_duplicate_error():
    try:
        note = _get_note()
        result = Note("Test1", "test", ["test"], color="yellow")
        expected = _get_note()
        assertion = result != expected
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test_save_no_encrypter_success():
    try:
        note = _get_note()
        note.save()
        note_path = Path("./{}".format(note._id))
        assertion = note_path.exists()
        note_path.unlink()
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test_save_with_encrypter_success():
    try:
        note = _get_note()
        encrypter = _get_encrypter()
        note.save(encrypter=encrypter)
        note_path = Path("./{}".format(note._id))
        assertion = note_path.exists()
        note_path.unlink()
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test_display():
    try:
        note = _get_note()
        displayer = Displayer()
        note.display(displayer)
        assertion = False
    except NotImplementedError:
        assertion = True
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test_add_one_new_tag():
    try:
        note = _get_note()
        note.add_tags("test2")
        assertion = note.tags == {"test", "test2"}
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test_add_one_present_tag():
    try:
        note = _get_note()
        note.add_tags("test")
        assertion = note.tags == {"test"}
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test_add_list_new_tags():
    try:
        note = _get_note()
        note.add_tags(["test2", "test3"])
        assertion = note.tags ==  {"test", "test2", "test3"}
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test_add_list_new_and_present_tag():
    try:
        note = _get_note()
        note.add_tags(["test", "test2"])
        assertion = note.tags == {"test", "test2"}
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test_from_json_file():
    try:
        note = Note.from_json_file(os.path.join(DIR, "note_json"))
        expected = Note("Test1", "Ceci est un test très simple qui ne fait "\
                        "qu'afficher une note.", ["tag1", "tag2"],
                        color="yellow")
        assertion = note == expected
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test_from_encrypted_json_file_success():
    try:
        note_path = os.path.join(DIR, "note_json_encrypted")
        encrypter = EncrypterSymmetric(b'gHsn9E3w20VBdcpTL-Yqic'\
                                       b'Cnwzam2gUK_warZprfv_M=')
        note = Note.from_encrypted_json_file(note_path, encrypter)
        expected = Note("Test1", "Ceci est un test très simple qui ne fait "\
                        "qu'afficher une note.", ["tag1", "tag2"],
                        color="yellow")
        assertion = note == expected
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test_from_encrypted_json_file_error_key():
    try:
        note_path = os.path.join(DIR, "note_json_encrypted")
        encrypter = EncrypterSymmetric(b'AHsn9E3w20VBdcpTL-Yqic'\
                                       b'Cnwzam2gUK_warZprfv_M=')
        note = Note.from_encrypted_json_file(note_path, encrypter)
        assertion = False
    except KeyError:
        assertion = True
    except Exception as e:
        print(e)
        return False

    assert assertion

def test_set_title():
    note = _get_note()
    note.title = "ok"
    assert note._version == 2

def test_set_content():
    note = _get_note()
    note.content = "ok"
    assert note._version == 2
