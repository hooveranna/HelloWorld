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
    print("ill add a million of these, pre gethostname")
    ## gives address of current server
    host = socket.gethostname()
    ## THIS IS THE LINE WE'RE MESSING WITH
    echo_addr = ('', port)

    print("starting echo on server: ")
    print(echo_addr)
    print >> sys.stderr, 'starting up on %s port %s' % echo_addr
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
            ## STEP 3: server prints out message, number, IP of client
            print("message number:" + str(num_message))
            print("message: " + data)
            print("client address: ")
            print(client_address)
            ## STEP 4: server replies message back to client
            client.send(data)
        client.close()


if __name__ == '__main__':
    print("is this thing even on")
    parsing = argparse.ArgumentParser(description ='echo server')
    parsing.add_argument('--port', action="store", dest="port", type=int, required=True)
    ## this is where we're currently getting stuck
    sure_args = parsing.parse_args()
    port = sure_args.port
    print("are we at least doing this? port is " + str(port))
    echoserver(port)
