from cryptography.fernet import Fernet, InvalidToken

from .encrypter import Encrypter

from notes_api.exceptions import DecryptionError

class EncrypterSymmetric(Encrypter):

    def encrypt(self, clear_message):
        encrypter = Fernet(self.key)
        encrypted = encrypter.encrypt(clear_message.encode())
        return encrypted


    def decrypt(self, cipher_message):
        decrypter = Fernet(self.key)

        try:
            decrypted = decrypter.decrypt(cipher_message).decode()
        except InvalidToken:
            raise DecryptionError("The key used to decrypt is not correct.")

        return decrypted
