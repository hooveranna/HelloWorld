#!/usr/bin/env python
"""inputs the message from the ternimal and sends it to the server
prints the "a reply received from:" along the server's IP address
"""
from __future__ import print_function
import socket
import sys
import argparse

## host = 'localhost'
integer_key_value = 3

def client():
    sok = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ## getting IP of server
    host = socket.getfqdn()
    print("host: " + host)
    ## SAME SPOT HERE, THIS IS WHERE THE PROBLEM IS hello
    client_addr = ('10.0.0.1', 12397)
    print("starting client on server: ")
    print(client_addr)

    sok.connect(client_addr)

    ## actually sending the data to the server
    try:
        ## get data from terminal
        message = raw_input("type message to send: ")
        message_temp = " "
        ## encoding message
        for i in range(0, len(message)):
            temp_int = ord(message[i]) + integer_key_value
            print("int value at "+str(i)+": "+str(temp_int) + ", char: " + chr(temp_int))
            message_temp = message.replace(message[i], chr(temp_int))
            message = str(message_temp)

        print("Encoded message: " + message)
        ## send to echo server
        sok.sendall(message)

        ## look for response
        char_received = 0
        while char_received < len(message):
            receiving = sok.recv(1024)
            char_received += len(receiving)
            print("received: " + receiving)

        echo, echo_address = sok.getpeername()
        ## required print statement for assignment
        print("A reply received from: ", echo)
    except socket.errno, e:
        print("Socket error: " + str(e))
    finally:
        sok.close()

if __name__ == '__main__':
    client()
