import json
from cryptography.fernet import Fernet

from notes_api.note import Note
from notes_api.notebook import Notebook
from notes_api.displayers.displayer_ascii import DisplayerAscii
from notes_api.encrypters.encrypter_symmetric import EncrypterSymmetric


note_1 = Note("Test1", "Ceci est un test très simple qui ne fait qu'afficher "\
              "une note.", ["tag1", "tag2"], color="yellow")

note_2 = Note("Test2", "Ceci est une deuxième note, encore une fois très "\
              "simple", ["tag2", "tag3"], color="red")

displayer = DisplayerAscii()
# note_1.display(displayer)
# note_2.display(displayer)
notebook = Notebook([note_1, note_2])
notebook.display(displayer)
notebook.reorder([0, 1])
notebook.display(displayer)

## test sans crypto
# note_1.save()
# with open(note_1._id, "r") as f:
#     ok = json.load(f)
# ok = json.JSONEncoder().encode(ok)
# test = Note.from_json(ok)
# test.display(displayer)

## test avec crypto
key = Fernet.generate_key()
print(key)
encrypter = EncrypterSymmetric(key)
note_1.save(encrypter=encrypter)

# test = Note.from_encrypted_json(note_1._id, encrypter=encrypter)
# test.display(displayer)
