import socket
from time import time

HOST = '127.0.0.1'  # The remote host
PORT = 12572  # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

from threading import Thread


def recv():
    while True:
        s.send(b'Fancy--hello--wee__d41d8cd98f00b204e9800998ecf8427e__')
        timed = time()
        data = s.recv(4096)
        print(f"耗时: {(time() - timed) * 1000}")
        print("收到反馈 ", data.decode("utf-8"))


p = Thread(target=recv)
p.setDaemon(daemonic=True)
p.setName("recv")
p.start()


while True:
    pass

