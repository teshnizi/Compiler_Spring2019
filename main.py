import lexer
import parser
from utils import read_rules, read_first_follow


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
    lexer = lexer.Lexer("input_code2.c")

    terminals = ['EOF', 'ID', ';', '[', 'NUM', ']', 'int', 'void', '{', '}', 'continue', 'break', 'if', 'else',
                 'while', 'return', '(', ')', 'switch', 'case', 'default', '+', '-', ',', '==', '=', '<', '>',
                 '*', ':', '']

    rules = read_rules('LL1.txt')
    first_sets, follow_sets = read_first_follow('first_sets_scratch.txt', 'follow_sets_scratch.txt')

    non_terminals = ['program', 'declaration-list', 'S1', 'declaration', 'var-declaration', 'T1', 'type-specifier',
                     'fun-declaration', 'params', 'param-list', 'S2', 'param', 'T2',  'compound-stmt',
                     'statement-list', 'S3', 'statement', 'expression-stmt', 'selection-stmt', 'iteration-stmt',
                     'return-stmt', 'T3', 'switch-stmt', 'case-stmts', 'S4', 'case-stmt', 'default-stmt', 'expression',
                     'var', 'T4', 'simple-expression', 'T5', 'relop',  'additive-expression', 'S5', 'addop',
                     'term', 'S6', 'signed-factor', 'factor', 'call', 'args', 'arg-list', 'S7']
     
    parser = parser.Parser(lexer=lexer, rules=rules, first_sets=first_sets, follow_sets=follow_sets,
                          non_terminals=non_terminals, terminals=terminals)

    print(parser.table)