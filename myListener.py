#!/usr/bin/python
#Author: Phil Grimes @grap3_ap3	
#Python 2.7.1 (r271:86832, Apr 12 2011, 16:15:16) 
#[GCC 4.6.0 20110331 (Red Hat 4.6.0-2)] on linux2
#Date: 2011-11-19 17:22:13 
#Revision: 1 $
#Description: This is a basic listener. Opens a port on localhost and listens to connections, allows for logging.


#Import some stuff
import socket
import os

#Get user input for setup
myAddress = raw_input("Listener IP Address (ENTER for localhost): ")
myPort = raw_input("Listener Port (ENTER for 8008): ")
saveFile = raw_input("Do you want to save results?(Y/N): ")

#Prepare our input
if myAddress == '':										#If nothing entered for address prompt
    listenerAddress = 'localhost'								#set address to 'localhost'
else:												#If SOMETHING was entered at the address prompt
	listenerAddress = myAddress								#Set address to entry.
	
if myPort == '':										#If nothing entered at port prompt
	listenerPort = 8008									#set port to '8008'
else:												#If SOMETHING was entered at port prompt
	listenerPort = int(myPort)								#set port to entry.

#Check for/initialize log file
if saveFile == "Y":										#If "Y" entered at save file prompt
	print ("Saving results to log.txt")							#Print confirmation to screen
	if os.path.exists('log.txt'):								#If our log file exists
		file = open('log.txt', 'a')							#Open log in append mode
		file.write('New Log Entry: \n')							#write to log
		file.close()									#Close log
	else:											#If log file DOES NOT exist
		file = open('log.txt', 'w')							#Create and open the log file
		file.write('Begin Log: \n')							#Write to log
		file.close()									#Close file
elif saveFile == "N":										#If "N" entered at save file prompt
	print("Not Saving results!")								#Print confirmation to screen
else:												#If anything else was entered at save file prompt
	print("Incorrect entry!")								#Print error
	
		
		
#Set up socket
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)					#Instantiate a new socket
mySocket.bind((listenerAddress, listenerPort))							#bind socket to address, port
mySocket.listen(1)										#put socket into listen mode
conn, addr = mySocket.accept()									#accept incoming data from socket connections

#Advise of connection
print ("Listener connected on port ", listenerPort)						#Print to screen
print ("<CTRL>+C to quit.")									#Print to screen

#Pass data
while 1:											#Will continue as long as data is available (because 1 is TRUE)
	data = conn.recv(1024)									#data label given to upto 1024 bits received by the connection
	if not data: break									#If data is empty, break/stop
	#Are we saving?	
	if saveFile == "Y":									#If we're saving
		file = open('log.txt', 'a')							#open log file in append mode
		file.write("%s" % data)								#write data to log file
		print ("Alert Logged: ", data)							#write data to screen
		file.close()									#close file
	else:											#If we're NOT saving
		print ("Alert Recieved: ", data)						#Print data to screen

conn.close()											#close connection, kill socket