import sys
from enum import Enum


class Lexer:
    def __init__(self, source):
        self.source = source + '\n'  # adding end of line to the source code for simplification
        self.currentChar = ''  # current character in the string
        self.currentPosition = -1  # current position in the string
        self.next_char()

    def peek(self):
        next_index = self.currentPosition + 1
        if next_index >= len(self.source):
            return '\0'
        return self.source[next_index]

    def next_char(self):
        self.currentPosition += 1
        if self.currentPosition >= len(self.source):
            self.currentChar = '\0'  # end of line
        else:
            self.currentChar = self.source[self.currentPosition]

    def abort(self, message):
        sys.exit("Lexing error: " + message)

    def skip_white_space(self):
        while self.currentChar == ' ' or self.currentChar == '\t' or self.currentChar == '\r':
            self.next_char()

    def skip_comment(self):
        if self.currentChar == '#':
            while self.currentChar != '\n':
                self.next_char()

    def get_token(self):

        self.skip_white_space()
        self.skip_comment()
        token = None

        if self.currentChar == '+':
            token = Token(self.currentChar, TokenType.PLUS)

        elif self.currentChar == '-':
            token = Token(self.currentChar, TokenType.MINUS)

        elif self.currentChar == '*':
            token = Token(self.currentChar, TokenType.ASTERISK)

        elif self.currentChar == '{':
            token = Token(self.currentChar, TokenType.OPENPAREN)

        elif self.currentChar == '}':
            token = Token(self.currentChar, TokenType.CLOSINGPAREN)

        elif self.currentChar == '/':
            token = Token(self.currentChar, TokenType.SLASH)

        elif self.currentChar == '=':
            if self.peek() == '=':
                second_char = self.peek()
                token = Token(self.currentChar + second_char, TokenType.EQEQ)
                self.next_char()
            else:
                token = Token(self.currentChar, TokenType.EQ)

        elif self.currentChar == '>':
            if self.peek() == '=':
                second_char = self.peek()
                token = Token(self.currentChar + second_char, TokenType.GTEQ)
                self.next_char()
            else:
                token = Token(self.currentChar, TokenType.GT)

        elif self.currentChar == '<':
            if self.peek() == '=':
                second_char = self.peek()
                token = Token(self.currentChar + second_char, TokenType.LTEQ)
                self.next_char()
            else:
                token = Token(self.currentChar, TokenType.LT)

        elif self.currentChar == '!':
            if self.peek() == '=':
                second_char = self.peek()
                token = Token(self.currentChar + second_char, TokenType.NOTEQ)
            else:
                self.abort("Expected !=, got !" + self.peek())

        elif self.currentChar == "\"":  # string
            self.next_char()
            start_pos = self.currentPosition

            while self.currentChar != "\"":
                if self.currentChar == '\n' or self.currentChar == '\r' or \
                        self.currentChar == '\t' or self.currentChar == '\\' or self.currentChar == '%':
                    self.abort("unwanted character in string")
                self.next_char()
            token_text = self.source[start_pos: self.currentPosition]
            token = Token(token_text, TokenType.STRING)

        elif self.currentChar.isdigit():
            start_pos = self.currentPosition

            while self.peek().isdigit():
                self.next_char()

            if self.peek() == '.':  # Decimal
                self.next_char()

                # there must be atleast a number after the decimal
                if not self.peek().isdigit():
                    self.abort("Invalid number")

                while self.peek().isdigit():
                    self.next_char()
            token_text = self.source[start_pos: self.currentPosition + 1]
            token = Token(token_text, TokenType.NUMBER)

        elif self.currentChar.isalpha():
            start_pos = self.currentPosition
            while self.peek().isalnum():
                self.next_char()
            token_text = self.source[start_pos: self.currentPosition + 1]  # can either be a token or an identifier
            keyword = Token.check_if_keyword(token_text)
            if keyword is None:
                token = Token(token_text, TokenType.IDENT)
            else:
                token = Token(token_text, keyword)
        elif self.currentChar == '\n':
            token = Token(self.currentChar, TokenType.NEWLINE)

        elif self.currentChar == '\0':
            token = Token('', TokenType.EOF)

        else:
            self.abort("Unknown token: " + self.currentChar)

        self.next_char()
        return token


class Token:
    def __init__(self, token_text, token_type):
        self.text = token_text  # the token's text
        self.kind = token_type

    @staticmethod
    def check_if_keyword(token_text):
        for kind in TokenType:
            if kind.name.lower() == token_text and 100 < kind.value < 200:
                return kind

        return None


class TokenType(Enum):
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2
    STRING = 3

    # Keywords.
    PRINT = 103
    ENTER = 104
    DECLARE = 105
    IF = 106
    THEN = 107
    ENDIF = 108
    WHILE = 109
    REPEAT = 110
    ENDWHILE = 111

    # Operators.
    EQ = 201
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    EQEQ = 206
    NOTEQ = 207
    LT = 208
    LTEQ = 209
    GT = 210
    GTEQ = 211
    OPENPAREN = 220
    CLOSINGPAREN = 222
