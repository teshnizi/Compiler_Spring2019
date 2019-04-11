


class lexer:

    line_number = 1
    input = 0
    lexer_output = 0
    error_output = 0
    buffer = ""
    tokens = []

    symbols = [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '=', '<', '==']

    def go_to_next_state(self, state, ch):

        if state == "start":
            if self.type_of(ch) == "digit":
                state = "num"
                self.buffer += ch
            elif self.type_of(ch) == "letter":
                state = "id"
                self.buffer += ch
            elif ch == "/":
                state = "slash"
                self.buffer += ch
            elif ch == "\\":
                state = "bslash"
                self.buffer += ch
            elif self.type_of(ch) == "symbol":
                self.tokens.append(self.line_number, "SYMBOL", ch)

        if state == "bslash":
            if ch in ['n','f','t','r','v']:
                self.buffer = ""
                state = "start"
            elif ch in ["n", "f", "v"]:
                self.line_number += 1

        if state == "num":
            if self.type_of(ch) == "digit":
                self.buffer += ch
            else:
                self.tokens.append((self.line_number, "NUM", self.buffer))
                self.buffer = ch
                state = "start"

        if state == "ID":
            tp = self.type_of(ch)
            if tp == "digit" or tp == "letter":
                self.buffer += ch
            else:
                self.tokens.append((self.line_number, "ID", self.buffer))
                self.buffer = ch
                state = "start"

        if state == "slash":
            if ch == '*':
                state = "fcomment"
            elif ch == '/':
                state = "comment"

        if state == "fcomment":
            if ch == "*":
                state = "fcomment*"

        if state == "fcomment*":
            if ch == "/":
                state = "start"
            else:
                state = "fcomment*"

        if state == "comment":
            if ch == "\\":
                state = "comment\\"

        if state == "comment\\":
            if ch == 'n' or ch == 'r':
                state = "start"
            else:
                state = "comment"

    def type_of(self, ch):
        if '0' <= ch and ch <= '9':
            return "digit"
        if 'a' <= ch and ch <= 'z':
            return "letter"
        if 'A' <= ch and ch <= 'Z':
            return "letter"
        if ch in self.symbols:
            return "symbol"

    def get_input_buffer(self, file_name):
        with open(file_name, 'r') as fin:
            input = fin.read()

    def get_next_token(self):
        current_state = "start"
        for i in len(input):
            ch = input[i]



