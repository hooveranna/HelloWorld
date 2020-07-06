#!/usr/bin/env python
"""
1- server receives messages from client.py
2- server numbers the message
3- server prints out the message number, the message itself, and
	the IP address of the client
4- server replies the message back to the client
"""
from __future__ import print_function
import socket
import sys
import argparse

## host = 'localhost'
integer_key_value = 3

def echoserver():
    sok = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ## sok.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("ill add a million of these, pre gethostname")
    ## gives address of current server
    ## host = socket.gethostname()

    ## THIS IS THE LINE WE'RE MESSING WITH
    echo_addr = ('', 12397)

    print("starting echo on server: ")
    print(echo_addr)
    sok.bind(echo_addr)
    num_message = 0
    print("listening for client now")
    ## backlog maximum is usually 5
    sok.listen(5)

    while True:
        client, client_address = sok.accept()
        ## STEP 1: server receives message from client.py
        data = client.recv(1024)
        if data:
            ## STEP 2: server numbers the message
            num_message = num_message + 1
            ## decoding the message
            data_decoded = None
            for i in range(0, len(data)):
                temp_int = ord(data[i]) - integer_key_value
                print("int value at "+str(i)+": "+str(temp_int) + ", char: " +chr(temp_int))
                data_decoded = data_decoded + chr(temp_int)

            ## THIS IS WHERE THE DECODING WILL HAPPEN
            ## for each char in data
                ## convert to int, subtract key value, convert to char

            ## STEP 3: server prints out message, number, IP of client
            print("message number: " + str(num_message))
            print("message: " + data_decoded)
            print("client address: ", client_address)
            ## STEP 4: server replies message back to client
            data_recoded = None
            for i in range(0, len(data_decoded)):
                temp_int = ord(data_decoded[i]) + integer_key_value
                print("int value at "+str(i)+": "+str(temp_int) + ", char: " +chr(temp_int))
                data_recoded = data_recoded + chr(temp_int)


            client.send(data_recoded)
        client.close()


if __name__ == '__main__':
    print("is this thing even on")
    ##parsing = argparse.ArgumentParser(description ='echo server')
    ##parsing.add_argument('--port', action="store", dest="port", type=int, required=True)
    ## this is where we're currently getting stuck
    ##sure_args = parsing.parse_args()
    ##port = sure_args.port
    ##print("are we at least doing this? port is " + str(port))
    echoserver()
