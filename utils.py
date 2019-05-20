
def read_rules(path):
    path = 'LL1.txt'
    with open(path, 'r') as f:
        last_nt = None
        rules = dict()
        for line in f:
            new_nt, rule = line.split('->')
            if new_nt != last_nt:
                last_nt = new_nt
                rules[new_nt] = [rule.split()]
            else:
                rules[last_nt].append(rule.split())

    return rules

