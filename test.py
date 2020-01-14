import json
from cryptography.fernet import Fernet
from encrypter_symmetric import EncrypterSymmetric

from note import Note
from displayer_ascii import DisplayerAscii


note_1 = Note("Test1", "Ceci est un test très simple qui ne fait qu'afficher "\
              "une note.", ["tag1", "tag2"], color="yellow")

note_2 = Note("Test2", "Ceci est une deuxième note, encore une fois très "\
              "simple", ["tag2", "tag3"], color="red")

displayer = DisplayerAscii()
note_1.display(displayer)
note_2.display(displayer)

## test snas crypto
# note_1.save()
# with open(note_1._id, "r") as f:
#     ok = json.load(f)
# ok = json.JSONEncoder().encode(ok)
# test = Note.from_json(ok)
# test.display(displayer)

## test avec crypto
key = Fernet.generate_key()
encrypter = EncrypterSymmetric(key)
note_1.save(encrypter=encrypter)

test = Note.from_encrypted_json(note_1._id, encrypter=encrypter)
test.display(displayer)
