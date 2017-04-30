import socket

def listen():
    TCP_IP = '127.0.0.1'
    TCP_PORT = 9874
    BUFFER_SIZE = 1

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)
    conn, addr = s.accept()
    while 1:
        data = conn.recv(1)
        if data!=b'':
            print(data)
        if data==b'\xFF':
            break
        elif data == b'':
            conn, addr = s.accept()
    s.close()

listen()
