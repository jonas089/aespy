import pickle, os

class Filesystem:
    def __init__(self, keystore, msgstore, users):
        self.keystore = keystore
        self.msgstore = msgstore
        self.users = users

    def initialise(self):
        if not os.path.exists(self.keystore):
            open(self.keystore, 'x')
        if not os.path.exists(self.msgstore):
            open(self.msgstore, 'x')
        if not os.path.exists(self.users):
            open(self.users, 'x')

class UserFile:
    def __init__(self, filesystem):
        self.filesystem = filesystem

    def add_user(self, id, user):
        data = None
        try:
            with open(self.filesystem.users, 'rb') as userstore:
                data = pickle.load(userstore)
                data[id] = user
        except Exception as empty:
            data = {
                id: user
            }
        with open(self.filesystem.users, 'wb') as userstore:
            pickle.dump(data, userstore)

    def get_user(self, id):
        with open(self.filesystem.users, 'rb') as userstore:
            data = pickle.load(userstore)
            return data[int(id)]
    
    def next_id(self):
        try:
            with open(self.filesystem.users, 'rb') as userstore:
                data = pickle.load(userstore)
                return len(data)
        except Exception as first:
            return 0

class SkFile:
    def __init__(self, filesystem):
        self.filesystem = filesystem

    def write_sk(self, sk):
        # Store private key in keystore
        with open(self.filesystem.keystore, 'w') as keystore:
            keystore.write(sk)

    def read_sk(self):
        with open(self.filesystem.keystore, 'r') as keystore:
            return keystore.read()

class MsgFile:
    def __init__(self, filesystem):
        self.filesystem = filesystem

    def store_msg(self, id, msg, recipient, sender, iv):
        data = None
        try:
            with open(self.filesystem.msgstore, 'rb') as msgstore:
                data = pickle.load(msgstore)
                data[id] = (msg, recipient, sender, iv)
        except Exception as empty:
            data = {
                id: (msg, recipient)
            }
        with open(self.filesystem.msgstore, 'wb') as msgstore:
            pickle.dump(data, msgstore)

    def get_messages_by_recipient(self, recipient):
        messages = []
        try:
            with open(self.filesystem.msgstore, 'rb') as msgstore:
                data = pickle.load(msgstore)
                for message in data.values():
                    print("MESSAGE: ", message)
                    if str(message[1]) == recipient:
                        print("IS EQUAL!")
                        messages.append(message)
        except Exception as e:
            return []
        return messages