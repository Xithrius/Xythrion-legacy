import threading
import socket
import sys
import pickle


HOST = "an ip"
PORT = 'a port'
MAX_AMOUNT = 50


class Server:

    def __init__(self, *args, **kwargs):
        try:
            if len(sys.argv[1:]) == 2:
                self.args = [int(x) for x in sys.argv[1:]]
            else:
                raise ValueError
        except ValueError:
            print('Usage: server.py number_of_clients seconds_for_timeout')
            return
        self.kwargs = kwargs
        self.s = socket.socket()
        self.s.bind((HOST, PORT))
        print(f'Server hostname: {HOST}:{PORT}')
        self.s.listen()
        self.initAThread()

    def initAThread(self):
        try:
            threads = []
            self.s.settimeout(self.args[1])
            for i in range(self.args[0]):
                (conn, addr) = self.s.accept()
                t = threading.Thread(target=self.findRequest, args=(conn,))
                threads.append(t)
            for t in threads:
                t.start()
            for t in threads:
                t.join()
        except socket.timeout:
            print(f'Connection timed out after {self.args[1]} seconds')
            return

    def findRequest(self, conn):
        print(conn)
        conn.send('Connection recieved')


if __name__ == "__main__":
    Server()
