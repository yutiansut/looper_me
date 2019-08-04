import socket
from time import sleep

HOST = '127.0.0.1'  # The remote host
PORT = 12572  # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

from threading import Thread


def send():
    while True:
        s.send(b'Hello--hello--wee__d41d8cd98f00b204e9800998ecf8427e__')
        sleep(5)


def recv():
    while True:
        data = s.recv(4096)
        print("收到反馈 ", data.decode("utf-8"))


p = Thread(target=recv)
p.setDaemon(daemonic=True)
p.setName("recv")
p.start()

send()
# print('Received', repr(data))
