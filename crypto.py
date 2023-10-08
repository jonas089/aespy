from Crypto.Cipher import AES
from constants import n

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