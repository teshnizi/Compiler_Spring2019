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
        self.first_sets = first_sets
        self.follow_sets = follow_sets

    def make_table(self, rules, first_sets, follow_sets):
        table = dict()

        for nt in self.non_terminals:
            # print("Non terminal: ", nt)
            for t in self.terminals:
                # print("     Terminal: ", t)
                for rule in rules[nt]:
                    # print("         rule:" , rule)

                    if rule[0] == t:
                        # if (nt,t) in table:
                            # print("             !!!!!!!!!!!!!Conflict1", (nt, t), table[(nt,t)])
                        table[(nt,t)] = rule
                        # print("                 TABLE UPDATED: ", (nt, t), rule)

                    if rule[0] in self.non_terminals and t in first_sets[rule[0]]:
                        # if (nt,t) in table:
                        #     print("             !!!!!!!!!!!!!Conflict2", (nt, t), table[(nt,t)])
                        table[(nt, t)] = rule
                        # print("                 TABLE UPDATED: ", (nt, t), rule)

                    if rule[0] in self.non_terminals and t in follow_sets[rule[0]] and 'ε' in first_sets[rule[0]]:
                        # if (nt,t) in table:
                        #     print("             !!!!!!!!!!!!!Conflict3", (nt, t), table[(nt,t)])
                        table[(nt,t)] = rule
                        # print("                 TABLE UPDATED: ", (nt, t), rule)

                    if rule[0] == 'ε' and t in follow_sets[nt]:
                        table[(nt,t)] = rule
                        # print("                 TABLE UPDATED: ", (nt, t), rule)

        return table
        # if (nt,t) in table:
        #     print("Conflict", table[(nt,t)])

    def get_and_split_token(self):
        self.input = self.lexer.get_next_token()
        if self.input[0] == False:
            self.input = "EOF"
            return

        self.line_number = self.input[1][0]

        if self.input[1][1] == "ID" or self.input[1][1] == "NUM":
            self.input = self.input[1][1]
        else:
            self.input = self.input[1][2]

    def parse(self, nt, depth):
        if nt == 'ε':
            return

        self.tree_file.write(' |    ' * depth + nt + '\n')

        print(nt, "   " , self.input)
        if self.input is None:
            self.get_and_split_token()

        if self.input is "EOF":
            if 'ε' in self.first_sets[nt]:
                return
            else:
                print("SOME ERROR SHOULD BE GENERATED HERE!") #TODO geenrate corresponding error

        while self.input not in self.follow_sets[nt] + self.first_sets[nt]:
            print(self.line_number, "Syntax Error! Unexpected ", self.input)
            self.get_and_split_token()

        if (self.input in self.first_sets[nt]) or \
                ('ε' in self.first_sets[nt] and self.input in self.follow_sets[nt]):
            for next_state in self.table[(nt, self.input)]:
                if next_state in self.terminals:
                    if next_state == self.input:
                        self.get_and_split_token()
                    else:
                        print(self.line_number, "Syntax Error! Missing ", next_state)
                else:
                    self.parse(next_state, depth+1)
        else:
            print(self.line_number, "Syntax Error! Missing", "")  # TODO: change the empty msg with appropriate value
