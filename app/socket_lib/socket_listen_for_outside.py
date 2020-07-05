#!/usr/bin/env python python3

import socket

def listen_outside_network(port):

    HOST = '172.17.0.2' # container
    # HOST = '192.168.161.129' # host
    PORT = port


    with socket.socket(socket.AF_INET , socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        s.bind((HOST , PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr )
            data = conn.recv(1024)
        #     break
        s.close
    print('Received', repr(data))
    return repr(data)

if __name__ == "__main__":
    listen_outside_network(6000)