import socket
from CommBase import CommBase
from Event import Event
import threading


class CommClient(CommBase):
    def __init__(self):
        super().__init__()
        self.serverIp = None
        self.serverPort = None
        self.recieveStack = []
        self.recieveThread = threading.Thread(target=self.recieveLoop)

    def connect(self, ip, port):
        self.serverIp = ip
        self.serverPort = port
        self.socket.connect((ip, port))
        self.recieveThread.start()

    def sendText(self, text):
        textBytes = bytes(text, "UTF-8")
        try:
            self.socket.send(textBytes)
        except socket.timeout:
            pass

    def sendEvent(self, **kwargs):
        textBytes = bytes(str(kwargs), "UTF-8")
        try:
            self.socket.send(textBytes)
        except socket.timeout:
            pass

    def recieve(self):
            text = self.socket.recv(1024)
            text = text.decode("UTF-8")
            try:
                if eval(text) == dict:
                    self.recieveStack.append(Event(**eval(text), type="kwarg"))
            except:
                self.recieveStack.append(Event(text=text, type="text"))

    def recieveLoop(self):
        while 1:
            self.recieve()