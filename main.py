#!/usr/bin/env python
from Scanner import Scanner
from Core import Core
import sys

def main():
    # Initialize the scanner with the input file
    S = Scanner(sys.argv[1])
    #write = Scanner(sys.argv[2])
    #w = open(write, "w")

    # Print the token stream
    while (S.currentToken() != Core.EOF):
        # Print the current token, with any extra data needed
        print(S.currentToken().name, end='')
        if (S.currentToken() == Core.ID):
            value = S.getID()
            print("[" + value + "]", end='');
        elif (S.currentToken() == Core.CONST):
            value = S.getCONST()
            print("[" + str(value) + "]", end='');
        print();
        # Advance to the next token
        S.nextToken();

    #w.close()

if __name__ == "__main__":
    main()
