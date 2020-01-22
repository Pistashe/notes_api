from notes_api.notes.note_tick import NoteTick
from notes_api.notes.note_plain import NotePlain


def _get_note():
    note = NoteTick("Test", [{"text": "Test1", "ticked": False},
                             {"text": "Test2", "ticked": True},
                             {"text": "Test3", "ticked": False}],
                    ["test"], color="yellow")
    return note

def test_init_success():
    try:
        note = _get_note()
        assertion = note._type == "tick"
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test_add_item_success():
    try:
        note = _get_note()
        note.add_item("Test4", False)
        expected = NoteTick("Test", [{"text": "Test1", "ticked": False},
                                     {"text": "Test2", "ticked": True},
                                     {"text": "Test3", "ticked": False},
                                     {"text": "Test4", "ticked": False}],
                             ["test"], color="yellow")
        assertion = note == expected
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test_remove_item_success():
    try:
        note = _get_note()
        note.remove_item(1)
        expected = NoteTick("Test", [{"text": "Test1", "ticked": False},
                                     {"text": "Test3", "ticked": False}],
                             ["test"], color="yellow")
        assertion = note == expected
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test_tick_item_true_success():
    try:
        note = _get_note()
        note.tick_item(2)
        assertion = note.content[2]["ticked"]
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test_tick_item_false_success():
    try:
        note = _get_note()
        note.tick_item(1)
        assertion = not note.content[2]["ticked"]
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test_is_item_ticked_success():
    try:
        note = _get_note()
        assertion = note.is_item_ticked(1)
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test_sort_by_ticked_success():
    try:
        note = _get_note()
        note.sort_by_ticked(False)
        expected = NoteTick("Test", [{"text": "Test2", "ticked": True},
                                     {"text": "Test3", "ticked": False},
                                     {"text": "Test1", "ticked": False}],
                            ["test"], color="yellow")
        assertion = note == expected
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test_to_plain_success():
    try:
        note = _get_note()
        result = note.to_plain()
        expected = NotePlain("Test", "Test1\nTest2\nTest3",
                             ["test"], color="yellow")
        assertion = result == expected
    except Exception as e:
        print(e)
        assertion = False

    assert assertion
