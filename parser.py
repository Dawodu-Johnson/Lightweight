import sys
from lex import *


# checks if the code matches the rules (grammar)
class Parser:
    def __init__(self, lexer, emitter):
        self.lexer = lexer
        self.emitter = emitter

        self.symbols = set()  # variables declared so far

        self.curToken = None
        self.peekToken = None
        self.nextToken()
        self.nextToken()

    # validates if current token matches
    def checkToken(self, kind):
        return kind == self.curToken.kind

    # validates if the next token matches
    def checkPeek(self, kind):
        return kind == self.peekToken.kind

    def match(self, kind):

        if not self.checkToken(kind):
            self.abort("Expected " + kind.name + ", got " + self.curToken.kind.name)
        self.nextToken()

    def nextToken(self):
        self.curToken = self.peekToken
        self.peekToken = self.lexer.get_token()

    def abort(self, message):
        sys.exit("Error. " + message)

    # program ::= { statement }
    def program(self):
        print("PROGRAM")

        self.emitter.headerLine("#include<iostream>")
        self.emitter.headerLine("using namespace std;\n")
        self.emitter.headerLine("int main() {")

        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()

        while not self.checkToken(TokenType.EOF):
            self.statement()

        self.emitter.emitLine(" \n  return 0;")
        self.emitter.emitLine("}")

    def statement(self):

        # "print" (expression | string)
        if self.checkToken(TokenType.PRINT):
            print("Statement-Print")
            self.nextToken()

            if self.checkToken(TokenType.STRING):
                self.emitter.emitLine(" cout << \"" + self.curToken.text + "\" << endl;")
                self.nextToken()
            else:
                self.emitter.emit(" cout << (double)(")
                self.expression()
                self.emitter.emitLine(") << endl")

        # | "IF" comparison "THEN" nl {statement} "ENDIF" nl
        elif self.checkToken(TokenType.IF):
            print("STATEMENT-IF")
            self.emitter.emit(" if(")
            self.nextToken()
            self.comparison()

            self.match(TokenType.OPENPAREN)
            self.nl()
            self.emitter.emitLine(") {")

            while not self.checkToken(TokenType.CLOSINGPAREN):
                self.statement()
            self.match(TokenType.CLOSINGPAREN)
            self.emitter.emitLine("}")

        # | "WHILE" comparison "REPEAT" {statement} "ENDWHILE"
        elif self.checkToken(TokenType.WHILE):
            print("STATEMENT-WHILE")

            self.emitter.emit(" while(")
            self.nextToken()
            self.comparison()

            self.match(TokenType.OPENPAREN)
            self.nl()
            self.emitter.emitLine(") {")

            while not self.checkToken(TokenType.CLOSINGPAREN):
                self.statement()

            self.match(TokenType.CLOSINGPAREN)
            self.emitter.emitLine("}")

        # "declare" identifier "=" expression
        elif self.checkToken(TokenType.DECLARE):
            print("declare")
            self.nextToken()
            self.emitter.emit(" double ")

            # check if it exists in the symbol table.
            if self.curToken.text not in self.symbols:
                self.symbols.add(self.curToken.text)
                self.emitter.emit(self.curToken.text + " ")

            self.match(TokenType.IDENT)
            self.match(TokenType.EQ)

            self.emitter.emit(" = ")
            self.expression()
            self.emitter.emitLine(";")

        elif self.checkToken(TokenType.IDENT):
            print("identifier")
            print("yo this is ", self.curToken.text)
            # check if it exists in the symbol table.
            if self.curToken.text not in self.symbols:
                self.abort("Error: cannot use variable " + self.curToken.text + " Without declartion")

            self.emitter.emit("    " + self.curToken.text)
            self.match(TokenType.IDENT)
            self.match(TokenType.EQ)

            self.emitter.emit(" = ")
            self.expression()
            self.emitter.emitLine(";")

        # "INPUT" identifer
        elif self.checkToken(TokenType.ENTER):
            print("STATEMENT-INPUT")
            self.nextToken()

            # if the variable does not exist, declare it
            if self.curToken.text not in self.symbols:
                self.symbols.add(self.curToken.text)

            self.match(TokenType.IDENT)

        else:
            self.abort("Invalid syntax at " + self.curToken.text + " (" + self.curToken.kind.name + ")")

        # Newline
        self.nl()

    # comparison ::= expression (("==" | "!=" | ">" | ">=" | "<" | "<=") expression)+
    def comparison(self):
        print("Comparison")

        self.expression()
        # There must be atleast one comparison operator and another expression.
        if self.isComparisonOperator():
            self.nextToken()
            self.expression()
        else:
            self.abort("Expected comparison operator at: " + self.curToken.text)

        # Can have 0 or more comparison operator and expression.
        while self.isComparisonOperator():
            self.nextToken()
            self.expression()

    # Return true if the current token is a comparison operator.
    def isComparisonOperator(self):
        return self.checkToken(TokenType.GT) or self.checkToken(TokenType.GTEQ) or self.checkToken(
            TokenType.LT) or self.checkToken(TokenType.LTEQ) or self.checkToken(TokenType.EQEQ) or self.checkToken(
            TokenType.NOTEQ)

    # expression ::= term { ( "-" | "+" ) term }
    def expression(self):
        print("EXPRESSION")

        self.term()
        while self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.nextToken()
            self.term()

    # term ::= unary { ("/" | "*" ) unary }
    def term(self):
        print("TERM")

        self.unary()
        # can have 0 or more *// and expressions.
        while self.checkToken(TokenType.ASTERISK) or self.checkToken(TokenType.SLASH):
            self.nextToken()
            self.unary()

    # unary ::= ["+" | "-"] primary
    def unary(self):
        print("UNARY")
        # Optional unary +/-
        if self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.nextToken()
        self.primary()

    # primary ::= number | indent
    def primary(self):
        print("PRIMARY (" + self.curToken.text + ")")

        if self.checkToken(TokenType.NUMBER):
            self.nextToken()
        elif self.checkToken(TokenType.IDENT):
            if self.curToken.text not in self.symbols:
                self.abort("Referencing variable before assignment: " + self.curToken.text)
            self.nextToken()
        else:
            # Error!
            self.abort("Unexpected token at " + self.curToken.text)

    # nl ::= '\n'+
    def nl(self):
        print("NEWLINE")

        self.match(TokenType.NEWLINE)
        # matching extra newlines if they exist
        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()