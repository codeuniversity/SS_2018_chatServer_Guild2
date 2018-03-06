import socket
import threading
import time

alias = input("Name: ")
message = input(alias + "-> ")

def receving():
    while True:
        try:
            while True:
                data, addr = s.recvfrom(2048)
                print (str(data))
        except:
            pass

server = ('127.0.0.1', 5000)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#s.bind(('127.0.0.1', 0))
#s.setblocking(0)

def sending():
    while True:
        message = input(alias + "-> ")
        s.sendto(alias.encode('utf-8') + ": ".encode('utf-8') + message.encode('utf-8'), server)
        time.sleep(0.2)


thread1 = threading.Thread(target=receving)
thread1.start()

thread2 = threading.Thread(target=sending)
thread2.start()
