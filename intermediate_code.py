class SymbolTableEntry():
    def __init__(self, lexeme, type=None, size=None, addr=None, n_params=None, PB_line=None):
        self.lexeme = lexeme
        self.addr = addr
        self.n_params = n_params
        self.size = size
        self.addr = addr
        self.type=type
        self.params_addr = None
        self.PB_line = PB_line

    def add_param(self, addr):
        if self.n_params is None:
            self.n_params = 1
            self.params_addr= []
        else:
            self.n_params += 1

        self.params_addr.append(addr)


class SemanticIntermediateCode:
    def __init__(self):
        self.SS = list()
        self.line = 0
        self.PB = dict()
        self.main_defined_flag = False
        self.temporary_SP = 500
        self.variables_SP = 1000
        self.symbol_table = list()
        self.scope_stack = list()

    def get_temp(self):
        self.temporary_SP += 4
        return self.temporary_SP - 4

    def get_symbol(self, lexeme):
        '''
        gets a lexeme as an input (function or variable name) and searches in scopes to find out if the lexeme has
        been defined previously. If not, prints out an error
        :param lexeme: str
        :return: corresponding entry of lexeme in symbol table which is an instance of SymbolTableEntry
        '''
        scope_end = len(self.symbol_table)  # last index of symbol table
        for scope_start in reversed(self.scope_stack):
            for entry in self.symbol_table[scope_start:scope_end]:
                if entry.lexeme == lexeme:
                    return entry
            scope_end = scope_start
        print('{} is not defined.'.format(lexeme))

    def start_if_scope(self):
        '''
        Makes an entry for if inside the symbol table
        pushes the index of that entry inside the scope stack.
        :return:
        '''
        self.scope_stack.append(len(self.symbol_table))
        self.symbol_table.append(['if',])

    def end_if_scope(self):
        if_scope_start = self.scope_stack.pop()
        self.symbol_table = self.symbol_table[:if_scope_start]

    def start_while_scope(self):
        self.scope_stack.append(len(self.symbol_table))
        self.symbol_table.append(['while',])

    def end_while_scope(self):
        while_scope_start = self.scope_stack.pop()
        self.symbol_table = self.symbol_table[:while_scope_start]

    def start_switch_scope(self):
        self.scope_stack.append(len(self.symbol_table))
        self.symbol_table.append(['switch',])

    def end_switch_scope(self):
        switch_scope_start = self.scope_stack.pop()
        self.symbol_table = self.symbol_table[:switch_scope_start]

    def check_break_scope(self):
        '''
        Checks out the latest scope; If it's not while or switch, prints out an error
        :return:
        '''
        entry = self.symbol_table[self.scope_stack[-1]]

        if entry[0] != 'switch' and entry[0] != 'while':
            print('No \'while\' or \'switch\' found for \'break\'.')

    def check_continue_scope(self):
        entry = self.symbol_table[self.scope_stack[-1]]
        if entry[0] != 'while':
            print('No \'while\' or \'switch\' found for \'break\'.')

    def start_func_scope(self):
        '''
        Makes an entry for the function inside symbol table
        Note that the address of paramaters will be appended to the addr_params of this entry later when the parser
        reaches parameters one by one
        :return:
        '''
        self.scope_stack.append(len(self.symbol_table))
        func_return_type, func_name = self.SS[-2], self.SS[-1]
        self.symbol_table.append(SymbolTableEntry(lexeme=func_name, type=func_return_type, PB_line=self.line))

    def pid(self, id):
        self.SS.append(id)

    def pint(self):
        '''
        push 'int' inside the SS
        '''
        self.SS.append('int')

    def pvoid(self):
        self.SS.append('void')

    def padd(self):
        self.SS.append('ADD')

    def psub(self):
        self.SS.append('SUB')

    def peq(self):
        self.SS.append('==')

    def pnum(self, num):
        '''
        push num into the SS (e.g. #2)
        :param num: string
        :return:
        '''
        self.SS.append('#' + num)

    def plt(self):
        self.SS.append('<')

    def pfunction(self):
        self.SS.append('function')

    def mult(self):
        t = self.get_temp()
        self.PB[self.line] = '(MULT,{},{},{})'.format(self.SS[-2], self.SS[-1], t)
        self.SS = self.SS[:-2]
        self.SS.append(t)
        self.line += 1

    def add(self):
        t = self.get_temp()
        self.PB[self.line] = '(ADD,{},{},{})'.format(self.SS[-2], self.SS[-1], t)
        self.SS = self.SS[:-2]
        self.SS.append(t)
        self.line += 1

    def lt(self):
        t = self.get_temp()
        self.PB[self.line] = ('<', self.SS[-2], self.SS[-1], t)
        self.SS = self.SS[:-2]
        self.SS.append(t)
        # print(self.SS)
        self.line += 1

    def assign(self):
        '''
        generates an assignment command, pops corresponding values and pushes the assigned variable to the stack
        '''
        self.PB[self.line] = '(ASSIGN,{},{},)'.format(self.SS[-1], self.SS[-2])
        self.line += 1
        # print(self.SS)
        self.SS = self.SS[:-1]

    def addop_routine(self):
        t = self.get_temp()
        operand1, addop, operand2= self.SS[-3], self.SS[-2], self.SS[-1]
        self.PB[self.line] = '({},{},{},{})'.format(addop, operand1, operand2, t)
        self.SS = self.SS[:-3]
        self.SS.append(t)
        self.line += 1

    def neg(self):
        t = self.get_temp()
        self.PB[self.line] = '(SUB,#0,{},{})'.format(self.SS[-1], t)
        self.SS.pop()
        self.SS.append(t)
        self.line += 1

    def relop_routine(self):
        # print(self.SS)
        '''
        relop is SS[-2] (either < or ==)
        fill the current line of program block with the appropriate command
        '''
        t = self.get_temp()
        self.PB[self.line] = '({},{},{},{})'.format(self.SS[-2], self.SS[-3], self.SS[-1],t)
        self.line += 1
        self.SS = self.SS[:-3]
        self.SS.append(t)

    def pop_expression(self):
        # print(self.SS)
        '''
        pops the value of expression from SS
        '''
        self.SS.pop()

    def calculate_indexed_var(self):
        '''
        pops two a variable and an index from the stack and pushes the corresponding address to the stack;
        '''
        address, size = self.get_symbol(self.SS[-2])
        index = self.SS[-1]

        t = self.get_temp()
        if index != '#0':
            self.PB[self.line] = '(MULT,{},{},{})'.format('#4', index, t)
            self.line += 1
            self.PB[self.line] = '(ADD,{},{},{})'.format(t, address, t)
            self.line += 1
            self.SS = self.SS[:-2]
            self.SS.append('@'.format(t))
        else:
            self.SS = self.SS[:-2]
            self.SS.append(address)

    def label(self):
        self.SS.append(self.line)

    def save(self):
        self.SS.append(self.line)
        # print(self.SS)
        self.line += 1

    def jpf_save(self):
        # print(self.SS)
        self.PB[self.SS[-1]] = '(JPF,{},{},)'.format(self.SS[-2], self.line + 1)
        self.SS = self.SS[:-2]
        self.SS.append(self.line)
        self.line += 1

    def jp(self):
        # print(self.SS)
        self.PB[self.SS[-1]] = '(JP,{},,)'.format(self.line)
        self.SS.pop()

    def while_routine(self):
        # print(self.SS)
        self.PB[self.SS[-1]] = '(JPF,{},{},)'.format(self.SS[-2], self.line + 1)
        self.PB[self.line] = '(JP,{},,)'.format(self.SS[-3])
        self.line += 1
        self.SS = self.SS[:-3]

    def continue_routine(self):
        pass

    def push0(self):
        self.SS.append('#0')

    def push1(self):
        self.SS.append('#1')

    def check_main(self):
        if self.SS[-1] == 'void':
            func_type, func_name = self.SS[-3], self.SS[-2]
            if func_type == 'void' and func_name == 'main':
                self.main_defined_flag = True
            self.SS = self.SS[:-3]
        else:
            self.SS = self.SS[:-2]

    def define_var(self):
        var_size, var_name, var_type = int(self.SS[-1][1:]), self.SS[-2], self.SS[-3]
        if var_type == 'void':
            print('Illegal type of void.')
        else:
            self.symbol_table.append(SymbolTableEntry(lexeme=var_name, type=var_type, addr=self.variables_SP, size=4 * var_size))
            self.variables_SP += 4 * var_size

        self.SS = self.SS[:-3]

    def define_param(self):
        param_type, param_name = self.SS[-2], self.SS[-1]
        func_scope = self.scope_stack[-1]
        func_entry = self.symbol_table[func_scope]

        # adding the parameter to symbol table
        self.symbol_table.append(SymbolTableEntry(lexeme=param_name, type=param_type, addr=self.variables_SP, size=4))
        func_entry.add_param(self.variables_SP)  # adds the address of parameter to the function entry inside symbol table
        self.variables_SP += 4
        self.SS = self.SS[:-2]

    def main_defined_routine(self):
        if not self.main_defined_flag:
            print('main function not found!')

    def call_func(self):
        func_name, n_args = int(self.SS[-2]), int(self.SS[-1][1:])
        func_entry = self.get_symbol(func_name)
        self.SS = self.SS[:-2]
        if func_entry.n_params != n_args:
            print('Mismatch in numbers of arguments of {}.'.format(func_name))
        else:
            for param_addr in func_entry.params_addr:
                self.PB[self.line] = '(ASSIGN,{},{},)'.format(self.SS[-1], param_addr)
                self.line += 1
                self.SS = self.SS[:-1]
            self.PB[self.line] = '(JP,{},,)'.format(func_entry.addr)  # jump to the beginning of function

    def add_arg(self):
        new_arg = self.SS[-1]
        n_args, func_name = int(self.SS[-2][1:]), self.SS[-3]
        self.SS = self.SS[-3]
        self.SS.append(new_arg)
        self.SS.append(func_name)
        self.SS.append('#{}'.format(n_args + 1))

    def return_routine1(self):
        return_addr = self.SS[-1]
        self.PB[self.line] = '(JP,{},,)'.format(return_addr)
        self.line += 1
        self.SS = self.SS[:-1]

    def return_routine2(self):
        expression, return_addr = self.SS[-1], self.SS[-2]
        self.PB[self.line] = '(JP,{},,)'.format(return_addr)
        self.line += 1
        self.SS = self.SS[:-2]
        self.SS.append(expression)

