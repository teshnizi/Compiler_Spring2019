import lexer
import parser
from utils import read_rules, read_first_follow, get_non_terminals


def func_phase1(lexer):
    with open('scanner.txt', 'w') as fout, open('errors_lexical.txt', 'w') as ferr:
        last_line_out = 0
        last_line_err = 0
        while True:
            tp = lexer.get_next_token()
            print(tp[1])
            new_line = tp[1][0]

            if tp[1][2] != 'invalid input':
                if new_line > last_line_out:
                    if last_line_out > 0:
                        fout.write('\n')
                    fout.write(str(new_line) + '. ')
                    last_line_out = new_line
                fout.write('(' + tp[1][1] + ', ' + tp[1][2] + ')' + ' ')
            else:
                if new_line > last_line_err:
                    if last_line_err > 0:
                        ferr.write('\n')
                    ferr.write(str(new_line) + '. ')
                    last_line_err = new_line
                ferr.write('(' + tp[1][1] + ', ' + tp[1][2] + ')' + ' ')

            if not tp[0]:
                break


if __name__ == '__main__':

    lexer = lexer.Lexer("All Tests/Parser/Test Error - Parser.txt")

    # func_phase1(lexer)

    terminals = ['EOF', 'ID', ';', '[', 'NUM', ']', 'int', 'void', '{', '}', 'continue', 'break', 'if', 'else',
                 'while', 'return', '(', ')', 'switch', 'case', 'default', '+', '-', ',', '==', '=', '<', '>',
                 '*', ':', '']

    rules = read_rules('LL1.txt')
    first_sets, follow_sets = read_first_follow('first_sets_scratch.txt', 'follow_sets_scratch.txt')
    non_terminals = get_non_terminals('LL1.txt')

    with open("tree.txt", "w") as tree_file, open("syntax_errors.txt", "w") as syntax_errors_file:
        parser = parser.Parser(lexer=lexer, rules=rules, first_sets=first_sets, follow_sets=follow_sets,
                        non_terminals=non_terminals, terminals=terminals, tree_file=tree_file, syntax_errors_file=syntax_errors_file)

        parser.parse('program', 0)

    # print(parser.table)