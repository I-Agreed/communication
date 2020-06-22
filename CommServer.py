import socket
import CommBase
import Event


class CommServer(CommBase):
    def __init__(self, maxClients=5):
        super().__init__()
        self.maxClients = maxClients
        self.connections = {}
        self.recieveStack = []

    def start(self, port):
        self.serverPort = port
        self.socket.bind((self.IP, port))
        self.listen(5)

    def handleConnection(self, socket):
        self.connections[socket[0]] = socket[1]

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
            except:
                self.recieveStack.append(Event(text=text, type="text"))