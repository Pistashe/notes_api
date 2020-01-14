class Encrypter():
    """
    Interface that must be implemented to correctly handle the encryption and
    decryption of a note.
    """
    def __init__(self, key):
        self.key = key


    def encrypt(self, file_name):
        """
        Encrypts a file
        """
        raise NotImplementedError("The encrypt function has not been "\
                                  "implemented.")

    def decrypt(self, file_name):
        """
        Decrypts a file
        """
        raise NotImplementedError("The encrypt function has not been "\
                                  "implemented.")
