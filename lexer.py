


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
            if self.type_of(ch) == "letter":
                state = "id"
                self.buffer += ch
            if ch == "/":
                state = "slash"
                self.buffer += ch
            if ch == "\\":
                state = "bslash"
                self.buffer += ch
        if state == "bslash":
            if ch in ['n','f','t','r','v']:
                self.buffer = ""
                state = "start"
            if ch in ["n", "f", "v"]:
                self.line_number += 1
        
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



