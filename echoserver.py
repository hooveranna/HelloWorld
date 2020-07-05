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


def echoserver(port):
    sok = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sok.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    ## gives address of current server
    echo_addr = ('', port)

    sok.bind(echo_addr)

    ## backlog maximum is usually 5
    sok.listen(5)

    num_message = 0

    while True:
        client, client_address = sok.accept()
        ## STEP 1: server receives message from client.py
        data = client.recv(1024)
        if data:
            ## STEP 2: server numbers the message
            num_message = num_message + 1
            ## STEP 3: server prints out message, number, IP of client
            print("message number:" + num_message)
            print("message: " + data)
            print("client address: " + client_address)
            ## STEP 4: server replies message back to client
            client.send(data)
        client.close()


if __name__ == '__main__':
    parsing = argparse.ArgumentParser(description ='echo server')
    parsing.add_argument('--port', action="store", dest="port", type=int, required=True)
    ## this is where we're currently getting stuck
    sure_args = parsing.parse_args()
    port = sure_args.port
    echoserver(port)
