#!/usr/bin/env python
"""inputs the message from the ternimal and sends it to the server
prints the "a reply received from:" along the server's IP address
"""
from __future__ import print_function
import socket
import sys
import argparse

host = 'localhost'


def client(port):
    sok = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ## getting IP of server
    ## I DON'T THINK THIS IS RIGHT FOR MY CURRENT GOAL SO GOTTA FIX THAT
    client_addr = (host, port)
    sok.connect(client_addr)

    ## actually sending the data to the server
    try:
        ## get data from terminal
        print("type message to send: ")
        message = input()
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
        print("A reply received from: " + client_addr)
    except socket.errno, e:
        print("Socket error: " + str(e))
    finally:
        sok.close()

if __name__ == '__main__':
    parsing = argparse.ArgumentParser(description ='echo server')
    parsing.add_argument('--port', action="store", dest="port", type=int, required=True)
    sure_args = parsing.parse_args()
    port = sure_args.port
    client(port)
