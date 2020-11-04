#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import multiprocessing
import threading
import time

def worker_thread(serverseocket):
    while True:
        clientsocket, (client_address, client_port) = serverseocket.accept()
        print('New client: {0}:{1}'.format(client_address, client_port))

        while True:
            try:
                message = clientsocket.recv(1024)
                print('Recv: {0} from {1}:{2}'.format(message, client_address, client_port))
            
            except OSError:
                break

            # 受信するメッセージが存在しない場合はbreak
            if len(message) == 0:
                break

            sent_message = message
            while True:
                # 送信したbytes数
                len_of_sent_message = clientsocket.send(sent_message)

                if len_of_sent_message == len(sent_message):
                    break
                sent_message = sent_message[len_of_sent_message:]

        clientsocket.close()
        print('Bye-Bye: {0}:{1}'.format(client_address, client_port))

def worker_process(serverseocket):
    NUMBER_OF_THREADS = 10

    for _ in range(NUMBER_OF_THREADS):
        thread = threading.Thread(target=worker_thread, args=(serverseocket,))
        thread.start()

    while True:
        time.sleep(1)

def main():
    serverseocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    serverseocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

    host, port = 'localhost', 37564
    serverseocket.bind((host,port))

    serverseocket.listen(128)

    NUMBER_OF_PROCESS = multiprocessing.cpu_count()

    for _ in range(NUMBER_OF_PROCESS):
        process = multiprocessing.Process(target=worker_process, args=(serverseocket,))

        process.daemon = True
        process.start()

    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()