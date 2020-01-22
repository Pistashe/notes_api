import os
import pathlib
from cryptography.fernet import Fernet

from notes_api.notebook import Notebook
from notes_api.notes.note import Note

from notes_api.exceptions import DecryptionError
from notes_api.displayers.displayer import Displayer
from notes_api.synchronizers.synchronizer import Synchronizer
from notes_api.encrypters.encrypter import Encrypter
# from notes_api.encrypters.encrypter_symmetric import EncrypterSymmetric


DIR = os.path.abspath(os.path.dirname(__file__))


def _get_notebook():
    note_1 = Note("Test1", "Test1.", ["test1"], color="yellow")
    note_2 = Note("Test2", "Test2.", ["test2"], color="yellow")
    notebook = Notebook([note_1, note_2])
    return notebook

def _get_synchronizer():
    return Synchronizer()

def _get_encrypter():
    return Encrypter("test")

def test_sync():
    try:
        notebook = _get_notebook()
        synchronizer = _get_synchronizer()
        notebook.sync(synchronizer)
        assertion = False
    except NotImplementedError:
        assertion = True
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test_reorder_success():
    try:
        notebook = _get_notebook()
        notebook.reorder([0, 1])
        note_1 = Note("Test2", "Test2.", ["test2"], color="yellow")
        note_2 = Note("Test1", "Test1.", ["test1"], color="yellow")

        expected = Notebook([note_1, note_2])
        assertion = notebook == expected
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test_reorder_error():
    try:
        notebook = _get_notebook()
        notebook.reorder([0, 2])
        assertion = False
    except IndexError:
        assertion = True
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test_add_one_note():
    try:
        notebook = _get_notebook()
        note_1 = Note("Test1", "Test1.", ["test1"], color="yellow")
        note_2 = Note("Test2", "Test2.", ["test2"], color="yellow")
        note_3 = Note("Test3", "Test3.", ["test3"], color="yellow")
        notebook.add_notes(note_3)

        expected = Notebook([note_1, note_2, note_3])
        assertion = notebook == expected
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test_add_list_notes():
    try:
        notebook = _get_notebook()
        note_1 = Note("Test1", "Test1.", ["test1"], color="yellow")
        note_2 = Note("Test2", "Test2.", ["test2"], color="yellow")
        note_3 = Note("Test3", "Test3.", ["test3"], color="yellow")
        note_4 = Note("Test4", "Test4.", ["test4"], color="yellow")
        notebook.add_notes([note_3, note_4])

        expected = Notebook([note_1, note_2, note_3, note_4])
        assertion = notebook == expected
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test_remove_one_note():
    try:
        notebook = _get_notebook()
        note_2 = Note("Test2", "Test2.", ["test2"], color="yellow")
        notebook.remove_notes(0)

        expected = Notebook([note_2])
        assertion = notebook == expected
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test_remove_list_notes():
    try:
        notebook = _get_notebook()
        notebook.remove_notes([0, 1])

        expected = Notebook([])
        assertion = notebook == expected
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test_display():
    try:
        notebook = _get_notebook()
        notebook.display(Displayer())
        assertion = False
    except TypeError:
        assertion = True
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test__update_tags():
    try:
        notebook = _get_notebook()
        note_3 = Note("Test3", "Test3.", ["test3"], color="yellow")
        notebook.add_notes(note_3)

        result = notebook.tags
        expected = {"test1", "test2", "test3"}
        assertion = result == expected
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test_set_notes():
    try:
        notebook = _get_notebook()
        note_3 = Note("Test3", "Test3.", ["test3"], color="yellow")
        notebook.notes = [note_3]

        result = notebook.tags
        expected = {"test3"}
        assertion = result == expected
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test_save_without_encryption_success():
    try:
        notebook = _get_notebook()
        notebook.save()
        archive_path = pathlib.Path("./notebook_archive.tar")
        assertion = archive_path.exists()
        archive_path.unlink()
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test_save_with_encryption_success():
    try:
        notebook = _get_notebook()
        encrypter = _get_encrypter()
        notebook.save(encrypter)
        assertion = False
    except NotImplementedError:
        assertion = True
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test_from_archive_success():
    try:
        archive_path = os.path.join(DIR, "notebook_archive.tar")
        notebook = Notebook.from_archive(archive_path)
        expected = _get_notebook()
        assertion = notebook == expected
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test_from_archive_error_nonexisting():
    try:
        archive_path = os.path.join(DIR, "notebook_archive_nonexisting.tar")
        notebook = Notebook.from_archive(archive_path)
        assertion = False
    except FileNotFoundError:
        assertion = True
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test_from_encrypted_archive_success():
    try:
        archive_path = os.path.join(DIR, "notebook_archive_encrypted.tar")
        encrypter = _get_encrypter()
        notebook = Notebook.from_archive(archive_path, encrypter)
        # expected = _get_notebook()
        # assertion = notebook == expected
        assertion = False
    except NotImplementedError:
        assertion = True
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

# def test_from_encrypted_archive_error_decryption():
#     try:
#         archive_path = os.path.join(DIR, "notebook_archive_encrypted.tar")
#         encrypter = EncrypterSymmetric(b'GHsn9E3w20VBdcpTL-Yqic'\
#                                        b'Cnwzam2gUK_warZprfv_M=')
#         notebook = Notebook.from_archive(archive_path, encrypter)
#         assertion = False
#     except DecryptionError:
#         assertion = True
#     except Exception as e:
#         print(e)
#         assertion = False

#     assert assertion

def test_is_eq_success():
    try:
        notebook_1 = _get_notebook()
        notebook_2 = _get_notebook()
        assertion = notebook_1 == notebook_2
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test_is_eq_error_index():
    try:
        notebook_1 = _get_notebook()
        notebook_2 = _get_notebook()
        note_3 = Note("Test3", "Test3.", ["test3"], color="yellow")
        notebook_2.add_notes(note_3)
        assertion = notebook_1 != notebook_2
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test_is_eq_error_order():
    try:
        notebook_1 = _get_notebook()
        notebook_2 = _get_notebook()
        notebook_2.reorder([0, 1])
        assertion = notebook_1 != notebook_2
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test_get_notes():
    try:
        notebook_1 = _get_notebook()
        result = notebook_1.notes
        expected = [Note("Test1", "Test1.", ["test1"], color="yellow"),
                    Note("Test2", "Test2.", ["test2"], color="yellow")]
        assertion = result == expected
    except Exception as e:
        print(e)
        assertion = False

    assert assertion
