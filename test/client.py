import socket
import pickle


HOST = "an ip"
PORT = 'a port'


class Client:

    def __init__(self):
        self.s = socket.socket()
        try:
            self.s.connect((HOST, PORT))
            print(f'Client connected to: {HOST}:{PORT}')
            self.initRequestInfo()
        except ConnectionRefusedError:
            print(f'Client connection to {HOST}:{PORT} refused by server.')

    def initRequestInfo(self):
        self.s.send(b)
        fromServer = pickle.loads(self.s.recv(1024))
        print(fromServer)
        self.s.close()


if __name__ == "__main__":
    Client()
