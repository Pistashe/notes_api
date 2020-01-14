from cryptography.fernet import Fernet

from encrypter import Encrypter

class EncrypterSymmetric(Encrypter):

    def encrypt(self, note_json):
        encrypter = Fernet(self.key)
        encrypted = encrypter.encrypt(note_json.encode())
        return encrypted


    def decrypt(self, file_name):
        decrypter = Fernet(self.key)
        with open(file_name, "rb") as file_:
            encrypted = file_.read()

        decrypted = decrypter.decrypt(encrypted).decode()
        return decrypted
