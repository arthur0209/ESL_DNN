#client for DNN container | DNN send data to BC
#from Socket_DNNtoBC_lib import SendDatatoBC

from socket_lib.client_for_inner import socket_connect_END
#from socket_lib.client_for_inner_1 import socket_connect
import time
import pickle
import argparse

HOST = "127.0.0.1"
PORT = 60002
# Server_address = "127.0.0.1" #Server ip address.
# Server_PORT = 1234    #Server Port number.
def send_Data_to_BC(data,port):
	 n = 200
	 str_arr = []

	 #test_string = "H-;2019-12-05,00:00:00;N;;GateWayID;END"    #split by ';'
	 test_string = []
	 test_string.append(data)
	
	 ''' 
	 # create data m*n array
	 for i in range(0,200): #here '200' need to find meter number file
	  str_arr.append(test_string.replace("H-","H-"+str(i+1)))

	 #print(str_arr)  #show the simulate data format.
	 #-----------------------------------------------------------------
	 '''
	 t0 = time.time()  #calculate the time about tranmission all data

	 #test_string = pickle.dumps(test_string)
	 socket_connect_END(port,test_string,len(test_string))
	 # SendDatatoBC(my_bytes,200)

	 print("total time : " + str(time.time() - t0))  #calculate the time about tranmission all data
#====================================================================================================
#====================================================================================================
if __name__ == "__main__":
	 parser = argparse.ArgumentParser(description='Please enter port: ')
	 parser.add_argument("-p", "--port", type=str, default="NULL", help='Enter port number')

	 args = parser.parse_args()

	 if args.port !="NULL":
	  senddata200(int(args.port))