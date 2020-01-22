import nacl.utils, nacl.secret, nacl.exceptions, nacl.pwhash

from .encrypter_symmetric import EncrypterSymmetric

from notes_api.exceptions import DecryptionError

class EncrypterSymmetricPassword(EncrypterSymmetric):
    def __init__(self, password, salt=None):
        kdf = nacl.pwhash.argon2i.kdf
        try:
            with open(salt, "rb") as salt_file:
                self.salt = salt_file.read()
        except (TypeError, ValueError):
            self.salt = nacl.utils.random(nacl.pwhash.argon2i.SALTBYTES)
        except FileNotFoundError:
            if isinstance(salt, bytes):
                self.salt = salt
            else:
                raise FileNotFoundError("salt file not found.")

        private_key = kdf(nacl.secret.SecretBox.KEY_SIZE, password, self.salt,
                          opslimit=nacl.pwhash.argon2i.OPSLIMIT_SENSITIVE,
                          memlimit=nacl.pwhash.argon2i.MEMLIMIT_SENSITIVE)
        EncrypterSymmetric.__init__(self, private_key)

    def save_salt(self, file_name):
        with open(file_name, "wb") as salt_file:
            salt_file.write(self.salt)
