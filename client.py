import requests, json

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
    
    def put_message(self, id, message, recipient, sender, iv):
        return requests.post((self.url+'/put'), data=json.dumps({
            "id": id,
            "message": message,
            "recipient": recipient,
            "sender": sender,
            "iv": iv
        }), headers=self.headers)

    def get_user(self, id):
        return requests.get((self.url+'/get/user/{}').format(id)).json()

    def get_messages(self, account):
        return requests.get((self.url+'/get/account/{}').format(account)).json()