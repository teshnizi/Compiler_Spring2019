import lexer


lexer = lexer.Lexer("input_code.c")


while (True):
    tp = lexer.get_next_token()
    print(tp[1])
    if tp[0] == False:
        break