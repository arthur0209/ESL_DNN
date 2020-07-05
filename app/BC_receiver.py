#server for BC container
import json
from socket_lib.socket_listen_for_inner import listen_inner_network_END

# our_address = "127.0.0.1"	#our ip address.
# our_PORT = 1234						#our Port number.
METER_AMOUNT = 200
PORT = 60003
def BC_receiver_run(flag, port):
	buf = []  #define a buffer for receive data.

	times = 0;		#calculate how many of data.

	total_data =[]			#storage total receive data(200).
	total_data_json =[]			#transform data format to json.
	print("BC thread start!")
	print(port)

	while True:
		total_data = listen_inner_network_END(port)
		if "ESC" in total_data[0]:
			print("Stoped!")
			break			#quit thread in a safe method.
		#********************************************************************************************   
		total_data_json.clear()

		#deal with datas to BC cmd format
		for i in range(0,len(total_data)):
			total_data_split = total_data[i].split(';')		#split string

			total_data_json.append('\'{\"Args\":[\"save_data\",\"'+ total_data_split[0] +'\",\"'+ total_data_split[1] +'\",\"'+ total_data_split[2] +'\",\"'+ total_data_split[3] +'\",\"'+total_data_split[4]+'\"]}\'')
			#print(total_data_json[i])

			#-----------finish transfrom---------------------
			total_data_split.clear()		#clear buffer 
		
		total_data.clear()			#clear buffer 	
		#print(len(total_data_json)

		#---------------do BC transaction----------------------------
		print("BC record data : ")
		print(total_data_json[0])

		"""record_file = open("BC_record.txt","w+")
		
		for i in range(0,len(total_data_json)):
			record_file.write(total_data_json[i]+"\n")
		
		record_file.close()

		print("record finished!")"""
		#------------------------------------------------------------
#=========BC store format=============================================================
"""
	'{"Args":["save_data","H-200","2019-12-05,00:00:00","N","","GateWayID"]}'   #the format of BC cmd 
"""
#-------------------------------------------------------------
"""
	'{"Args":["save_data","H-200","2019-12-05,00:00:00","N","60.5","GateWayID"]}'   #the format of BC cmd 
"""
#=====================================================================================
BC_receiver_run(0,PORT)