import socket
import sys
from time import clock
import threading
import queue


class ClientControl():
    def __init__(self, ip_addr, port):
        #create a tcp/ip socket
        self.sock = socket.socket(socket.AF_INET,
                             socket.SOCK_STREAM)
        #connect the socket to the port where the server is listening
        serv_addr = (ip_addr, port)
        print('connecting to {} port {}'.format(serv_addr[0],serv_addr[1]))
        self.sock.connect(serv_addr)
        self.requests = queue.Queue()
        threading.Thread(target=self.rec_data, args=()).start()

    def send_build_obj(self, msg):
        #send data
        byte_msg = msg.encode('utf-8')
        self.sock.sendall(byte_msg)

    def rec_data(self):
        while True:
            self.requests.put(self.sock.recv(1024).decode('utf-8'))

    def close(self):
        print("closing socket")
        self.sock.close()
        print("closing application")
