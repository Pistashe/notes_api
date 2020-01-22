from notes_api.notes.note_plain import NotePlain


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

