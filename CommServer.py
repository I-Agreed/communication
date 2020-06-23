import socket
from CommBase import CommBase
from Event import Event
import threading


class CommServer(CommBase):
    def __init__(self, maxClients=5):
        super().__init__()
        self.maxClients = maxClients
        self.connections = {}
        self.recieveStack = []
        self.recieveThread = threading.Thread(target=self.recieveLoop)
        self.acceptThread = threading.Thread(target=self.acceptLoop)


    def start(self, port):
        self.serverPort = port
        self.socket.bind((self.IP, port))
        self.socket.listen(self.maxClients)
        self.recieveThread.start()
        self.acceptThread.start()

    def handleConnection(self, new):
        self.connections[new[1]] = new[0]

    def sendText(self, text, target=""):
        textBytes = bytes(text, "UTF-8")
        if target:
            try:
                self.connections[target].send(textBytes)
            except socket.timeout:
                pass
        else:
            for i in self.connections:
                try:
                    self.connections[i].send(textBytes)
                except socket.timeout:
                    pass

    def sendEvent(self, target="", **kwargs):
        textBytes = bytes(str(kwargs), "UTF-8")
        if target:
            try:
                self.connections[target].send(textBytes)
            except socket.timeout:
                pass
        else:
            for i in self.connections:
                try:
                    self.connections[i].send(textBytes)
                except socket.timeout:
                    pass

    def recieve(self):
        for i in self.connections:
            text = self.connections[i].recv(1024)
            text = text.decode("UTF-8")
            try:
                if eval(text) == dict:
                    self.recieveStack.append(Event(**eval(text), type="kwarg"))
            except NameError:
                self.recieveStack.append(Event(text=text, type="text"))

    def recieveLoop(self):
        while 1:
            self.recieve()

    def acceptLoop(self):
        while 1:
            try:
                new = self.socket.accept()
                self.handleConnection(new)
            except socket.timeout:
                pass
