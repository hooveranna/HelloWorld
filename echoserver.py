#!/usr/bin/env python
"""
1- server receives messages from client.py
2- server numbers the messages
3- server prints out the message number, the message itself, and
	the IP address of the client
4- server replies the message back to the client
"""
from __future__ import print_function



# this handler will be run for each incoming connection in dedicated greenlet
def echoserver(port):
    sok = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sok.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    ## gives address of current server
    echo_addr = (host, port)

    sok.bind(echo_addr)

    ## NOT SURE BOUT THIS LINE
    sok.listen(backlog)

    while True:
        client, client_address = sok.accept()
        ## STEP 1
        data = client.recv()
        if data:

            ## STEP 3
            print("message number:" + )
            print("message: " + data)
            print("client address: " + client_address)
            ## STEP 4
            client.send(data)
        client.close()


if __name__ == '__main__':
    parsing = argparse.ArgumentParser(description ='echo server')
    parsing.add_argument('--port', action="store", dest="port", type=int, required=True)
    sure_args = parsing.parse_args()
    port = sure_args.port
    echoserver(port)
