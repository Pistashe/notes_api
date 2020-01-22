from notes_api.notes.note_plain import NotePlain
from notes_api.notes.note_tick import NoteTick


def _get_note():
    note = NotePlain("Test", "test", ["test"], color="yellow")
    return note

def test_init():
    try:
        note = _get_note()
        assertion = note._type == "plain"
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test_to_tick_success():
    try:
        note = _get_note()
        result = note.to_tick()
        expected = NoteTick("Test", [{"text": "test", "ticked":False}],
                            ["test"], color="yellow")
        assertion = result == expected
    except Exception as e:
        print(e)
        assertion = False

    assert assertion
