from crypto import Key, Cryptography
from secret import SharedSecret
from Crypto.Random import get_random_bytes
from hashlib import sha256
from constants import p, g
import os

def test_encrypt():
    dh = SharedSecret(p, g)
    alice_sk = dh.new_sk()
    alice_pk = dh.compute_pub(alice_sk)
    bob_sk = dh.new_sk()
    bob_pk = dh.compute_pub(bob_sk)

    shared_secret = dh.compute_secret(alice_sk, bob_pk)
    check_secret = dh.compute_secret(bob_sk, alice_pk)
    assert(shared_secret == check_secret)

    key = Key(shared_secret)
    cryptography = Cryptography(key)

    # Padded message to encrypt
    message = "Hello".encode()
    block_size = 16
    pad = block_size - (len(message) % block_size)
    padded_message = message + bytes([pad]) * pad

    iv = get_random_bytes(16)
    print(iv)
    encrypted_msg = cryptography.encrypt(padded_message, iv)
    print("Encrypted Message: ", encrypted_msg)
    decrypted_msg = cryptography.decrypt(encrypted_msg, iv)
    # Determine and remove PKCS7 padding
    pad_length = decrypted_msg[-1]
    unpadded_message = decrypted_msg[:-pad_length]
    assert(unpadded_message == b"Hello")

def clear():
    try:
        os.remove('keystore.dat')
        os.remove('msgstore.dat')
        os.remove('userstore.dat')
    except Exception as exists:
        pass

def test_filesystem():
    from storage import Filesystem, UserFile, SkFile, MsgFile
    filesystem = Filesystem('keystore.dat', 'msgstore.dat', 'userstore.dat')
    userfile = UserFile(filesystem)
    skfile = SkFile(filesystem)
    msgfile = MsgFile(filesystem)

    userfile.add_user(0, "Jonas")
    userfile.add_user(1, "Admin")
    user = userfile.get_user(0)
    assert(user == "Jonas")

    skfile.write_sk("some_sk")
    sk = skfile.read_sk()
    assert(sk == "some_sk")

    msgfile.store_msg(0, "some_message", "some_recipient")
    msgfile.store_msg(1, "some_other_message", "some_other_recipient")
    msg_by_recipient = msgfile.get_messages_by_recipient("some_recipient")
    assert(msg_by_recipient == [('some_message', 'some_recipient')])
#test_filesystem()
test_encrypt()
clear()