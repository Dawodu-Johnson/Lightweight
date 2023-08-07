from lex import *
from parser import *
from emitter import *
import sys


def main():
    if len(sys.argv) != 2:
        sys.exit("Error: compiler needs source file as argument.")
    with open(sys.argv[1], 'r') as inputFile:
        print('''
                     -------------------Light weight compiler-------------------
        ''')

        source = inputFile.read()
        lexer = Lexer(source)
        emitter = Emitter("output.cpp")

        parser = Parser(lexer, emitter)
        parser.program()  # start
        emitter.writeFile()  # write the output to the file

        print("Parsing completed.")


main()
