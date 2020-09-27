#!/usr/bin/env python
from Scanner import Scanner
from Core import Core
from Nonterminals import Program
import sys

def main():
    # Initialize the scanner with the input file
    S = Scanner(sys.argv[1])
    # Initialize the parser for the program with the input file
    P = Program(sys.argv[1])
    # run the parser (this creates the parse tree, checks it, and prints it)
    P.readFile(S, 0)


if __name__ == "__main__":
    main()
