#!/usr/bin/env python
from Core import Core
from Scanner import Scanner

## parent class of all NonTerminals that allows them to print out the program
class NonTerminal:
    def __init__(self, name):
        self.name = name

    def printTabs(self, numTabs):
        for n in range(numTabs):
            print('\t', end = '')

    def printAndAdvance(self, scan, numTabs):
        print(scan.currentWord(), end = '')
        scan.nextToken()
    def printAndAdvanceNL(self, scan, numTabs):
        print(scan.currentWord())
        scan.nextToken()
        ##self.printTabs(numTabs)
    def printAndAdvanceSS(self, scan, numTabs):
        print(" " + scan.currentWord(), end = ' ')
        scan.nextToken()
    def printAndAdvanceSp(self, scan, numTabs):
        print(scan.currentWord(), end = ' ')
        scan.nextToken()

class Program(NonTerminal):
    ## you'll start by calling this
    ## it will set off the recursion to call all the other stuff
    def __init__(self, name):
        super().__init__(name)
        self.declseq = DeclarationSequence(name)
        self.statseq = StatementSequence(name)
    def readFile(self, scan, tab):
        vars = []
        curTab = tab
        ##skip current token cuz its Program
        if  scan.currentToken() is Core.PROGRAM:
            self.printAndAdvanceNL(scan, curTab)
        else:
            raise SyntaxError("error: PROGRAM token required to begin file")
            return
        ##print("in program class")
        ##print(scan.currentToken().name)
        curTab += 1
        scan = self.declseq.readFile(scan, curTab, vars)
        curTab -= 1
        ## skip current token cuz its BEGIN
        if scan.currentToken() is Core.BEGIN:
            curTab += 1
            self.printAndAdvanceNL(scan, curTab)
            ##print("made it through declaration, onto statements")
        else:
            raise SyntaxError("error: BEGIN token requried")
            return
        scan = self.statseq.readFile(scan, curTab, vars)
        ##print("in program, made it out of statement sequence")
        ## skip current token cuz its END
        if scan.currentToken() is Core.END:
            self.printAndAdvanceNL(scan, curTab)
        else:
            raise SyntaxError("error: END token required to end file")
            return
        if scan.currentToken() is Core.EOF:
            return
        else:
            raise SyntaxError("error: no code allowed past END token")
            return
        ##tell it that it's the end of the file somehow?
        return

class StatementSequence(NonTerminal):
    def __init__(self, name):
        super().__init__(name)
        self.state = Statement(name)
    def readFile(self, scan, tab, vars):
        scan = self.state.readFile(scan, tab, vars)
        if ((scan.currentToken() != Core.END) and
            (scan.currentToken() != Core.ENDIF) and
            (scan.currentToken() != Core.ENDWHILE) and
            (scan.currentToken() != Core.ELSE)):
            ##print("StatementSequence: " + scan.currentToken().name)
            scan = self.readFile(scan, tab, vars)
        return scan

class DeclarationSequence(NonTerminal):
    def __init__(self, name):
        super().__init__(name)
        self.decl = Declaration(name)
    def readFile(self, scan, tab, vars):
        curTab = tab
        if scan.currentToken() is not Core.EOF:
            ##print("in declaration sequence:")
            ##print(scan.currentToken().name)
            self.printTabs(curTab)
            scan = self.decl.readFile(scan, curTab, vars)
            if scan.currentToken() is not Core.BEGIN:
                scan = self.readFile(scan, curTab, vars)
        return scan

class Declaration(NonTerminal):
    def __init__(self, name):
        super().__init__(name)
        self.IDL = IDList(name)
    def readFile(self, scan, tab, vars):
        ## skip current token cuz it's int
        if scan.currentToken() is Core.INT:
            self.printAndAdvanceSp(scan, tab)
        else:
            print(scan.currentToken().name)
            raise SyntaxError("error: INT expected, given: " + scan.currentToken().name)
        scan = self.IDL.readFile(scan, tab, vars)
        ## skup current token cuz it's ;
        if scan.currentToken() is Core.SEMICOLON:
            self.printAndAdvanceNL(scan, tab)
        else:
            raise SyntaxError("error: semicolon required to close declaration")
        return scan

class IDList(NonTerminal):
    def __init__(self, name):
        super().__init__(name)
        self.hello = name
    def readFile(self, scan, tab, vars):
        if scan.currentToken() is Core.ID:
            ## skip current token cuz it's ID
            if scan.currentWord() in vars:
                raise SyntaxError("ERROR: declared same variable twice: " + scan.currentWord())
            vars.append(scan.currentWord())
            self.printAndAdvance(scan, tab)
            if scan.currentToken() is Core.COMMA:
                ## skip current token cuz it's COMMA
                self.printAndAdvanceSp(scan, tab)
                scan = self.readFile(scan, tab, vars)
        else:
            raise SyntaxError("Error: ID expected, given: " + scan.currentToken().name)
        return scan

class Statement(NonTerminal):
    def __init__(self, name):
        super().__init__(name)
        self.name = name
    def readFile(self, scan, tab, vars):
        self.printTabs(tab)
        if scan.currentToken() is Core.IF:
            iff = If(self.name)
            scan = iff.readFile(scan, tab, vars)
        elif scan.currentToken() is Core.WHILE:
            loop = Loop(self.name)
            scan = loop.readFile(scan, tab, vars)
        elif scan.currentToken() is Core.INPUT:
            inn = In(self.name)
            scan = inn.readFile(scan, tab, vars)
        elif scan.currentToken() is Core.OUTPUT:
            out = Out(self.name)
            scan = out.readFile(scan, tab, vars)
        elif scan.currentToken() is Core.INT:
            decl = Declaration(self.name)
            scan = decl.readFile(scan, tab, vars)
        elif scan.currentToken() is Core.ID:
            ass = Assignment(self.name)
            scan = ass.readFile(scan, tab, vars)
            ##print("made it out of assignment: " + scan.currentToken().name)
        else:
            ## ERROR TIME WOOOOOO
            print(scan.currentToken().name)
            raise SyntaxError("error: statement not began")
        return scan

class Assignment(NonTerminal):
    def __init__(self, name):
        super().__init__(name)
        self.expr = Expression(name)
    def readFile(self, scan, tab, vars):
        ## skip current token cuz it's ID
        if scan.currentToken() is Core.ID and scan.currentWord() in vars:
            self.printAndAdvance(scan, tab)
        else:
            raise SyntaxError("error: declared ID expected, given: " + scan.currentToken().name)
        ## skip current token cuz it's =
        if scan.currentToken() is Core.ASSIGN:
            self.printAndAdvanceSS(scan, tab)
        else:
            raise SyntaxError("error: = expected, given: " + scan.currentToken().name)
        scan = self.expr.readFile(scan, tab, vars)
        ## skip current token cuz it's ;
        if scan.currentToken() is Core.SEMICOLON:
            self.printAndAdvanceNL(scan, tab)
            ##print("just read ; in assign, now " + scan.currentToken().name)
        else:
            raise SyntaxError("error: ; expected, given: " + scan.currentToken().name)
        return scan

class In(NonTerminal):
    def __init__(self, name):
        super().__init__(name)
        self.hello = name
    def readFile(self, scan, tab, vars):
        ## skip current token cuz it's INPUT
        if scan.currentToken() is Core.INPUT:
            self.printAndAdvanceSp(scan, tab)
        else:
            raise SyntaxError("error: INPUT expected, given: " + scan.currentToken().name)
        ## skip current token cuz it's ID
        if scan.currentToken() is Core.ID:
            self.printAndAdvance(scan, tab)
        else:
            raise SyntaxError("error: ID expected, given: " + scan.currentToken().name)
        ## skip current token cuz it's ;
        if scan.currentToken() is Core.SEMICOLON:
            self.printAndAdvanceNL(scan, tab)
        else:
            raise SyntaxError("error: ; expected, given: " + scan.currentToken().name)
        return scan

class Out(NonTerminal):
    def __init__(self, name):
        super().__init__(name)
        self.expr = Expression(name)
    def readFile(self, scan, tab, vars):
        ## skip current token cuz it's OUTPUT
        if scan.currentToken() is Core.OUTPUT:
            self.printAndAdvanceSp(scan, tab)
        else:
            raise SyntaxError("error: OUTPUT expected, given: "+scan.currentToken().name)
        scan = self.expr.readFile(scan, tab, vars)
        ## skip current token cuz it's ;
        if scan.currentToken() is Core.SEMICOLON:
            self.printAndAdvanceNL(scan, tab)
        else:
            raise SyntaxError("error: ; expected, given: " + scan.currentToken().name)
        return scan

class If(NonTerminal):
    def __init__(self, name):
        super().__init__(name)
        self.cond = Condition(name)
        self.state_seq = StatementSequence(name)
    def readFile(self, scan, tab, vars):
        curTab = tab
        ##storing number of variables before loop
        insideVarNumber = len(vars)
        ## skip current token cuz it's IF
        if scan.currentToken() is Core.IF:
            self.printAndAdvanceSp(scan, curTab)
        else:
            raise SyntaxError("error: IF expected, given: " + scan.currentToken().name)
        scan = self.cond.readFile(scan, curTab, vars)
        print(" ", end = '')
        ## skip current token cuz it's THEN
        if scan.currentToken() is Core.THEN:
            curTab += 1
            self.printAndAdvanceNL(scan, curTab)
        else:
            raise SyntaxError("error: THEN expected, given: " + scan.currentToken().name)
        scan = self.state_seq.readFile(scan, curTab, vars)
        if scan.currentToken() is Core.ELSE:
            ## skip current token cuz it's ELSE
            self.printAndAdvanceNL(scan, curTab)
            scan = self.state_seq.readFile(scan, curTab, vars)
        ## skip current token cuz it's ENDIF
        ##print("right before ENDIFF check " + scan.currentToken().name)
        if scan.currentToken() is Core.ENDIF:
            curTab -= 1
            self.printTabs(curTab)
            self.printAndAdvance(scan, curTab)
        else:
            raise SyntaxError("error: ENDIF expected, given: " + scan.currentToken().name)
        ## skip current token cuz it's ;
        if scan.currentToken() is Core.SEMICOLON:
            self.printAndAdvanceNL(scan, curTab)
        else:
            raise SyntaxError("error: ; expected, given: " + scan.currentToken().name)
        ##removing vars declared inside if statement
        for i in range(len(vars)-insideVarNumber):
            vars.pop()
        return scan

class Loop(NonTerminal):
    def __init__(self, name):
        super().__init__(name)
        self.state_seq = StatementSequence(name)
        self.name = name
    def readFile(self, scan, tab, vars):
        curTab = tab
        ##storing number of variables before loop
        insideVarNumber = len(vars)
        ## skip current token cuz it's WHILE
        if scan.currentToken() is Core.WHILE:
            self.printAndAdvanceSp(scan, curTab)
        else:
            raise SyntaxError("error: WHILE expected, given: " + scan.currentToken().name)
        cond = Condition(self.name)
        scan = cond.readFile(scan, curTab, vars)
        print(" ", end = '')
        ## skip current token cuz it's BEGIN
        if scan.currentToken() is Core.BEGIN:
            curTab += 1
            self.printAndAdvanceNL(scan, curTab)
        else:
            raise SyntaxError("error: BEGIN expected, given: " + scan.currentToken().name)
        scan = self.state_seq.readFile(scan, curTab, vars)
        ## skip current token cuz it's ENDWHILE
        if scan.currentToken() is Core.ENDWHILE:
            curTab -= 1
            self.printTabs(curTab)
            self.printAndAdvance(scan, curTab)
        else:
            raise SyntaxError("error: ENDWHILE expected, given: "+scan.currentToken().name)
        ## skip current token cuz it's ;
        if scan.currentToken() is Core.SEMICOLON:
            self.printAndAdvanceNL(scan, curTab)
        else:
            raise SyntaxError("error: ; expected, given: " + scan.currentToken().name)
        ##removing vars declared inside loop
        for i in range(len(vars)-insideVarNumber):
            vars.pop()
        return scan

class Condition(NonTerminal):
    def __init__(self, name):
        super().__init__(name)
        self.name = name
    def readFile(self, scan, tab, vars):
        if scan.currentToken() is Core.NEGATION:
            ## skip current token cuz it's NEGATION
            self.printAndAdvance(scan, tab)
            ## skip current token cuz it's LPAREN
            if scan.currentToken() is Core.LPAREN:
                self.printAndAdvance(scan, tab)
            else:
                raise SyntaxError("error: if negation used, parentheses needed")
            scan = self.readFile(scan, tab, vars)
            ## skip current token cuz it's RPAREN
            if scan.currentToken() is Core.RPAREN:
                self.printAndAdvance(scan, tab)
            else:
                raise SyntaxError("error if parenteses open, it must be closed")
        else:
            cmpr = Comparison(self.name)
            scan = cmpr.readFile(scan, tab, vars)
            if scan.currentToken() is Core.OR:
                ## skip current token cuz it's OR
                self.printAndAdvanceSp(scan, tab)
                scan = self.readFile(scan, tab, vars)
        return scan

class Comparison(NonTerminal):
    def __init__(self, name):
        super().__init__(name)
        self.name = name
    def readFile(self, scan, tab, vars):
        expr = Expression(self.name)
        scan = expr.readFile(scan, tab, vars)
        ## skip current token cuz it's ==, <, or <=
        if ((scan.currentToken() is Core.EQUAL) or
            (scan.currentToken() is Core.LESSEQUAL) or
            (scan.currentToken() is Core.LESS)):
            self.printAndAdvanceSS(scan, tab)
        else:
            raise SyntaxError("error: ==, <=, < TOKEN expected")
        scan = expr.readFile(scan, tab, vars)
        return scan

class Expression(NonTerminal):
    def __init__(self, name):
        super().__init__(name)
        self.name = name
    def readFile(self, scan, tab, vars):
        term = Term(self.name)
        scan = term.readFile(scan, tab, vars)
        if ((scan.currentToken() is Core.ADD) or
            (scan.currentToken() is Core.SUB)):
            ## skip current token cuz it's PLUS or MINUS
            self.printAndAdvance(scan, tab)
            scan = self.readFile(scan, tab, vars)
        return scan

class Term(NonTerminal):
    def __init__(self, name):
        super().__init__(name)
        self.name = name
    def readFile(self, scan, tab, vars):
        fact = Factor(self.name)
        scan = fact.readFile(scan, tab, vars)
        if  scan.currentToken() is Core.MULT:
            ## skip current token cuz it's MULT
            self.printAndAdvance(scan, tab)
            scan = self.readFile(scan, tab, vars)
        return scan

class Factor(NonTerminal):
    def __init__(self, name):
        super().__init__(name)
        self.name = name
    def readFile(self, scan, tab, vars):
        if scan.currentToken() is Core.LPAREN:
            ## skip current token cuz it's LPAREN
            self.printAndAdvance(scan, tab)
            expr = Expression(self.name)
            scan = expr.readFile(scan, tab, vars)
            ## skip current token cuz it's RPAREN
            if scan.currentToken() is Core.RPAREN:
                self.printAndAdvanceSs(scan, tab)
            else:
                raise SyntaxError("error: ( expected, given: "+scan.currentToken().name)
        elif scan.currentToken() is Core.ID:
            if scan.currentWord() in vars:
                self.printAndAdvance(scan, tab)
            else:
                raise SyntaxError("ERROR: var used without declaring: "+scan.currentToken().name)
        elif ((scan.currentToken() is Core.ID) or
            (scan.currentToken() is Core.CONST)):
            ## skip current token cuz it's ID or CONST
            self.printAndAdvance(scan, tab)
        else:
            raise SyntaxError("error: That isn't in the syntax")
        return scan
