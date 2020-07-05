#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys,os

sys.path.append(os.path.join(os.path.dirname(__file__),'../socket_lib'))

from socket_listen_for_outside import *
from socket_listen_for_inner import *

values = ""

def run(net, port = None):
    while True:
        if(net == "in"):
            # print(sys.argv[0])
            values = listen_inner_network(port)
        elif(net == "out"):
        # serverrr(sys.argv[0])
            values = listen_outside_network(8002)
        else:
            print("Don't input tag( in or out ) not yet")
    print('put data into DNN model')
    print(values)

if __name__ == "__main__":
    run(sys.argv[1],sys.argv[2])
