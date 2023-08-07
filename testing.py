from lex import *


def testing_lexer():
    # testing characters

    source_code = "LET foobar = 123"
    lexer = Lexer(source_code)

    while lexer.peek() != '\0':
        print(lexer.currentChar)
        lexer.next_char()

    # testing operators

    source_code = "+- \"This is a string\" # This is a comment!\n   */ +-1239.8654*/"
    lexer = Lexer(source_code)
    token = lexer.get_token()

    while token.kind != TokenType.EOF:
        print(token.kind)
        token = lexer.get_token()


testing_lexer()
