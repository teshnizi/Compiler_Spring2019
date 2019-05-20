
class Lexer:

    line_number = 1
    input_string = 0
    output = 0
    error_output = 0
    buffer = ""
    iterator = 0
    state = "start"
    keywords = ['if', 'else', 'void', 'int', 'while', 'break', 'continue', 'switch', 'default', 'case', 'return']
    symbols = [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '=', '<', '==']

    def __init__(self, input_name):
        self.iterator = 0
        with open(input_name, 'r') as fin:
            self.input_string = fin.read()
            # print(len(self.input_string))

    def is_in_alphabet(self, ch):
        if self.type_of(ch) != ch or ch in ['\n','\f','\t','\r','\v',' ','/']:
            return True
        return False

    def go_to_next_state(self):

        if self.iterator >= len(self.input_string):
            # ch = "EOF"
            return (False, (self.line_number, "EOF", "EOF"))
        else:
            ch = self.input_string[self.iterator]

        token = (0, 0, 0)
        self.iterator += 1
        # print("State: " + self.state + "  character: " + ch)

        if self.state == "start":
            if self.type_of(ch) == "digit":
                self.state = "num"
                self.buffer += ch
            elif self.type_of(ch) == "letter":
                self.state = "ID"
                self.buffer += ch
            elif ch == "/":
                self.state = "slash"
                self.buffer += ch
            elif ch in ['\n', '\f', '\t', '\r', '\v', ' ']:
                self.buffer = ""
                self.state = "start"
                if ch in ["\n", "\f", "\v"]:
                    self.line_number += 1
            elif self.type_of(ch) == "symbol":
                token = (self.line_number, "SYMBOL", ch)
                if ch == '=' and len(self.input_string) > self.iterator and self.input_string[self.iterator] == '=':
                    self.iterator += 1
                    token = (self.line_number, "SYMBOL", "==")
            else:
                self.buffer = ch
                self.state = "error"
                self.iterator -= 1
            return not (len(self.input_string) == self.iterator), token

        if self.state == "num":
            if self.type_of(ch) == "digit":
                self.buffer += ch
            else:
                if self.is_in_alphabet(ch):
                    token = (self.line_number, "NUM", self.buffer)
                    self.iterator -= 1
                else:
                    token = (self.line_number, self.buffer + ch, "Invalid Input")
                self.buffer = ""
                self.state = "start"

            return not (len(self.input_string) == self.iterator), token

        if self.state == "ID":
            tp = self.type_of(ch)
            if tp == "digit" or tp == "letter":
                self.buffer += ch
            else:
                if self.is_in_alphabet(ch):
                    if self.buffer in self.keywords:
                        token = (self.line_number, "KEYWORD", self.buffer)
                        self.iterator -= 1
                    else:
                        token = (self.line_number, "ID", self.buffer)
                        self.iterator -= 1
                else:
                    token = (self.line_number, self.buffer + ch, "invalid input")
                self.buffer = ""
                self.state = "start"

            return not (len(self.input_string) == self.iterator), token

        if self.state == "slash":
            if ch == '*':
                self.state = "fcomment"
            elif ch == '/':
                self.state = "comment"
            else:
                self.buffer = ch
                self.state = "error"
            return not (len(self.input_string) == self.iterator), token

        if self.state == "fcomment":
            if ch == "*":
                self.state = "fcomment*"
            return not (len(self.input_string) == self.iterator), token

        if self.state == "fcomment*":
            if ch == "/":
                self.state = "start"
            else:
                self.state = "fcomment*"
            return not (len(self.input_string) == self.iterator), token

        if self.state == "comment":
            if ch in ["\n", "\f", "\v"]:
                self.state = "start"
                self.line_number += 1
            return not (len(self.input_string) == self.iterator), token

        if self.state == "error":
            token = (self.line_number, self.buffer, "invalid input")
            self.buffer = ""
            self.state = "start"
            return not (len(self.input_string) == self.iterator), token

        print("INVALID STATE DETECTED:" + self.state)
        return not (len(self.input_string) == self.iterator), token

    def type_of(self, ch):
        if '0' <= ch <= '9':
            return "digit"
        if 'a' <= ch <= 'z':
            return "letter"
        if 'A' <= ch <= 'Z':
            return "letter"
        if ch in self.symbols:
            return "symbol"
        return ch

    def set_input_buffer(self, file_name):
        with open(file_name, 'r') as fin:
            input = fin.read()

    def get_next_token(self):
        while True:
            tp = self.go_to_next_state()
            if tp[1] != (0, 0, 0):
                break
        return tp