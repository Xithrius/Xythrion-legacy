# socket server demo

import socket

HOST = "an ip"      
PORT = 'a port'

with socket.socket() as s:
    s.bind((HOST, PORT))
    print("Server hostname:", HOST, "port:", PORT)

    s.listen()
    (conn, addr) = s.accept()
    while True:
        fromClient = conn.recv(1024).decode('utf-8')
        if fromClient == 'q':
            break
        print("From client:", addr)
        print("Received:", fromClient)

        mesg = input("Enter response: ")
        conn.send(mesg.encode('utf-8'))
