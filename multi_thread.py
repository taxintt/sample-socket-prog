#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import threading

def client_handler(clientsocket, client_address, client_port):
    while True:
        try:
            message = clientsocket.recv(1024)
            print('Recv: {0} from {1}:{2}'.format(message,client_address,client_port))
        except OSError:
            break

        if len(message) == 0:
            break

        sent_message = message
        while True:
            sent_len = clientsocket.send(sent_message)
            if sent_len == len(sent_message):
                break
            sent_message = sent_message[sent_len:]
        print('Send: {0} from {1}:{2}'.format(message,client_address,client_port))

    clientsocket.close()
    print('Bye-Bye: {0}:{1}'.format(client_address, client_port))


def print_call():
    print("making threads...")

def main():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

    host = 'localhost'
    port = 37564

    serversocket.bind((host,port))
    serversocket.listen(128)

    try:
        while True:
            clientsocket, (client_address, client_port) = serversocket.accept()
            print('New Client: {0}:{1}'.format(client_address, client_port))

            client_thread = threading.Thread(target=client_handler, args=(clientsocket,client_address,client_port))

            # if deletes main thread, delete sub thread
            client_thread.daemon = True

            # run thread
            client_thread.start()

            # run func for printing
            print_call()
    except KeyboardInterrupt:
        serversocket.close()

if __name__ == "__main__":
    main()