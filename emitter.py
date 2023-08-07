class Emitter:
    def __init__(self, file):
        self.file = file
        self.header = ""
        self.code = "\n"

    def emit(self, code):
        self.code += code

    def emitLine(self, code):
        self.code += code + '\n'

    def headerLine(self, header):
        self.header += header + '\n'

    def writeFile(self):
        with open(self.file, 'w') as outputFile:
            outputFile.write(self.header + self.code)