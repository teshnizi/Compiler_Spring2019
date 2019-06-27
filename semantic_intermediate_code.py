import os


class SemanticIntermediateCode:
    def __init__(self):
        self.SS = list()

    def analyze(self, nt, rule, next_state, input_token):
        if nt == 'expression' and next_state == 'ID':
            self.SS.append(self.find_addr(input_token))
            print('Inside semantic nt: {}  stack: {} input token: {}'.format(nt, self.SS, input_token))

        if nt == 'type-specifier':
            self.SS.append(next_state)

    def generate(self):
        pass


    def find_addr(self, input):
        pass  # TODO: find the adrress of ID in memory