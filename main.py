import lexer
import parser


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

    parser = parser.Parser(lexer=lexer, rules=None, first_sets=None, follow_sets=None,
                           non_terminals=None, terminals=None)
