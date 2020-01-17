import nacl.utils
from nacl.public import PrivateKey, Box
# from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives import serialization, hashes
# from cryptography.hazmat.primitives.asymmetric import rsa, padding

from .encrypter import Encrypter


class EncrypterAsymmetric(Encrypter):

    def __init__(self, private_key=None, public_key=None):
        if private_key is None:
            private_key = PrivateKey.generate()

        self.private_key = private_key
        if public_key is None:
            self._public_key = public_key
        else:
            self.public_key = public_key

    @property
    def public_key(self):
        return self._public_key

    @public_key.setter
    def public_key(self, public_key):
        self._public_key = public_key
        self._box = Box(self.private_key, self._public_key)


    @classmethod
    def from_file(cls, file_name, password=None):
        """
        Create an EncrypterAsymetric object from a private key serialized file.
        """
        with open(private_key, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=password,
                backend=default_backend()
            )
        return EncrypterAsymmetric(private_key)

    def encrypt(self, clear_message):
        encrypted = self._box.encrypt(clear_message.encode())
        return encrypted

    def decrypt(self, cipher_message):
        decrypted = self._box.decrypt(cipher_message).decode()
        return decrypted

    def save_private_key(self, file_name):
        pem = self.key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        with open(file_name, "wb") as key_file:
            key_file.write(pem)

    def save_public_key(self, file_name):
        public_key = self.key.public_key()
        pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        with open(file_name, "wb") as key_file:
            key_file.write(pem)

