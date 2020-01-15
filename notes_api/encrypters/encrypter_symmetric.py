from cryptography.fernet import Fernet, InvalidToken

from .encrypter import Encrypter

class EncrypterSymmetric(Encrypter):

    def encrypt(self, note_json):
        encrypter = Fernet(self.key)
        encrypted = encrypter.encrypt(note_json.encode())
        return encrypted


    def decrypt(self, file_name):
        decrypter = Fernet(self.key)
        with open(file_name, "rb") as file_:
            encrypted = file_.read()

        try:
            decrypted = decrypter.decrypt(encrypted).decode()
        except InvalidToken:
            raise KeyError("The key used to decrypt is not correct.")
        return decrypted
