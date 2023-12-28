from crypto import Key, Cryptography, SharedSecret
from Crypto.Random import get_random_bytes
from hashlib import sha256
from constants import p, g
import os, ast, base64, time

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
#test_encrypt()
#clear()

def test_client():
    from client import Message, MsgClient
    dh = SharedSecret(p, g)
    alice_sk = 145445439166789001181607796932907250698607586749406549218211058829454196917453710621971063937123275228434927674123049009907031200537398765123840222109709905581401635995989163610690432786381290141260837554163089202665360902523122139437304945518965234130662446895530697166363815201973129253416517122278452916795
    alice_pk = 74735286538231079383450513075059563439294305061289349419938450200099314298432162810932375937468934335924065872582050029723735879227074200142613685952348844520188090093659262660575190525525414044532940352093674928319326741469948582490743763087921471053806836084850872944846164271681521324182852912260564065980
    bob_sk = 76859302922621079307590675176787672146792850475126205103299756545942660109261238126098068144572155266349754947917144850262900667711875314914346759949576048039576251190739860829327942643649503187321337237211547428869114340267956859264047326538377407475834233343968000095511999037266551945044467198144479885772
    bob_pk = 171490573824433259871281292163394108066377440069176614266220938669762241831595251163988386442458573761445585996751700096433159098842982601277837997460784471159524573528766677358425528014848233511442255983948286395589437740738960121784764767356603190058674370989779318611683476427354828815784342995257615935269
    iv = get_random_bytes(16)

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
    encrypted_msg = cryptography.encrypt(padded_message, iv)
    msgclient = MsgClient("http://127.0.0.1", 8000)
    
    print(msgclient.register(alice_pk))
    print(msgclient.register(bob_pk))

    print("User 0: ", msgclient.get_user(0))
    print("User 1: ", msgclient.get_user(1))

    _message = Message(
        "0x00",
        str(encrypted_msg),
        bob_pk,
        alice_pk,
        base64.b64encode(iv).decode('utf-8')
    )

    print(msgclient.put_message(_message).text)
    msg = msgclient.get_messages(bob_pk)[0]
    stored_message = ast.literal_eval(msg[0])
    decrypted_msg = cryptography.decrypt(stored_message, base64.b64decode(msg[3]))

    pad_length = decrypted_msg[-1]
    unpadded_message = decrypted_msg[:-pad_length]
    print("Read message: ", unpadded_message)
    
#clear()
test_client()
