
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


def read_first_follow(path_first, path_follow):
    first_sets = dict()
    with open(path_first, 'r') as f:
        for line in f:
            line = line[:-1]
            content = line.split(' ')
            non_terminal = content.pop(0)
            first_set = [x.replace(',', '') for x in content]
            first_sets[non_terminal] = first_set

    follow_sets = dict()
    with open(path_follow, 'r') as f:
        for line in f:
            line = line[:-1]
            content = line.split(' ')
            non_terminal = content.pop(0)
            follow_set = [x.replace(',', '') for x in content]
            follow_sets[non_terminal] = follow_set

    return first_sets, follow_sets


def func():
    pass
