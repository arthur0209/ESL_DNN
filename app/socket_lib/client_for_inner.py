#!/usr/bin/env python3

import socket
import sys
import time

HOST = '127.0.0.1' # container
#HOST = '192.168.112.133' # host
PORT = 8003
#==============================================================================================================================
"""******************************************************************************
*   Function : socket_connect_END                                               *
*   Describe : if you want to send a lot of data, you can use this function,but *
*   the string need include "END" in each send.                                 *
*   @Para (Int)     | port |  : The port which you want to connect.             *
*   @Para (list)    | data |  : The list with string which you want to send.    *
*   @Para (Int)     | times | : How many times which you want to send.          *  
******************************************************************************"""
def socket_connect_END(port,data,times):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:    #create socket use ipv4 and TCP/IP protocol.
        s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)    #set reuseable time to 0s.
        s.connect((HOST,port))      #start to connect and wait for client connect.

        TxData = []

        for i in range(0,times):
            TxData.append(data[i].encode('utf-8'))  #encode
        

        for i in range(0,times):
            s.sendall(TxData[i])
            print("send : " + TxData[i].decode('utf-8'))
            time.sleep(0.005)    #important 0.005 sec to avoid dataloss
        s.sendall("final".encode())
        s.close()
#--------------------------------------------------------------------------------------------------------------
"""******************************************************************************
*   Function : socket_connect_once                                              *
*   Describe : if you want to send only one data, just use this function, data  *
*   of string do not need include "END".                                        *
*   @Para (Int)     | port |  : The port which you want to connect.             *
*   @Para (string)  | data |  : The string which you want to send.              *
******************************************************************************"""
def socket_connect_once(port,data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:    #create socket use ipv4 and TCP/IP protocol.
        s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)    #set reuseable time to 0s.
        s.connect((HOST,port))      #start to connect and wait for client connect.

        TxData = data.encode()

        s.sendall(TxData)
        print("send : " + TxData.decode('utf-8'))

        s.close()
