#!/usr/bin/env python3

import socket
import sys

# HOST = '172.17.0.2' # container
HOST = '127.0.0.1'
#HOST = '192.168.112.133' # host
PORT = 12345

def socket_connect(data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        s.connect((HOST,PORT))
        
        RxData = data.encode('utf-8')
        print(RxData)
        if RxData:
            s.send(RxData)
        s.close()

socket_connect("3513")
