import os
import json
from pathlib import Path
import nacl

from notes_api.exceptions import DecryptionError
from notes_api.encrypters.encrypter_symmetric_password import EncrypterSymmetricPassword


DIR = os.path.abspath(os.path.dirname(__file__))

def _get_encrypters():
    enc_1 = EncrypterSymmetricPassword(b"test")
    enc_2 = EncrypterSymmetricPassword(b"test", enc_1.salt)
    return enc_1, enc_2

def _get_clear_message():
    note_object = {"title": "Test",
                   "content": "test",
                   "tags": ["test"],
                   "datetime": "Thu Jan 16 15:44:01 2020",
                   "version": 1,
                   "color": "yellow",
                   "id": "2b4ef8a1cb804d4883fad2e0176ff16a",
                   "history": []}
    return json.JSONEncoder().encode(note_object)

def test_encryption_decryption_success():
    try:
        enc_1, enc_2 = _get_encrypters()
        clear_message = _get_clear_message()
        encrypted = enc_1.encrypt(clear_message)
        decrypted = enc_2.decrypt(encrypted)
        assertion = decrypted == clear_message
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test_save_salt_success():
    try:
        enc_1, _ = _get_encrypters()
        salt_path = Path(os.path.join(DIR, "test_salt"))
        enc_1.save_salt(salt_path)
        with open(salt_path, "rb") as file_:
            result = file_.read()

        assertion = result == enc_1.salt
        salt_path.unlink()
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test_encryption_decryption_file_salt_success():
    try:
        enc_1 = EncrypterSymmetricPassword(b"test")
        salt_path = Path(os.path.join(DIR, "test_salt"))
        enc_1.save_salt(salt_path)
        enc_2 = EncrypterSymmetricPassword(b"test", salt_path)
        clear_message = _get_clear_message()
        encrypted = enc_1.encrypt(clear_message)
        decrypted = enc_2.decrypt(encrypted)
        assertion = decrypted == clear_message
        salt_path.unlink()
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test_encryption_decryption_file_salt_error_salt_file():
    try:
        enc_1 = EncrypterSymmetricPassword(b"test")
        salt_path = Path(os.path.join(DIR, "test_salt"))
        enc_1.save_salt(salt_path)
        enc_2 = EncrypterSymmetricPassword(b"test", "salt_file_nonexisting")
    except FileNotFoundError:
        salt_path.unlink()
        assertion = True
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test_encryption_decryption_error_salt():
    try:
        enc_1 = EncrypterSymmetricPassword(b"test")
        enc_2 = EncrypterSymmetricPassword(b"test")
        clear_message = _get_clear_message()
        encrypted = enc_1.encrypt(clear_message)
        decrypted = enc_2.decrypt(encrypted)
        assertion = False
    except DecryptionError:
        assertion = True
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test_encryption_decryption_error_password():
    try:
        enc_1 = EncrypterSymmetricPassword(b"test")
        enc_2 = EncrypterSymmetricPassword(b"best", enc_1.salt)
        clear_message = _get_clear_message()
        encrypted = enc_1.encrypt(clear_message)
        decrypted = enc_2.decrypt(encrypted)
        assertion = False
    except DecryptionError:
        assertion = True
    except Exception as e:
        print(e)
        assertion = False

    assert assertion
