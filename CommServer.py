import socket
import CommBase


class CommServer:
    def __init__(self, maxClients=5):
        super().__init__()
        self.maxClients = maxClients

    def start(self, port):
        self.serverPort = port
        self.socket.bind((self.IP, port))
        self.listen(5)
