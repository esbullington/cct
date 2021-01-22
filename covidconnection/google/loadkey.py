import os
from covidconnection.google.rsa.key import PrivateKey


# this class holds a private RSA key
class LoadKey:

    # loads key
    def __init__(self, key_filename):
        self.key = self.load_key(key_filename)

    # returns the private key
    def private_rsa_key(self):
        return self.key

    # loads a private RSA key
    @staticmethod
    def load_key(filename):
        try:
            with open(filename) as f:
                return PrivateKey.load_pkcs1(f.read())
        except Exception as exc:
            print("Error opening config file: {}".format(str(exc)))
