#!/usr/bin/env python
"""inputs the message from the ternimal and sends it to the server
prints the "a reply received from:" along the server's IP address
"""
from __future__ import print_function
import socket
import sys
import argparse

## host = 'localhost'


def client():
    sok = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ## getting IP of server
    host = socket.gethostname()

    ## SAME SPOT HERE, THIS IS WHERE THE PROBLEM IS hello
    client_addr = ('10.1.2.3', 12397)
    print("starting client on server: ")
    print(client_addr)

    sok.connect(client_addr)

    ## actually sending the data to the server
    try:
        ## get data from terminal
        print("type message to send: ")
        message = input()

        ## THIS IS WHERE THE ENCODING WILL HAPPEN
        ## for each char in message
            ## convert to int, add key value, convert to char

        ## send to echo server
        sok.sendall(message)

        ## look for response
        char_received = 0
        while char_received < len(message):
            receiving = sok.recv(1024)
            char_received += len(receiving)
            print("received " + receiving)

        ## required print statement for assignment
        ## THIS PRINTS THE WRONG THING CURRENTLY
        print("A reply received from: ")
        print(client_addr)
    except socket.errno, e:
        print("Socket error: " + str(e))
    finally:
        sok.close()

if __name__ == '__main__':
    client()
