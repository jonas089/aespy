import requests, json

class Message:
    def __init__(self, id, message, recipient, sender, iv):
        self.id = id
        self.message = message
        self.recipient = recipient
        self.sender = sender
        self.iv = iv
    
    def as_json(self):
        return json.dumps({
            "id": self.id,
            "message": self.message,
            "recipient": self.recipient,
            "sender": self.sender,
            "iv": self.iv
        })

class MsgClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.url = host + ':' + str(port)
        self.headers = {'Content-Type': 'application/json'}
    
    def register(self, publickey):
        return requests.post((self.url+'/register'), data=json.dumps({
            "publickey":publickey
        }), headers=self.headers).json()
    
    def put_message(self, message):
        return requests.post((self.url+'/put'), data=message.as_json(), headers=self.headers)

    def get_user(self, id):
        return requests.get((self.url+'/get/user/{}').format(id)).json()

    def get_messages(self, account):
        return requests.get((self.url+'/get/account/{}').format(account)).json()