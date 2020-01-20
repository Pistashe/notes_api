import json
import nacl

from notes_api.exceptions import DecryptionError
from notes_api.encrypters.encrypter_asymmetric import EncrypterAsymmetric



def _get_encrypters():
    enc_2 = EncrypterAsymmetric(b'\xbaD+\x8d\x1cO\xd0\xcf\x99\x1eFj\x077\xdb'\
                                b'\xe7o\xc3\x10\x02U\xcc\xe4\x11\xd2\xf3\x0fy'\
                                b'\xd8\xa1~i')
    enc_1 = EncrypterAsymmetric(b'\xbaC+\x8d\x1cO\xd0\xcf\x99\x1eFj\x077\xdb'\
                                b'\xe7o\xc3\x10\x02U\xcc\xe4\x11\xd2\xf3\x0fy'\
                                b'\xd8\xa1~i',
                                enc_2.private_key.public_key)
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

def _get_cipher_message():
    return b'!\xf7\x1db#pk{N\xf7l\xf4\x1a\xc5\xc3\x1c\xb4w\t\x02D\xe1l<;\xc6'\
           b'>*\x86\x98dM\x86.\xa7I\xee\xb6\xe0D\x1c\x88"n\xc0\xb9<\xaf!\xf6'\
           b'\xd3\xa6\xfd\xd3\xc3\x082b\xb6)\x93\xb3\x90\x88!\x9c\x17\xa3\xcf'\
           b'u\xe0\xcc\xd3\xfb\x93\x8a\xbf\x96\x17\x8e0\x8b0\xc6^\xff\x90\x81'\
           b'P(\xcd\xf6\x08#\xa1[1C\xbe\xfc\xd5M\x18\x90\n\x8fIs)\xc2\xd3(;'\
           b'\xb3\xa1\xa3\xdd\xc1\xa7\xbbh\x9a\xe2\xd9\xd4\xf9VT\xf4\xb2\x8c'\
           b'Ip16\x88\xe3e\x0f\xae\x99!\x8da\xe0x\x1f\x8bk\xc0Q\xa4\xdd\x94'\
           b'\xda\xf3Ik\xdct\x02\xf8\xd8\tB\x16\xefQj\xa6Fx\xf1\x91w\xfa\xaf'\
           b'\x90L\xc8Q\xf6\x90\x88&\x80\rt\xd2\xb5\x96\x9b\td)\xdc\x98\x96'\
           b'\x92\xc3\xef\xeb\x9f\xe0\x9e%\xc3\xf0\r\xc5e\xe1\xce\xb1G\xb4'\
           b'\xb7$c\xe3\n\xcc`\xc9'

def test_encrypt_success():
    try:
        enc_1, _ = _get_encrypters()
        clear_message = _get_clear_message()
        nonce = b'!\xf7\x1db#pk{N\xf7l\xf4\x1a\xc5\xc3\x1c\xb4w\t\x02D\xe1l<'
        result = enc_1.encrypt(clear_message, nonce=nonce)
        expected = _get_cipher_message()
        assertion = result == expected
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test_decrypt_success():
    try:
        enc_1, _ = _get_encrypters()
        cipher_message = _get_cipher_message()
        result = enc_1.decrypt(cipher_message)
        expected = _get_clear_message()
        assertion = result == expected
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test_decrypt_error_key_enc_1():
    try:
        enc_1 = EncrypterAsymmetric(b'\xbaD+\x8d\x1cO\xd0\xcf\x99\x1eFj\x077\xdb'\
                                    b'\xe7o\xc3\x10\x02U\xcc\xe4\x11\xd2\xf3\x0fy'\
                                    b'\xd8\xa1~i')
        enc_2 = EncrypterAsymmetric(b'\xbaD+\x8d\x1cO\xd0\xcf\x99\x1eFj\x077\xdb'\
                                    b'\xe7o\xc3\x10\x02U\xcc\xe4\x11\xd2\xf3\x0fy'\
                                    b'\xd8\xa1~i')
        enc_1.public_key = enc_2.private_key.public_key
        cipher_message = _get_cipher_message()
        result = enc_1.decrypt(cipher_message)
        assertion = False
    except DecryptionError:
        assertion = True
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test_decrypt_error_key_enc_2():
    try:
        enc_1 = EncrypterAsymmetric(b'\xbaJ+\x8d\x1cO\xd0\xcf\x99\x1eFj\x077\xdb'\
                                    b'\xe7o\xc3\x10\x02U\xcc\xe4\x11\xd2\xf3\x0fy'\
                                    b'\xd8\xa1~i')
        enc_2 = EncrypterAsymmetric(b'\xbaK+\x8d\x1cO\xd0\xcf\x99\x1eFj\x077\xdb'\
                                    b'\xe7o\xc3\x10\x02U\xcc\xe4\x11\xd2\xf3\x0fy'\
                                    b'\xd8\xa1~i')
        enc_1.public_key = enc_2.private_key.public_key
        cipher_message = _get_cipher_message()
        result = enc_1.decrypt(cipher_message)
        assertion = False
    except DecryptionError:
        assertion = True
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test_no_key():
    try:
        enc_1, enc_2 = EncrypterAsymmetric(), EncrypterAsymmetric()
        enc_1.public_key = enc_2.private_key.public_key
        enc_1.public_key
        clear_message = _get_clear_message()
        result = enc_1.encrypt(clear_message)
        assertion = True
    except Exception as e:
        print(e)
        assertion = False

    assert assertion
