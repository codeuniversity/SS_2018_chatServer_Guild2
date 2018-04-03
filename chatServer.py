import socket
import time
import threading
import json

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

def connection(conn):
    with conn:
        print('Connected by', addr)
        size = conn.recv(2)
        size = int.from_bytes(size, "big")
        if (size > MAX_MSG_SIZE):
            raise CCCPException
        data = conn.recv(size)
        package = json.loads(data.decode())
        if (package["msg-type"] != "create-user"):
            raise CCCPException
        user_name = package["msg"]["name"]
        print(user_name)
        while True:
            pass
            #if not data: break
            #conn.sendall(data)



def broadcastToClients(msg):
    for client in clientConnections:
        client.connection.sendall(msg)

# entry point
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen(1)
    while True:
        conn, addr = s.accept()
        thread = threading.Thread(target = connection, args = (conn))
        clientConnection = ClientConnection(conn, thread)
        thread.start()
        clientConnections.append(clientConnection)
