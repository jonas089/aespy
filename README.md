Exercise project - Diffie Hellman / secure peer-to-peer messaging

# CLI EXAMPLE

⚠️ No safety guarantees, no `true randomness`, python code, proceed with caution!

Assume a message exchange between two parties "Alice" and "Bob".

Each party has their own `secret` and `public` key, e.g.:

```Python
    alice_secret = 145445439166789001181607796932907250698607586749406549218211058829454196917453710621971063937123275228434927674123049009907031200537398765123840222109709905581401635995989163610690432786381290141260837554163089202665360902523122139437304945518965234130662446895530697166363815201973129253416517122278452916795
    alice_public = 74735286538231079383450513075059563439294305061289349419938450200099314298432162810932375937468934335924065872582050029723735879227074200142613685952348844520188090093659262660575190525525414044532940352093674928319326741469948582490743763087921471053806836084850872944846164271681521324182852912260564065980
    bob_secret = 76859302922621079307590675176787672146792850475126205103299756545942660109261238126098068144572155266349754947917144850262900667711875314914346759949576048039576251190739860829327942643649503187321337237211547428869114340267956859264047326538377407475834233343968000095511999037266551945044467198144479885772
    bob_public = 171490573824433259871281292163394108066377440069176614266220938669762241831595251163988386442458573761445585996751700096433159098842982601277837997460784471159524573528766677358425528014848233511442255983948286395589437740738960121784764767356603190058674370989779318611683476427354828815784342995257615935269
```

To calculated a shared `master key`, that will be used for `encryption` and 
`decryption` of messages, `diffie hellman` is used:

```python
master_secret = pow(bob_public, alice_secret, P)
master_public = pow(G, alice_secret, P)
```

Where `P` is the prime modulo and `G` is a fixed generator point. Elliptic curve diffie hellman is not yet supported, but for the concept of this project basic DH is sufficient.

Before signing a message with the `master key`, the sender needs to calculate `random bytes`, that'll be unique for the communication session and will be appended to the message data (as a public parameter):

```python
iv = get_random_bytes(16)
```

These random bytes make derivation of the master key more difficult as messages accumulate.

⚠️ the `master key` is sometimes referred to as `shared_secret` in the code.

The `master key` is used as an `AES` key of form:

```python
aes_key = (self.shared_secret % n).to_bytes(32, byteorder='big')
```

where `n` is a big prime.

The `AES key` can be used to encrypt and decrypt messages:

❗ Messages need to be padded

```python    
block_size = 16
pad = block_size - (len(message) % block_size)
padded_message = message + bytes([pad]) * pad
cryptography.encrypt(padded_message, iv)
```

or

```python
cryptography.decrypt(cipher, iv)
```

To submit a message to the `service`, run it on localhost:

```bash
python3 service.py
```

and use the `client` to submit it to a public filestore:

```python
MsgClient.put_message(
    ...
)
```

Before submitting an encrypted message to the filestore, make sure both the sender and user are registered:

```python
MsgClient.register(
    ...
)
```

To query all messages submitted with `bob` as recipient:

```python
MsgClient.get_messages(bob_public)
```

this will return a list of all messages addressed to `bob`.

The sender is part of the message data, as well as the iv bytes used for encryption.

To decrypt the message:

```python
    decrypted_msg = cryptography.decrypt(stored_message, iv)
    pad_length = decrypted_msg[-1]
    unpadded_message = decrypted_msg[:-pad_length]
```

❗ Don't forget to remove padding from the message

ℹ️ see full python example in test.py

# Core functionality

## Diffie Hellman implementation

```python
from crypto import SharedSecret
from constants import p, g
dh = SharedSecret(p, g)

dh.new_sk() # -> new secret key
dh.compute_pub(SOME_SECRET) # -> compute public key
dh.compute_secret(...) # -> compute shared secret
```

## AES implementation

```python
from crypto import Key, SharedSecret
from constants import iv
key = Key(shared_secret)
c = Cryptography(key)

c.encrypt(...) # -> encrypt with master key
c.decrypt(...) # -> decrypt with master key
```

## Storage implementation

### Filesystem

```python
filesystem = Filesystem(
    path_to_keystore, # where this client's keys are stored
    path_to_msgstore, # where message data is stored
    path_to_userstore # where userdata is stored
)
'''
Note: currently only one private key can be stored per user,
master keys are derived for each peer to peer session
'''
```

### UserFile

```python
userfile = UserFile(filesystem)
userfile.add_user(...) # add a new user
userfile.get_user(id) # get user by id
userfile.next_id(id) # get current user height (used in "register")
```

### SkFile

```python
skfile = SkFile(filesystem)
skfile.write_sk(sk) # write private key to keystore
skfile.read_sk() # read private key from keystore
```

### MsgFile
```python
msgfile = MsgFile(filesystem)
msgfile.store_msg(...) # store a new message
msgfile.get_messages_by_recipient(account) # get all messages sent to a specific recipient (stored messages are encrypted/decrypted with master key)
```

