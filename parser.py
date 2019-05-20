import os
from lexer import Lexer


class Parser:
    def __init__(self, lexer, rules, first_sets, follow_sets, non_terminals, terminals):
        self.lexer = lexer
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.table = self.make_table(rules, first_sets, follow_sets)
        self.input = None
        self.tree_file = open("tree.txt", "w")
        self.line_number = None

    def make_table(self, rules, first_sets, follow_sets):
        table = dict()

        for nt in self.non_terminals:
            follow_set = follow_sets[nt]
            first_set = first_sets[nt]

            for t in first_set:
                for rule in rules[nt]:
                    if rule[0] == t:
                        table[(nt,t)] = rule

            for t in follow_set:
                for rule in rules[nt]:
                    if rule[0] == 'ε':
                        table[(nt,t)] = rule
        return table

    def get_and_split_token(self):
        self.input = self.lexer.get_next_token()
        if self.input[0] == False:
            self.input = None
            return

        self.line_number = self.input[1][0]

        if self.input[1][1] == "ID" or self.input[1][1] == "NUM":
            self.input = self.input[1][1]
        else:
            self.input = self.input[1][2]

    def parse(self, NT, depth):
        self.tree_file.write(['|'] * depth, NT)

        if self.input == None:
            self.get_and_split_token()

        next_state = self.table[NT]
        for element in next_state:
            if element in self.terminals:
                if element == self.input:
                    self.get_and_split_token()
                else:
                    print(self.line_number, "Syntax Error! Missing", self.input)
            else:
                self.parse(element, depth+1)
