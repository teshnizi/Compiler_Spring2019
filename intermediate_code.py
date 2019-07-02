class SymbolTableEntry():
    def __init__(self, lexeme, type=None, size=None, addr=None, n_params=0, PB_line=None, return_value=None):
        '''
        :param lexeme: name of variable or function
        :param type: type of variable or function return value
        :param size: size of variable, None for function
        :param addr: address of variable or return address of function
        :param n_params: parameters of function, None for variable
        :param PB_line: starting point of function
        :param return_value: return value of function, None for variable
        '''
        self.lexeme = lexeme
        self.n_params = n_params
        self.size = size
        self.addr = addr
        self.type = type
        self.params_addr = []
        self.PB_line = PB_line
        self.return_value = return_value

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
        self.line = 1
        self.PB = dict()
        self.main_defined_flag = False
        self.temporary_SP = 500
        self.variables_SP = 1000
        self.values_SP = 1400
        self.symbol_table = list()
        self.scope_stack = [0]

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
        # print(lexeme)
        # print("----")
        # self.print_symbol_table()
        scope_end = len(self.symbol_table)  # last index of symbol table
        for scope_start in reversed(self.scope_stack):
            for entry in self.symbol_table[scope_start:scope_end]:
                if entry.lexeme == lexeme:
                    return entry
            scope_end = scope_start
        return None

    def start_if_scope(self):
        '''
        Makes an entry for if inside the symbol table
        pushes the index of that entry inside the scope stack.
        :return:
        '''
        self.scope_stack.append(len(self.symbol_table))
        self.symbol_table.append(SymbolTableEntry(lexeme='if'))

    def end_if_scope(self):
        if_scope_start = self.scope_stack.pop()
        self.symbol_table = self.symbol_table[:if_scope_start]

    def start_else_scope(self):
        self.scope_stack.append(len(self.symbol_table))
        self.symbol_table.append(SymbolTableEntry(lexeme='else'))

    def end_else_scope(self):
        else_scope_start = self.scope_stack.pop()
        self.symbol_table = self.symbol_table[:else_scope_start]

    def start_while_scope(self):
        self.scope_stack.append(len(self.symbol_table))
        self.symbol_table.append(SymbolTableEntry(lexeme='while', PB_line=self.SS[-3] + 1))

    def jp_while(self):
        self.PB[self.line] = '(JP,{},,)'.format(self.line + 2)
        self.SS.append(self.line + 1)
        self.line += 2

    def end_while_scope(self):
        while_scope_start = self.scope_stack.pop()
        self.symbol_table = self.symbol_table[:while_scope_start]

    def jp_switch(self):
        self.PB[self.line] = '(JP,{},,)'.format(self.line + 2)
        self.SS.append(self.line + 1)
        self.line += 2

    def start_switch_scope(self):
        self.scope_stack.append(len(self.symbol_table))
        self.symbol_table.append(SymbolTableEntry(lexeme='switch', PB_line=self.SS[-2] + 1))

    def cmp_save(self):
        operand1, operand2 = self.SS[-1], self.SS[-2]
        t = self.get_temp()
        self.PB[self.line] = '(EQ,{},{},{})'.format(operand1, operand2, t)
        self.line += 1
        self.SS = self.SS[:-1]
        self.SS.append(t)
        self.SS.append(self.line)
        self.line += 1

    def jpf_switch(self):
        self.PB[self.SS[-1]] = '(JPF,{},{},)'.format(self.SS[-2], self.line)
        self.SS = self.SS[:-2]

    def end_switch_scope(self):
        self.PB[self.SS[-2]] = '(JP,{},,)'.format(self.line)
        switch_scope_start = self.scope_stack.pop()
        self.symbol_table = self.symbol_table[:switch_scope_start]
        self.SS = self.SS[:-2]

    def break_routine(self):
        # print(self.SS)
        entry = None
        flag = False
        scope_end = len(self.symbol_table)  # last index of symbol table
        for scope_start in reversed(self.scope_stack):
            for element in self.symbol_table[scope_start:scope_end]:
                if element.lexeme == 'while' or element.lexeme == 'switch' and not flag:
                    entry = element
                    flag = True
            scope_end = scope_start

        if entry is not None:
            self.PB[self.line] = '(JP,{},,)'.format(entry.PB_line - 1)
            self.line += 1
        else:
            print('No \'while\' or \'switch\' found for \'break\'.')

    def print_symbol_table(self):
        print("Symbol table:")
        for entry in self.symbol_table:
            print(entry.lexeme)
        print("=============")

    # def check_break_scope(self):
    #     '''
    #     Checks out the latest scope; If it's not while or switch, prints out an error
    #     :return:
    #     '''
    #     entry = self.get_symbol[self.scope_stack[-1]]
    #
    #     if entry.lexeme != 'switch' and entry.lexeme != 'while':
    #         print('No \'while\' or \'switch\' found for \'break\'.')

    def check_continue_scope(self):
        entry = self.get_symbol('while')
        if entry is None:
            print('No \'while\' found for \'continue\'.')

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

    def end_func_scope(self):
        # func = self.get_symbol(self.SS[-1])
        scope_start = self.scope_stack.pop()
        self.symbol_table = self.symbol_table[:scope_start + 1]
        self.SS.pop()
        # print(self.SS)

    def push_break_symbol(self):
        self.symbol_table.append(SymbolTableEntry(lexeme='break', PB_line=self.line))
        self.line += 1

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
        # print(self.SS)

    def plt(self):
        self.SS.append('LT')

    def pfunction(self):
        self.SS.append('function')

    def mult(self):
        t = self.get_temp()
        operand1, operand2 = self.SS[-2], self.SS[-1]
        if operand1 is None or operand2 is None:
            print("Type mismatch in operands.")
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
        self.PB[self.line] = '(LT,{},{},{})'.format(self.SS[-2], self.SS[-1], t)
        self.SS = self.SS[:-2]
        self.SS.append(t)
        # print(self.SS)
        self.line += 1

    def assign(self):
        '''
        generates an assignment command, pops corresponding values and pushes the assigned variable to the stack
        '''
        if self.SS[-1] == None or self.SS[-2] == None:
            print("Type mismatch in operands.")
        self.PB[self.line] = '(ASSIGN,{},@{},)'.format(self.SS[-1], self.SS[-2])
        self.line += 1
        # print(self.SS)
        self.SS = self.SS[:-1]

    def addop_routine(self):
        t = self.get_temp()
        operand1, addop, operand2= self.SS[-3], self.SS[-2], self.SS[-1]
        if operand1 == None or operand2 == None:
            print("Type mismatch in operands.")
        self.PB[self.line] = '({},{},{},{})'.format(addop, operand1, operand2, t)
        self.SS = self.SS[:-3]
        self.SS.append(t)
        self.line += 1

    def neg(self):
        t = self.get_temp()
        if self.SS[-1] == None:
            print("Type mismatch in operands.")
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
        pops a variable and an index from the stack and pushes the corresponding address to the stack;
        '''
        # print(self.SS)

        var = self.get_symbol(self.SS[-2])
        if var is None:
            print('{} is not defined.'.format(self.SS[-2]))
            self.SS = self.SS[:-2]
            self.SS.append("NONE")
            return
        address = var.addr
        size = var.size
        index = self.SS[-1]
        # print(address, size, index)
        t = self.get_temp()
        # if index != '#0':
        self.PB[self.line] = '(MULT,{},{},{})'.format('#4', index, t)
        self.line += 1
        if var.type == 'array':
            self.PB[self.line] = '(ADD,{},{},{})'.format(t, address, t)
        else:
            self.PB[self.line] = '(ADD,{},#{},{})'.format(t, address, t)
        self.line += 1
        self.SS = self.SS[:-2]
        self.SS.append('{}'.format(t))

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
        self.PB[self.line] = '(JP,{},,)'.format(self.SS[-3] + 1)
        self.PB[self.SS[-3]] = '(JP,{},,)'.format(self.line + 1)
        self.line += 1
        self.SS = self.SS[:-3]

    def continue_routine(self):
        while_entry = self.get_symbol('while')
        if while_entry is not None:
            self.PB[self.line] = '(JP,{},,)'.format(while_entry.PB_line)
            self.line += 1

    def push0(self):
        self.SS.append('#0')
        # print(self.SS)

    def push1(self):
        self.SS.append('#1')

    def set_signature(self):
        #print(self.SS)
        func = self.get_symbol(self.SS[-2])
        func.type = self.SS[-3]
        t = self.get_temp()
        func.addr = t
        self.SS = self.SS[:-3]
        self.SS.append(func.lexeme)

        if func.lexeme == 'main' and func.type == 'void' and func.n_params == 0:
            self.main_defined_flag = True
            self.PB[0] = '(JP,{},,)'.format(self.line)

        if func.type == 'int':
            func.return_value = self.get_temp()
        # print(self.SS)

    def define_var(self):
        var_type = self.SS.pop()
        var_size, var_name, void_int = int(self.SS[-1][1:]), self.SS[-2], self.SS[-3]
        if void_int == 'void':
            print('Illegal type of void.')
        else:
            self.symbol_table.append(SymbolTableEntry(lexeme=var_name, type=var_type, addr=self.variables_SP, size=4 * var_size))
            if var_type == 'array':
                self.PB[self.line] = '(ASSIGN,#{},{},)'.format(self.values_SP, self.variables_SP)
                self.line += 1
                self.values_SP += 4 * var_size
            self.variables_SP += 4

        self.SS = self.SS[:-3]

    def define_param(self):
        print(self.SS)

        void_int, param_name, param_type = self.SS[-3], self.SS[-2], self.SS[-1]
        func_scope = self.scope_stack[-1]
        func_entry = self.symbol_table[func_scope]
        # adding the parameter to symbol table
        self.symbol_table.append(SymbolTableEntry(lexeme=param_name, type=param_type, addr=self.variables_SP, size=4))
        # print(func_entry.n_params)
        func_entry.add_param(self.variables_SP)  # adds the address of parameter to the function entry inside symbol table
        # print(func_entry.n_params)
        self.variables_SP += 4
        self.SS = self.SS[:-3]
        # print(self.SS)

    def main_defined_routine(self):
        if not self.main_defined_flag:
            print('main function not found!')

    def call_func(self):
        # print(self.SS)
        func_name, n_args = self.SS[-2], int(self.SS[-1][1:])
        func_entry = self.get_symbol(func_name)
        self.SS = self.SS[:-2]
        if func_entry is None:
            print('{} is not defined.'.format(func_name))
            self.SS.append(None)
        elif func_entry.n_params != n_args:
            print('Mismatch in numbers of arguments of {}.'.format(func_name))
        else:
            for param_addr in reversed(func_entry.params_addr):
                self.PB[self.line] = '(ASSIGN,{},{},)'.format(self.SS[-1], param_addr)
                self.line += 1
                self.SS = self.SS[:-1]


            # if func_entry.type != 'void':
            self.SS.append(func_entry.return_value)
            self.PB[self.line] = '(ASSIGN,#{},{},)'.format(self.line+2, func_entry.addr)
            self.line += 1
            self.PB[self.line] = '(JP,{},,)'.format(func_entry.PB_line)  # jump to the beginning of function
            self.line += 1

        # print(self.SS)

    def add_arg(self):
        # print(self.SS)
        new_arg = self.SS[-1]
        func = self.get_symbol(self.SS[-3])

        n_args, func_name = int(self.SS[-2][1:]), self.SS[-3]
        self.SS = self.SS[:-3]
        self.SS.append(new_arg)
        self.SS.append(func_name)
        self.SS.append('#' + str(n_args + 1))

    def return_routine_void(self):
        # print(self.SS)
        func = self.get_symbol(self.SS[-1])
        if func.type == 'int':
            print("missing return value!")
        self.PB[self.line] = '(JP,@{},,)'.format(func.addr)
        self.line += 1

    def return_routine_int(self):
        func = self.get_symbol(self.SS[-2])
        # print(self.SS, func.lexeme, func.addr, func.n_params, func.PB_line, func.type)
        expression = self.SS[-1]
        self.PB[self.line] = '(ASSIGN,{},{},)'.format(expression, func.return_value)
        self.line += 1
        self.PB[self.line] = '(JP,@{},,)'.format(func.addr)
        self.line += 1
        self.SS = self.SS[:-1]

    def has_params(self):
        self.SS.append('not_void')
        # print(self.SS)

    def push_simple(self):
        self.SS.append("simple")

    def push_array(self):
        self.SS.append("array")