#!/usr/bin/env python
from Core import Core

class Scanner:
    # Constructor should open the file and find the first token
    def __init__(self, filename):
        ## list of words in R1
        self.R_one = ["program", "begin", "new", "int", "define",
                        "endfunc", "class", "extends", "endclass",
                        "then", "else", "while", "endwhile", "endif",
                        "or", "input", "output", "end", "if"]
        ## list of symbols in R4
        self.R_four = ["==", "<=", ";", "(", ")", ",", "=", "!", "<", "+",
                        "-", "*"]
        ## dictionary of core values with their corresponding language strings
        self.core_dict = {
            "program": Core.PROGRAM,
            "begin": Core.BEGIN,
            "end": Core.END,
            "new": Core.NEW,
            "int": Core.INT,
            "define": Core.DEFINE,
            "endfunc": Core.ENDFUNC,
            "class": Core.CLASS,
            "extends": Core.EXTENDS,
            "endclass": Core.ENDCLASS,
            "if": Core.IF,
            "then": Core.THEN,
            "else": Core.ELSE,
            "while": Core.WHILE,
            "endwhile": Core.ENDWHILE,
            "endif": Core.ENDIF,
            "or": Core.OR,
            "input": Core.INPUT,
            "output": Core.OUTPUT,
            ";": Core.SEMICOLON,
            "(": Core.LPAREN,
            ")": Core.RPAREN,
            ",": Core.COMMA,
            "=": Core.ASSIGN,
            "!": Core.NEGATION,
            "==": Core.EQUAL,
            "<": Core.LESS,
            "<=": Core.LESSEQUAL,
            "+": Core.ADD,
            "-": Core.SUB,
            "*": Core.MULT,
        }

        file_in = open(filename, "r")
        temp = file_in.read()

        self.tokens = temp.split()
        self.index = 0
        self.currentTokenCore = Core.ID

        ## actaully finding the first token
        ## R1
        divided = self.removeKeyword(self.tokens[self.index])
        ## R3
        if (not divided) and self.tokens[self.index][0].isdigit():
            self.removeConstant(self.tokens[self.index],self.tokens[self.index][0])
            divided = True
        ## R4
        if not divided :
            divided = self.removeSpecial(self.tokens[self.index])
        ## R2
        if not divided :
            self.removeID(self.tokens[self.index])


    ### checkign to see if there is a keyword at the beginning of the current token
    ### if so, removing it from the token, and splitting that token into 2
    def removeKeyword(self, token):
        found = False
        for word in self.R_one:
            if token.startswith(word):
                ## just a keyword
                if (len(token) == len(word)):
                    found = True
                    ##change core value to the symbol
                    self.currentTokenCore = self.core_dict.get(word)
                ## keyword followed by R4
                elif (len(token) > len(word)):
                    after = token[len(word)]
                    if (after in self.R_four):
                        self.tokens.remove(token)
                        self.tokens.insert(self.index, token[len(word):])
                        self.tokens.insert(self.index, word)
                        found = True
                        ##change core value to the symbol
                        self.currentTokenCore = self.core_dict.get(word)
            ## not a keyword, an ID instead
        return found

    ### separating a constant from a token, and making sure it's not too high
    def removeConstant(self, token, firstnum):
        complete = False
        max = 5
        ## make sure to only read the relevant chars
        if len(token) < max:
            max = len(token)
        ## loop through chars in token
        for i in range(1, max):
            if token[i].isdigit() and (not complete):
                firstnum = firstnum + token[i]
            else:
                complete = True
                ## not trying to deal with any other cases here, so once
                ## the numbers are done, the string is split
        if int(firstnum) > 1023:
            # ERROR
            print("ERROR: INVALID CONSTANT. int [" + firstnum + "] is too high.")
            print("The max value for constants is 1023.")
            self.currentTokenCore = Core.EOF
            return 0
        ## splitting the string if we need to and adding both back to the list
        if len(firstnum) < len(token):
            self.tokens.remove(token)
            self.tokens.insert(self.index, token[len(firstnum):])
            self.tokens.insert(self.index, firstnum)
        ## change core value to constant
        self.currentTokenCore = Core.CONST
        return 0

    ### check for symbol at the beginning of the string and remove if needed
    def removeSpecial(self, token):
        complete = False
        for sym in self.R_four:
            if token.startswith(sym) and (not complete):
                ## split string if needed
                if len(sym) < len(token):
                    self.tokens.remove(token)
                    self.tokens.insert(self.index, token[len(sym):])
                    self.tokens.insert(self.index, sym)
                complete = True
                ##change core value to the symbol
                self.currentTokenCore = self.core_dict.get(sym)
        return complete

    ### with the assumption that the string doesn't start with anything in
    ### R1, R2, or R4, cut off the string for one ID
    def removeID(self, token):
        complete = False
        inde = 0
        for i in range(len(token)):
            ## it's a symbol
            if self.R_four.count(token[i]) > 0:
                complete = True
            ## another character to add to the ID
            elif token[i].isalnum() and not complete:
                inde = i
            ## char isn't in the library of allowed characters
            elif not complete:
                print("ERROR: INVALID TOKEN. char [" + token[i] +
                            "] is not included in this language.")
                self.currentTokenCore = Core.EOF
                return 0
            ## print("inde = " + str(inde))
        ## we've found the extent of the ID, see if we need to chop
        if (inde+1) < len(token):
            self.tokens.remove(token)
            self.tokens.insert(self.index, token[(inde+1):])
            self.tokens.insert(self.index, token[:(inde+1)])
        self.currentTokenCore = Core.ID
        return 0

    # nextToken should advance the scanner to the next token
    def nextToken(self):
        self.index = self.index + 1
        if self.index < len(self.tokens):
            ## R1
            ## print("curr token: " + self.tokens[self.index])
            divided = self.removeKeyword(self.tokens[self.index])

            ## R3
            if (not divided):
                starting = self.tokens[self.index]
                ## print("starting: " + starting)
                if self.tokens[self.index][0].isdigit():
                    self.removeConstant(self.tokens[self.index], starting[0])
                    divided = True
            ## R4
            if not divided :
                divided = self.removeSpecial(self.tokens[self.index])
            ## R2
            if not divided :
                self.removeID(self.tokens[self.index])
        ## end of file
        else:
            self.currentTokenCore = Core.EOF

        return 0

    # currentToken should return the current token
    def currentToken(self):
        return self.currentTokenCore

    # If the current token is ID, return the string value of the identifier
    # Otherwise, return value does not matter
    def getID(self):
        return self.tokens[self.index]

    # If the current token is CONST, return the numerical value of the constant
    # Otherwise, return value does not matter
    def getCONST(self):
        return int(self.tokens[self.index])
