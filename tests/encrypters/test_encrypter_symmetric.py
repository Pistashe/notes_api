import json
import nacl

from notes_api.exceptions import DecryptionError
from notes_api.encrypters.encrypter_symmetric import EncrypterSymmetric



def _get_encrypter():
    return EncrypterSymmetric(b'\x99\x1c\xce\xad\xab\xa2\xed\xd9>\x9dZ_I\xf6'\
                              b'\xb8\x1e)c\xd4(\xf4\xf7[\x9c\xba\xfa\xed\xdb'\
                              b'\x0en\xbb\xa9')

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
    return b'!\xf7\x1db#pk{N\xf7l\xf4\x1a\xc5\xc3\x1c\xb4w\t\x02D\xe1l<\xbd'\
           b'\xcf\xe4e\xde\xb1\x17\xf9\\Q\xf5\xf9\x10i\x9fI\xed>\r\xc2\xb8'\
           b'\xd0\xe6@"U\xc3\x99\xfa\x04\x08\xbc\xd2^\xefl\xfdd\xb3\xdaq\x08'\
           b'\x8c\x13O\x9a\x9b\xc7\x88\xa2J*\xd0F\x86J\xdf\xd3\x84\xb8\xf4'\
           b'\xe4P\xec\x13\xd1s\x97\x1b\x97\x83\x85\xd6\xda\xcf\xeb>=\x88A*'\
           b'\x97\xa42\xc3N\x07]\x9b\x96\x00\x12=+\xd5\xe3\xc4ra\xde\xa5\xff'\
           b'\xf2\x9e\x96g\xfa\xd1\x8abu\xc7\xcf\xa2\x1e\x1c\x8ah\x89\xa2\x1a'\
           b'\xf5O=jd\xc3iw9_\xc4\x8a\x8c\xae\xfdP\xb3\x8f\xac\xc90\xbf\xd4'\
           b'\xcd\x9a\x1b \xf5\xd0\xa6\xb1\xf5\x99\x10f\xe1\xe0\x8c\xc7M\xe4'\
           b'+dF\x9a+\xd8\x94\x95\x12\xbap\xc8a\x04\x03\xbcb\xdf\xe0T\x96'\
           b'\x9f\xcba\xce\xb9\xcfL\xd7O^9T^\x1f0"\x13'

def test_encrypt_success():
    try:
        encrypter = _get_encrypter()
        clear_message = _get_clear_message()
        nonce = b'!\xf7\x1db#pk{N\xf7l\xf4\x1a\xc5\xc3\x1c\xb4w\t\x02D\xe1l<'
        result = encrypter.encrypt(clear_message, nonce=nonce)
        expected = _get_cipher_message()
        assertion = result == expected
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test_decrypt_success():
    try:
        encrypter = _get_encrypter()
        cipher_message = _get_cipher_message()
        result = encrypter.decrypt(cipher_message)
        expected = _get_clear_message()
        assertion = result == expected
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test_decrypt_error_decryption():
    try:
        encrypter = EncrypterSymmetric(b'\x99\x1c\xce\xad\xab\xa2\xed\xd9>'\
                                       b'\x9dZ_I\xf6\xb8\x1e)c\xd4(\xf4\xf7'\
                                       b'[\x9c\xba\xfa\xed\xdb\x0er\xbb\xa9')
        cipher_message = _get_cipher_message()
        result = encrypter.decrypt(cipher_message)
        assertion = False
    except DecryptionError:
        assertion = True
    except Exception as e:
        print(e)
        assertion = False

    assert assertion

def test_no_key():
    try:
        encrypter = EncrypterSymmetric()
        clear_message = _get_clear_message()
        result = encrypter.encrypt(clear_message)
        assertion = True
    except Exception as e:
        print(e)
        assertion = False

    assert assertion
