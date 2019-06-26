import os
from lexer import Lexer

class Parser:

    def __init__(self, lexer, rules, first_sets, follow_sets, non_terminals, terminals, tree_file, syntax_errors_file):
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

    def make_table(self, rules, first_sets, follow_sets):
        table = dict()

        for nt in self.non_terminals:
            for t in self.terminals:

                for rule in rules[nt]:

                    if rule[0] == t:
                        table[(nt,t)] = rule

                    if rule[0] in self.non_terminals and t in first_sets[rule[0]]:
                        table[(nt, t)] = rule

                    if rule[0] in self.non_terminals and t in follow_sets[rule[0]] and 'ε' in first_sets[rule[0]]:
                        table[(nt,t)] = rule

                    if rule[0] == 'ε' and t in follow_sets[nt]:
                        table[(nt,t)] = rule


        return table


    def get_and_split_token(self):

        # if len(self.input_buffer_stack) > 0:
            # self.input = self.input_buffer_stack[0]
            # if len(self.input_buffer_stack)
            # self.input_buffer_stack = self.input_buffer_stack[1:-1]

        self.input = self.lexer.get_next_token()
        # self.tree_file.write("--------------------" + str(self.input) + "  inp\n")

        if self.input[0] == False:
            self.input = "EOF"
            return
        if self.input[1][2] == 'invalid input':
            self.get_and_split_token()
            return

        self.line_number = self.input[1][0]

        if self.input[1][1] == "ID" or self.input[1][1] == "NUM":
            self.input = self.input[1][1]
        else:
            self.input = self.input[1][2]

    def parse(self, nt, depth):

        # print("ppp " + nt , depth)

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
            # self.error_file.write(str(self.line_number) + " Syntax Error! Unexpected " + str(self.input) + "\n")
            # self.tree_file.write(self.input + "\tERROR: " + nt + " :: \n" + str(self.follow_sets[nt]) + " \n" + str(self.first_sets[nt]) + "\n")
            # self.tree_file.write("OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO\n")
            self.get_and_split_token()
            if self.input == 'EOF':
                return

        # flag = False
        # while flag == False:
        flag = False
        if (self.input in self.first_sets[nt]) or \
                ('ε' in self.first_sets[nt] and self.input in self.follow_sets[nt]):
            for next_state in self.table[(nt, self.input)]:

                if next_state in self.terminals:
                    if nt == 'program':
                        if next_state != 'EOF':
                            self.error_file.write(str(self.line_number) + " Syntax Error! Malformed Input\n")
                    if self.input is None:
                       self.get_and_split_token()
                    #
                    # self.tree_file.write("\tMESSAGE: " + nt + " " + str(self.input) + " " + next_state + "\n")

                    if next_state == self.input:
                        self.input = None
                    else:
                        self.error_file.write(str(self.line_number) + " Syntax Error! Missing " + next_state + " \n")
                    # self.tree_file.write("\tMESSAGE: " + nt + " " + str(self.input) + " " + next_state + "\n")
                        # return
                else:
                    self.parse(next_state, depth+1)
        else:
            self.error_file.write(str(self.line_number) + " Syntax Error! Missing " + nt + " couldn't find the appropriate rule: " + str(self.rules[nt]) + "\n")