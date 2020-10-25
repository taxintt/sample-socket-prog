#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

def main():
    # prepare IPv4/TCP socket
    ## SOCK_STREAM: TCP connection (byte stream)
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Addressのreuseを許可する('Address already in use' の回避策)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

    host = 'localhost'
    port = 37564

    # set hostname and port for waiting connection
    serversocket.bind((host, port))
    # start listening
    serversocket.listen(128)

    try:
        while True:
            # server - accept()
            # try:
            clientsocket, (client_address, client_port) = serversocket.accept()
            print('New Client: {0}:{1}'.format(client_address,client_port))

            while True:
                try:
                    message = clientsocket.recv(1024)
                    print('Recv: {}'.format(message))
                except OSError:
                    break
                if len(message) == 0:
                    break

                # echo back - set received message to sent_message
                sent_message = message
                while True:
                    sent_len = clientsocket.send(sent_message)

                    if sent_len == len(sent_message):
                        break

                    sent_message = sent_message[sent_len:]
                print('Send back: {}'.format(message))
            
            clientsocket.close()
            print('Bye - client socket : {0}:{1}'.format(client_address, client_port))

    except KeyboardInterrupt:
        # close server socket
        serversocket.close()
        print('Bye - server socket : {0}:{1}'.format(host, port))

if __name__ == "__main__":
    main()