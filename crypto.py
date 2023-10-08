from Crypto.Cipher import AES
from constants import n
import random

class Key:
    def __init__(self, shared_secret):
        self.shared_secret = shared_secret
    def derive_master_key(self):
        return (self.shared_secret % n).to_bytes(32, byteorder='big')


class Cryptography:
    def __init__(self, key):
        self.key = key
    def encrypt(self, message, iv):
        cipher = AES.new(self.key.derive_master_key(), AES.MODE_CBC, iv)
        return cipher.encrypt(message)
    def decrypt(self, message, iv):
        decrypt_cipher = AES.new(self.key.derive_master_key(), AES.MODE_CBC, iv)
        return decrypt_cipher.decrypt(message)

class SharedSecret:
    def __init__(self, p, g):
        self.p = p
        self.g = g
    def new_sk(self):
        return random.randint(1, self.p-1)
    def compute_pub(self, sk):
        return pow(self.g, sk, self.p)
    def compute_secret(self, sk, pub):
        return pow(pub, sk, self.p)