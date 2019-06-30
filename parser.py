import os
from lexer import Lexer
from intermediate_code import SemanticIntermediateCode

class Parser:
    def __init__(self, lexer, rules, first_sets, follow_sets, non_terminals, terminals, tree_file, syntax_errors_file):
        self.semantic_intermediate_code = SemanticIntermediateCode()
        self.lexer = lexer
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.table = self.make_table(rules, first_sets, follow_sets)
        self.input = None
        self.tree_file = tree_file
        self.error_file = syntax_errors_file
        self.line_number = None
        self.first_sets = first_sets
        self.follow_sets = follow_sets
        self.rules = rules
        self.input_buffer_stack = []
        self.semantic_input = 0
        self.waiting_for_id = False
        self.waiting_for_num = False

    def make_table(self, rules, first_sets, follow_sets):
        table = dict()

        for nt in self.non_terminals:
            for t in self.terminals:

                for rule in rules[nt]:

                    i = 0;
                    while rule[i][0] == '#':
                        i += 1

                    first_terminal  = rule[i]

                    if first_terminal == t:
                        table[(nt,t)] = rule

                    if first_terminal in self.non_terminals and t in first_sets[first_terminal]:
                        table[(nt, t)] = rule

                    if first_terminal in self.non_terminals and t in follow_sets[first_terminal] and 'ε' in first_sets[first_terminal]:
                        table[(nt,t)] = rule

                    if first_terminal == 'ε' and t in follow_sets[nt]:
                        table[(nt,t)] = rule

        return table

    def get_and_split_token(self):

        self.input = self.lexer.get_next_token()

        if self.input[0] == False:
            self.input = "EOF"
            return
        if self.input[1][2] == 'invalid input':
            self.get_and_split_token()
            return

        self.line_number = self.input[1][0]
        self.semantic_input = self.input[1][2]

        if self.input[1][1] == "ID" or self.input[1][1] == "NUM":
            self.input = self.input[1][1]
        else:
            self.input = self.input[1][2]

    def parse(self, nt, depth):
        if nt == 'ε':
            return


        self.tree_file.write(' | ' * depth + nt + '\n')

        if self.input is None:
            self.get_and_split_token()

        if self.input is "EOF":
            if 'ε' in self.first_sets[nt]:
                return
            else:
                self.error_file.write(str(self.line_number) + " Syntax Error! Unexpected EndOfFile\n")

        while self.input not in self.follow_sets[nt] + self.first_sets[nt]:
            self.get_and_split_token()
            if self.input == 'EOF':
                return

        if (self.input in self.first_sets[nt]) or \
                ('ε' in self.first_sets[nt] and self.input in self.follow_sets[nt]):
            backup = self.input

            for index in range(len(self.table[(nt, backup)])):
                table = self.table[(nt, backup)]
                next_state = table[index]

                if next_state[0] == '#':
                    '''
                    Certain functions (like functions with non-void arguments)
                    should be called individually, for others use getattr.
                    '''
                    # print(self.semantic_intermediate_code.SS)
                    # print(next_state)
                    if next_state == "#pid":
                        self.waiting_for_id = True # pid routine will be executed after reading variable name
                    elif next_state == "#pnum":
                        self.waiting_for_num = True # pnum routine will be executed after reading the number
                    else:
                        func = getattr(self.semantic_intermediate_code, next_state[1:])
                        func()

                elif next_state in self.terminals:
                    if nt == 'program':
                        if next_state != 'EOF':
                            self.error_file.write(str(self.line_number) + " Syntax Error! Malformed Input\n")
                    if self.input is None:
                       self.get_and_split_token()
                    if next_state == self.input:
                        if self.waiting_for_id:
                            self.waiting_for_id = False
                            self.semantic_intermediate_code.pid(self.semantic_input)
                        elif self.waiting_for_num:
                            self.waiting_for_num = False
                            self.semantic_intermediate_code.pnum(self.semantic_input)

                        self.input = None
                    else:
                        self.error_file.write(str(self.line_number) + " Syntax Error! Missing " + next_state + " \n")

                else:
                    self.parse(next_state, depth+1)

        else:
            self.error_file.write(str(self.line_number) + " Syntax Error! Missing " + nt + " couldn't find the appropriate rule: " + str(self.rules[nt]) + "\n")
