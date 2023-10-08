import random

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