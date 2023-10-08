Exercise project - Diffie Hellman / secure peer-to-peer messaging

# 1. Diffie Hellman

```python
from crypto import SharedSecret
from constants import p, g
dh = SharedSecret(p, g)

dh.new_sk() # -> new secret key
dh.compute_pub(SOME_SECRET) # -> compute public key
dh.compute_secret(...) # -> compute shared secret
```

# 2. AES

```python
from crypto import Key, SharedSecret
from constants import iv
key = Key(shared_secret)
c = Cryptography(key)

c.encrypt(...) # -> encrypt with master key
c.decrypt(...) # -> decrypt with master key
```

# 3. Storage

## Filesystem

```python
filesystem = Filesystem(
    path_to_keystore, # where this client's keys are stored
    path_to_msgstore, # where message data is stored
    path_to_userstore # where userdata is stored
)
'''
Note: currently only one master key can be stored 
-> fix this in the near future
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
skfile.write_sk(sk) # write master key to keystore
skfile.read_sk() # read master key from keystore
```

### MsgFile
```python
msgfile = MsgFile(filesystem)
msgfile.store_msg(...) # store a new message
msgfile.get_messages_by_recipient(account) # get all messages sent to a specific recipient (stored messages are encrypted/decrypted with master key)
```

