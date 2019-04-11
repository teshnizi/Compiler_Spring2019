


class Lexer:

    line_number = 1
    input_string = 0
    output = 0
    error_output = 0
    buffer = ""
    tokens = []
    iterator = 0
    state = "start"
    symbols = [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '=', '<', '==']

    def __init__(self, input_name, output_name, errorfile_name):
        self.iterator = 0
        with open(input_name, 'r') as fin:
            self.input_string = fin.read()
            print(len(self.input_string))
        # with open(output_name, 'w') as fout:
        #     self.output = fout.read()
        # with open(errorfile_name, 'w') as fout:
        #     self.input_string = fout.read()

    def go_to_next_state(self):

        ch = self.input_string[self.iterator]
        self.iterator += 1
        print("State: " + self.state + "  character: " + ch)

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
            elif ch in ['\n','\f','\t','\r','\v',' ']:
                self.buffer = ""
                self.state = "start"
                if ch in ["\n", "\f", "\v"]:
                    self.line_number += 1
            elif self.type_of(ch) == "symbol":
                self.tokens.append((self.line_number, "SYMBOL", ch))
            else:
                self.buffer = ch
                self.state = "error"
            return not (len(self.input_string) == self.iterator)

        # if self.state == "bslash":
        #     if ch in ['n','f','t','r','v']:
        #         self.buffer = ""
        #         self.state = "start"
        #         if ch in ["n", "f", "v"]:
        #             self.line_number += 1
        #     else:
        #         self.buffer = ch
        #         self.state = "error"
        #     return not (len(self.input_string) == self.iterator)

        if self.state == "num":
            if self.type_of(ch) == "digit":
                self.buffer += ch
            else:
                self.tokens.append((self.line_number, "NUM", self.buffer))
                self.buffer = ""
                self.state = "start"
                self.iterator -= 1
            return not (len(self.input_string) == self.iterator)

        if self.state == "ID":
            tp = self.type_of(ch)
            if tp == "digit" or tp == "letter":
                self.buffer += ch
            else:
                self.tokens.append((self.line_number, "ID", self.buffer))
                self.buffer = ""
                self.iterator -= 1
                self.state = "start"
            return not (len(self.input_string) == self.iterator)

        if self.state == "slash":
            if ch == '*':
                self.state = "fcomment"
            elif ch == '/':
                self.state = "comment"
            else:
                self.buffer = ch
                self.state = "error"
            return not (len(self.input_string) == self.iterator)

        if self.state == "fcomment":
            if ch == "*":
                self.state = "fcomment*"
            return not (len(self.input_string) == self.iterator)


        if self.state == "fcomment*":
            if ch == "/":
                self.state = "start"
            else:
                self.state = "fcomment*"
            return not (len(self.input_string) == self.iterator)


        if self.state == "comment":
            if ch == "\\":
                self.state = "comment\\"
            return not (len(self.input_string) == self.iterator)

        if self.state == "comment\\":
            if ch == 'n' or ch == 'r':
                self.state = "start"
            else:
                self.state = "comment"
            return not (len(self.input_string) == self.iterator)


        print("INVALID STATE DETECTED:" + self.state)
        return not (len(self.input_string) == self.iterator)


    def type_of(self, ch):
        if '0' <= ch and ch <= '9':
            return "digit"
        if 'a' <= ch and ch <= 'z':
            return "letter"
        if 'A' <= ch and ch <= 'Z':
            return "letter"
        if ch in self.symbols:
            return "symbol"
        return ch

    def set_input_buffer(self, file_name):
        with open(file_name, 'r') as fin:
            input = fin.read()

    def get_next_token(self):
        k = len(self.tokens)
        while len(self.tokens) == k:
            self.go_to_next_state()
        print(self.tokens)




