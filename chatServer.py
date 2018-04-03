import socket
import time
import threading
import json
import uuid

host = '127.0.0.1'
port = 5000
MAX_MSG_SIZE = 32767

clientConnections = []

class CCCPException(BaseException):
    pass

class ClientConnection:
    def __init__(self, connection, thread):
        self.connection = connection
        self.thread = thread
        self.user_name = None
        self.user_id = None

def connection(conn):
    with conn:
        print('Connected by', addr)

        msg = read_validated_msg_from_socket(conn, "create-user")
        user_name = msg["name"]

        if (len(list(filter(lambda ccn: ccn.user_name == user_name, clientConnections))) > 0):
            raise CCCPException
        clientConnection = list(filter(lambda ccn: ccn.connection.fileno() == conn.fileno(), clientConnections))[0]
        clientConnection.user_name = user_name
        clientConnection.user_id = str(uuid.uuid4())

        conn.sendall(create_package("user-created", {"name": clientConnection.user_name, "id": clientConnection.user_id} ))

        while True:
            pass
            #if not data: break
            #conn.sendall(data)

def read_validated_msg_from_socket(conn, msg_type):
    size = conn.recv(2)
    size = int.from_bytes(size, "big")
    if (size > MAX_MSG_SIZE):
        raise CCCPException
    data = conn.recv(size)
    package = json.loads(data.decode())
    if (package["msg-type"] != msg_type):
        raise CCCPException
    return package["msg"]

def create_package(msg_type, content):
    content_json = json.dumps(content)
    msg_envelope = json.dumps({"msg-type": msg_type, "msg": content_json}).encode()
    msgb = len(msg_envelope).to_bytes(2, 'big') + msg_envelope
    return msgb


def broadcastToClients(msg):
    for client in clientConnections:
        client.connection.sendall(msg)

# entry point
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen(1)
    while True:
        conn, addr = s.accept()
        thread = threading.Thread(target = connection, args = (conn,))
        clientConnection = ClientConnection(conn, thread)
        clientConnections.append(clientConnection)
        thread.start()
