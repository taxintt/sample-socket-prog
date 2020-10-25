import socket

def create_server_socket(host, port):
    # Specify address family(AF_INET：Ipv4) and the type of socket(SOCK_STREAM：TCP)
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # ソケットオプションでソケットの再利用フラグをONに設定
    # クライアントと通信途中で中断した場合同じIPアドレスとポートでバインドできるようにする
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return server_sock


def accept_loop(server_sock):
    while True:
        # 4.新しい接続要求を受け付ける
        # server_sock.accept()はブロッキング処理なので、接続が来るまでは次の処理に進まない
        print("start accepting...")
        conn, (client_host, client_port) = server_sock.accept()

        # ソケットのファイル記述子、新規に作成されたソケットにBindされたIPアドレス・ポートを表示する
        print('[FD:{}] Accept: {}: {}'.format(conn.fileno(), client_host, client_port))

        # ソケットからデータを受信し、結果をbytesオブジェクトで返す(一度に512bytes受信する)
        data = conn.recv(512)
        print('[FD:{}] Recv: {}'.format(conn.fileno(), data))

        # 送信されてきたデータを返す
        conn.send(data)

        # 5.接続を切断する
        conn.close()

if __name__ == '__main__':
    host, port = "localhost", 7777

    # 1.ソケットの作成
    server_sock = create_server_socket(host, port)

    # 2.接続を待ち受けるIPアドレスとポートを指定する
    server_sock.bind((host, port))

    # 3.接続要求の受け付けを開始する
    server_sock.listen(5)
    print('Server Run Port: {}'.format(port))

    try:
        accept_loop(server_sock)
    except KeyboardInterrupt:
        server_sock.close()