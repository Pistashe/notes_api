from notes_api.notebook import Notebook
from notes_api.note import Note

from notes_api.displayers.displayer import Displayer
from notes_api.synchronizers.synchronizer import Synchronizer


def _get_notebook():
    note_1 = Note("Test1", "Test1.", ["test1"], color="yellow")
    note_2 = Note("Test2", "Test2.", ["test2"], color="yellow")

    notebook = Notebook([note_1, note_2])
    return notebook

def _get_synchronizer():
    return Synchronizer()


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

    return assertion

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

    return assertion

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

    return assertion

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

    return assertion

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

    return assertion

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

    return assertion

def test_remove_list_notes():
    try:
        notebook = _get_notebook()
        notebook.remove_notes([0, 1])

        expected = Notebook([])
        assertion = notebook == expected
    except Exception as e:
        print(e)
        assertion = False

    return assertion

def test_display():
    try:
        notebook = _get_notebook()
        notebook.display(Displayer())
        assertion = False
    except NotImplementedError:
        assertion = True
    except Exception as e:
        print(e)
        assertion = False

    return assertion

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

    return assertion

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

    return assertion
