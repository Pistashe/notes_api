class Encrypter():
    """
    Interface that must be implemented to correctly handle the encryption and
    decryption of a note.
    """
    def __init__(self, key):
        self.key = key


    def encrypt(self, string):
        """
        Encrypts a file
        """
        raise NotImplementedError("The encrypt function has not been "\
                                  "implemented.")

    def decrypt(self, string):
        """
        Decrypts a file
        """
        raise NotImplementedError("The encrypt function has not been "\
                                  "implemented.")
