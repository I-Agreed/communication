import socket
import CommBase


class CommClient:
    def __init__(self):
        super().__init__()
        self.serverIp = None
        self.serverPort = None

    def connect(self, ip, port):
        self.serverIp = ip
        self.serverPort = port
        self.socket.connect((ip, port))