import nacl.secret
import nacl.utils

from .encrypter import Encrypter

from notes_api.exceptions import DecryptionError

class EncrypterSymmetric(Encrypter):

    def __init__(self, private_key=None):
        if private_key is None:
            private_key = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)

        self.private_key = private_key
        self._box = nacl.secret.SecretBox(self.private_key)


    def encrypt(self, clear_message, nonce=None):
        encrypted = self._box.encrypt(clear_message.encode(), nonce=nonce)

        return encrypted


    def decrypt(self, cipher_message):
        try:
            decrypted = self._box.decrypt(cipher_message).decode()
        except nacl.exceptions.CryptoError:
            raise DecryptionError("The key used to decrypt is not correct.")

        return decrypted
