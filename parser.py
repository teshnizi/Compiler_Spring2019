


class Parser:

    def __init__(self, lexer, first_sets, follow_sets):
        self.lexer = lexer
        self.table = self.make_table(first_sets, follow_sets)


    def make_table(self, rules, first_sets, follow_sets):
        table = dict()

        non_terminals = list(first_sets.keys())

        for nt in non_terminals:
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
        #
        # for iterator in range(len(non_terminals) * 2):
        #     for nt in non_terminals:
        #         for rule in rules[nt]:
        #             for key, goal in table.items():
        #                 if key[0] ==



