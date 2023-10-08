from flask import Flask, request, jsonify
from storage import Filesystem, UserFile, SkFile, MsgFile
app = Flask(__name__)

filesystem = Filesystem("keystore.dat", "msgstore.dat", "userstore.dat")
filesystem.initialise()

@app.route('/get/account/<account>', methods=['GET'])
def get_messages(account):
    msgfile = MsgFile(filesystem)
    messages = msgfile.get_messages_by_recipient(account)
    return jsonify(
        messages
    )

@app.route('/get/user/<id>', methods=['GET'])
def get_user(id):
    userfile = UserFile(filesystem)
    return jsonify(
        userfile.get_user(id)
    )

@app.route('/put', methods=['POST'])
def put_message():
    data = request.get_json()
    msgfile = MsgFile(filesystem)
    msgfile.store_msg(data["id"], data["message"], data["recipient"], data["sender"])
    return jsonify(
        "[Debug] Message received."
    )

# id: publickey // all other DH params are handled by the backend as constants.
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    userfile = UserFile(filesystem)
    id = userfile.next_id()
    userfile.add_user(id, data["publickey"])
    return jsonify(
        "User created with ID: {}".format(id)
    )
    
if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8000)