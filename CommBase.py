import socket


class CommBase:
    def __init__(self):
        self.socket = socket.socket()
        self.IP = socket.gethostbyname(socket.gethostname())

    def getStack(self):
        stack = self.recieveStack
        self.recieveStack = []
        return stack
