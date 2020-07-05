# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 22:14:14 2020

@author: Darmawan Utomo
"""


# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 18:52:46 2019

@author: TK1
"""

#import os
#os.environ["CUDA_VISIBLE_DEVICES"] = "7"


import datetime
import datetime as DtTm
import time
import socket
import numpy as np

from keras.models import model_from_json
from sklearn.metrics import mean_squared_error
from math import sqrt
#from socket_lib.client_for_inner import socket_connect_END
from DNN_to_BC import send_Data_to_BC


NO = 'AT_PC14I128_tanh_64_5_1'
# load json and fill model
json_file = open(NO +".json", 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
# load weights into new model
model.load_weights(NO +".h5")
print("Loaded model-" + NO + " and weight from disk")


model.summary() #or for layer in model.layers: print(layer.output_shape)


#INTERVAL = 200 = TIMESTEP
#current=0

import datetime as DtTm
send_to_BC = 60003
def prtTimeStamp(ts):
    print('H-'+str(ts[0])+';'+str(DtTm.datetime.fromtimestamp(ts[1]).strftime('%Y-%m-%d %H:%M:%S'))+';' 
          +str(ts[3])+';'+'%.3f'%ts[2]+';GateWayID;END',end=' ')
    anomaly_data = 'H-'+str(ts[0])+';'+str(DtTm.datetime.fromtimestamp(ts[1]).strftime('%Y-%m-%d %H:%M:%S'))+';' +str(ts[3])+';'+'%.3f'%ts[2]+';GateWayID;END'
    print()
    send_Data_to_BC(anomaly_data,send_to_BC)
    
                

    time.sleep(5)

TIMESTEP=200
KOLOM=200
#dt = np.dtype([('ID', np.unicode_, 16), ('TIMESTAMP', np.float64),('USAGE',np.float64),('STATUS',np.str,8)])
dt = np.dtype([('ID', np.int64), ('TIMESTAMP', np.float64),('USAGE',np.float64),('STATUS',np.str,20)])
ts_data = np.zeros((200), dtype=dt) #creating array of new datatype
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 60002        # Port to listen on (non-privileged ports are > 1023)
strdata=''
dw=''
##############CREATE INSTANCE RINGBUFFER SEBANYAK TIMESTEP

data4DNNin = np.zeros((200,KOLOM))
prediction_storage = np.zeros((365,KOLOM))
ccc = np.zeros((1,KOLOM)) # to get the USAGE DATA FROM TS-data
j=0 # to fill the TIMESTEP UPTO 200 AFTER THAT CHANGE TO DELETE-APPEND
i=0
ii=0
NUM_ANO = 0
print("server is ready to receive CONNECTION and DATA ....")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    
    with conn:
        print('Connected by', addr)
        data=''.encode()
        buf=''.encode()
        while True:
            tStart = time.time()
            data = conn.recv(1024)
            #TO EXIT FROM SERVER PROGRAM
            if (b'806410004' in data):
                print('EXPERIMENT-DONE')
                break
            #200 DATA FROM SMARTMETERS HAVE BEEN COLLECTED -> READY TO
            #FIRE THE INFERENCE ENGINE    
            if ( b'123Xcq' in data):
                data=''.encode()
                buf=''.encode()
                #for i in range(200):
                #    print(ts_data[i])
                #TEST THE ANOMALY
#==============================================================================
# BLOCK IF WE WANT START INFERENCING AFTER 200 ROWS OF DATA OR 1 TIMESTEP
#                if (j < TIMESTEP) : 
#                    for i in range(KOLOM): #copy from TS-DATA,USAGE ONLY
#                        ccc[0,i] = ts_data[i][2]
#                    data4DNNin[j] = ccc[0] # move to BLOCK TIMESTEPS
#                    j = j+1 #TO PROTECT SO THAT THE BUFFER MAXIMUM 200TSs
#                    print('REACH : ', j-1)
#                if (j == 200) : 
#                    print('BLOCK IS FULL, ready to INFER')
#                
#                if (j >= TIMESTEP):
#                    for i in range(KOLOM):
#                        ccc[0,i] = ts_data[i][2]
#                    data4DNNin= np.delete(data4DNNin, (0),axis=0)
#                    data4DNNin= np.append(data4DNNin, ccc,axis=0)
#                    print('INFER using DNN',j)
#                    j = j+1
                #=======================================================
                #GENERAL WAY, GET 1 ROW OF DATA->SLIDING->INFER
                #Move only the electic usage to 1 block input
                for i in range(KOLOM):
                    ccc[0,i] = ts_data[i][2]
                data4DNNin= np.delete(data4DNNin, (0),axis=0)
                data4DNNin= np.append(data4DNNin, ccc,axis=0)
                sample = data4DNNin[200-128:,:].T #128 bcs the implement model used 128 timestep
                sample = sample.reshape(200,128,1)
                print("normalize finish")

                #INFERENCING
                prediction_results = model.predict(sample, verbose=0)
                tEnd = time.time()
                print("prediction finish cost ",(tEnd-tStart)," sec")
                
                 
   
                                
                #SET 0.7 AS THRESHOLD, NORMALY 0.5 RUN THE ROC/PR GRAPH TO MAKE SURE
                pre_status = np.where (prediction_results > 0.5, 'ANOMALY','NORMAL')
                prediction_storage[j] = (np.where (prediction_results > 0.5, 1,0)).reshape(200)

                #print(prediction_results, pre_status, pre_status.shape, ts_data.shape)
                #UPDATE THE STATUS
                for i in range(KOLOM): #copy from TS-DATA,USAGE ONLY
                    ts_data[i][3] = pre_status[i,0]    #[0,i]
                
                #SEND TO THE BLOCK CHAIN
                #CHECK ONLY THE ANOMALY PRODUCE BY DNN PREDICTION MODEL
                loc,val = np.where(pre_status == 'ANOMALY')
                for i in loc:
                    NUM_ANO = NUM_ANO +1
                    print(NUM_ANO, end=' --> ');prtTimeStamp(ts_data[i]); print('',end=' | ');print()
                    
                    
                #TO SHOW THE TWO SAMPLE LINE OUTPUTS, PRINT AFTER 200 ROWS
                #if (j >= 200) :
                #    print('| ',j,end=' | '); prtTimeStamp(ts_data[0]); print('',end=' | '); prtTimeStamp(ts_data[1]); print('|');
                #    #print(j,ts_data[0], ts_data[1])
                j = j+1
                #break
            else :#COLLECT 200 DATA FROM SMARTMETERS
                if (b'END' in data) :
                    conn.sendall(buf+data)
                    buf=''.encode()
                    #print('Received', repr(data))
                    strdata = str(data)[2:-1] #to remove the 'b   '
                    dw = strdata.split(',')
                    #print(dw)
                    
                    #if i in range(200):
                    ii = int(dw[0]) #for capture the Meter-ID
                    ts_data[ii][0] = ii #ID-Meter
                    ts_data[ii][1] = float(dw[1]) #Timestamp()
                    ts_data[ii][2] = float(dw[2]) #Usages
                    ts_data[ii][3] = dw[3] #Status END means empty/original status
                    
                else:
                    buf= buf + data #+'-'.encode()
#%%