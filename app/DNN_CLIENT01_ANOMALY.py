# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 22:15:35 2020

@author: Darmawan Utomo
"""


# -*- coding: utf-8 -*-
"""
DNN CLIENT-SIMULATOR
Created on Tue Apr 16 18:50:26 2019

@author: TK1
"""
#import os
#os.environ["CUDA_VISIBLE_DEVICES"] = "6"

import time
import datetime as DtTm
import socket
import numpy as np
from numpy import savetxt, loadtxt

#from pandas import read_csv
#from pandas import DataFrame
#from pandas import concat




# load dataset and calculate the Anomaly

def convDatetime (string):
    return 0.0
#remove row-0, and coloum-0 : header and datetime
dataset1 = loadtxt('ResidentialProfiles_days.csv', delimiter=',',skiprows=1, converters = {0:convDatetime })
values = dataset1[:,1:]
values = values.astype('float32')
#scaled = values/np.max(values) #to normalize data to the max values per column
scaled = values/np.max(values, axis =0) #to normalize data to the max values per column #to normalize data to the max values per column
values = scaled

#ANOMALY BASED ON STANDARD DEVIATION

val_x, val_y = values.shape

mean3std = np.zeros((val_y),dtype=float)
mean_ax0 = np.mean(values[::,0:200], axis=0)
mstd_ax0 = np.std(values[::,0:200], axis=0)
mean3std = mean_ax0 + 3* mstd_ax0


xn = np.zeros((val_x, val_y))
for i in range(val_y):
    xn[::,i] = (values[::,i] > mean3std[i]).astype(int)

print("Check mean3std: ", np.sum(xn), val_x, val_y)    

ss=np.sum(xn,axis=0) #to find all the numbers of anomalous
loc_ss= np.where(ss!=0) #filtered out the normal data
xnT = xn.T
xn_filteredT = xnT[loc_ss]
xn_filtered = xn_filteredT.T
#serialized the xn_seri based on F order
vT = values.T
values_filteredT = vT[loc_ss]
values_filtered = values_filteredT.T

xn_seri = xn_filtered.reshape((xn_filtered.shape[0]*xn_filtered.shape[1],1), order='F')
values_seri = values_filtered.reshape((values_filtered.shape[0]*values_filtered.shape[1],1), order='F')
print(values_filtered.shape, xn_filtered.shape, xn_seri.shape, values_seri.shape, mean_ax0.shape, mstd_ax0.shape, mean3std.shape)

loc_ss= np.where(ss==0) #select in the normal data
xnT = xn.T
xn_normalT = xnT[loc_ss]
xn_normal = xn_normalT.T
#serialized the xn_seri based on F order
vT = values.T
values_normalT = vT[loc_ss]
values_normal = values_normalT.T

xn_normal_seri = xn_normal.reshape((xn_normal.shape[0]*xn_normal.shape[1],1), order='F')
values_normal_seri = values_normal.reshape((values_normal.shape[0]*values_normal.shape[1],1), order='F')
print(values_normal.shape, xn_normal.shape, xn_normal_seri.shape, values_normal_seri.shape)


INTERVAL = 200

NUM_OF_COLOMNS = 200
TIMESTEP=200
test = values

# split into input and outputs and arrange to consider INTERVAL
tsx, tsy = test, xn # xn= ground truth, test is the dataset contain electricity consumption


HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 60002        # The port used by the server

##############CREATE INSTANCE RINGBUFFER SEBANYAK TIMESTEP
KOLOM=200
current=0
data = np.zeros((200,KOLOM))
dt = np.dtype([('ID', np.unicode_, 16), ('TIMESTAMP', 'datetime64[m]'),('USAGE',np.float64),('STATUS',np.str,8)])
x = np.array([(199, '1979-03-22T15:00', 34.56, 'BLANK')], dtype=dt)

jmlROW = 364
#############READ ONE ROW, SPLIT INTO KOLOM-200


dt = np.dtype([('ID', np.int64), ('TIMESTAMP', np.float64),('USAGE',np.float64),('STATUS',np.str,8)])
x = np.zeros((200), dtype=dt) #creating array of new datatype
#%
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    for iFILL_MAX in range(jmlROW+1):
        for i in range(KOLOM):
            id = str(i)
            ts = str(DtTm.datetime.now().timestamp())
            usg = str(tsx[iFILL_MAX][i])
            paket = id + ',' + ts + ','+ usg + ',' +'END'
            s.sendall(paket.encode())
            #s.sendall('END'.encode())
            data = s.recv(1024)
            print('Received', repr(data))
            strdata = str(data)[2:-1] #to remove the 'b   '
            dw = strdata.split(',')
            x[i][0] = int(dw[0])
            x[i][1] = float(dw[1])
            x[i][2] = float(dw[2])
            x[i][3] = dw[3]
            print(str(x[i][0])+','+str(DtTm.datetime.fromtimestamp(x[i][1]).strftime('%Y-%m-%d %H:%M:%S'))+','+str(x[i][2])+','+str(x[i][3]))
            #strdata = str(data).split(',')

        s.sendall('123Xcq'.encode()) #send code setelah 200 kali kirim
    s.sendall('806410004'.encode()) #send EXIT code


#datetime.datetime.now().timestamp()
#Out[33]: 1555424796.230251
#datetime.datetime.fromtimestamp(datetime.datetime.now().timestamp()).strftime('%Y-%m-%d %H:%M:%S')
#Out[34]: '2019-04-16 22:28:08'

#%%
