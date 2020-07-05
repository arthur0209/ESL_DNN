#!/usr/bin/env python python3

import socket
import pickle
import socketserver
import json
import types
import string

HOST = '127.0.0.1'

data_array = None

#=================================================================================================================
"""**********************************************************************************************
*   Function : listen_inner_network                                                             *
*   Describe : if you want to receive only one data, just use this function, received data need *
*   include "END".                                                                              *
*   @Para (Int)     | port |  : The port which you want to listen.                              *
*   return (string)                                                                             *
**********************************************************************************************"""
def listen_inner_network(port):

    #     PORT = int(str(port))
    PORT = int(port)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)

        conn, addr = s.accept()
        print('Connected by', addr)
        
        with conn:
            
            data = conn.recv(4096)
            data_array = data.decode()
        print(data_array)

        # data = conn.recv((repr(data)))

    print('Received', data_array)
    return data_array
#--------------------------------------------------------------------------------------------------------------
"""******************************************************************************
*   Function : listen_control_message                                           *
*   Describe : this function will return 2 strings what the received string     *
*   split by ','.                                                               *
*   @Para (Int)     | port |  : The port which you want to connect.             *
*   @Para (string)  | message |  : The string which you want to send.           *
*   return (string), (string)                                                   *
******************************************************************************"""
def listen_control_message(port, message = None):

    with socket.socket(socket.AF_INET , socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        s.bind((HOST , port))
        s.listen()
        conn, addr = s.accept()
        
        with conn:
            print('Connected by', addr )
            data = conn.recv(1024)
        #     break
        s.close
    print('Received', repr(data))
    message = repr(data)[2:-1].split(',')
    print(message)
    return message[0], message[1]
#--------------------------------------------------------------------------------------------------------------
"""**********************************************************************************************
*   Function : listen_inner_network_END                                                           *
*   Describe : if you want to receive a lot of data, use this function, received data need      *
*   include "END" and it will stop when receive "final"                                         *
*   @Para (Int)     | port |  : The port which you want to listen.                              *
*   return (list)                                                                               *
**********************************************************************************************"""
def listen_inner_network_END(port):     #need received "END" and "final" to finish data transmit.

    #     PORT = int(str(port))
    PORT = int(port)
    buf = []

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:    #create socket use ipv4 and TCP/IP protocol.
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)     #set reuse addr = ture
        s.bind((HOST, PORT))

        s.listen(1)     #start to listen and wait for client connect.
        print("Server is already listen on port: "+ str(PORT) +" ...")


        conn, addr = s.accept()
        print('Connected by', addr)

        with conn:
            while True:
                data = conn.recv(1024)
                if "final".encode('utf-8') in data:
                    break
                elif "END".encode('utf-8') in data:
                    buf.append(data.decode('utf-8'))
                    #print("receive: " + data.decode('utf-8') +"\n")
        conn.close()
        s.close()
    return buf
#======================================================================================================
#======================================================================================================
# if __name__ == "__main__":
#     pass
    # listen_inner_network("Enter port")
    # listen_control_message(12345)
