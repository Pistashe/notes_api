import nacl.utils, nacl.secret, nacl.exceptions, nacl.pwhash

from .encrypter_symmetric import EncrypterSymmetric

from notes_api.exceptions import DecryptionError

class EncrypterSymmetricPassword(EncrypterSymmetric):
    def __init__(self, password, salt=None):
        kdf = nacl.pwhash.argon2i.kdf
        self.salt = nacl.utils.random(nacl.pwhash.argon2i.SALTBYTES) \
                    if salt is None else salt

        private_key = kdf(nacl.secret.SecretBox.KEY_SIZE, password, self.salt,
                          opslimit=nacl.pwhash.argon2i.OPSLIMIT_SENSITIVE,
                          memlimit=nacl.pwhash.argon2i.MEMLIMIT_SENSITIVE)
        EncrypterSymmetric.__init__(self, private_key)
