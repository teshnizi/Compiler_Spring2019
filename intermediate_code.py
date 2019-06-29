
class SemanticIntermediateCode:
    def __init__(self):
        self.SS = list()
        self.line = 0
        self.PB = dict()
        self.main_defined_flag = False

    def pid(self):
        pass  # TODO: find address of following ID in the rule and push it into the stack

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
        t = None
        self.PB[self.line] = '(MULT,{},{},{})'.format(self.SS[-2], self.SS[-1], t)
        self.SS = self.SS[:-2]
        self.SS.append(t)
        self.line += 1

    def add(self):
        t = None
        self.PB[self.line] = '(ADD,{},{},{})'.format(self.SS[-2], self.SS[-1], t)
        self.SS = self.SS[:-2]
        self.SS.append(t)
        self.line += 1

    def lt(self):
        t = None
        self.PB[self.line] = ('<', self.SS[-2], self.SS[-1], t)
        self.SS = self.SS[:-2]
        self.SS.append(t)
        self.line += 1

    def assign(self):
        self.PB[self.line] = '(ASSIGN,{},{},)'.format(self.SS[-1], self.SS[-2])
        self.SS = self.SS[-2]
        self.line += 1

    def addopp_routine(self):
        t = None  #TODO: get an address for t
        operand1, operand2, addop = self.SS[-3], self.SS[-2], self.SS[-1]
        self.PB[self.line] = '({},{},{})'.format(addop, operand1, operand2, t)
        self.SS = self.SS[:-3]
        self.SS.append(t)
        self.line += 1

    def neg(self):
        t = None  # TODO: get an address for t
        self.PB[self.line] = '(SUB,#0,{}, t)'.format(self.SS[-1])
        self.SS.pop()
        self.SS.append(t)
        self.line += 1

    def relop_routine(self):
        '''
        relop is SS[-2] (either < or ==)
        fill the current line of program block with the appropriate command
        '''
        self.PB[self.line] = '({},{},{})'.format(self.SS[-2], self.SS[-3], self.SS[-1])
        self.line += 1
        self.SS = self.SS[:-3]

    def pop_expression(self):
        '''
        pops the value of expression from SS
        '''
        self.SS.pop()

    def label(self):
        self.SS.append(self.line)

    def save(self):
        self.SS.append(self.line)
        self.line += 1

    def jpf_save(self):
        self.PB[self.SS[-1]] = '(jpf,{},{},)'.format(self.SS[-2], self.line + 1)
        self.SS = self.SS[-2]
        self.SS.append(self.line)
        self.line += 1

    def jp(self):
        self.PB[self.SS[-1]] = '(jp,{},,)'.format(self.line)
        self.SS.pop()

    def while_loop(self):
        self.PB[self.SS[-1]] =  '(jpf,{},{},)'.format(self.SS[-2], self.line + 1)
        self.PB[self.line] =  '(jp,{},,)'.format(self.SS[-3])
        self.line += 1
        self.SS = self.SS[-3]

    def continue_routine(self):
        pass

    def define_var(self):
        var_name, var_type = self.SS[-1], self.SS[-2]
        if var_type == 'void':
            print('Illegal type of void.')
        else:
            pass  # TODO: assign an address to the defined variable

        self.SS = self.SS[-2]

    def check_main(self):
        func_type, func_name  = self.SS[-2], self.SS[-1]
        if func_type == 'void' and func_name == 'main':
            self.main_defined_flag = True

    def define_arr(self):
        pass  # TODO: assign an address to the defined array

    def main_defined_routine(self):
        if not self.main_defined_flag:
            print('main function not found!')

    def return_routine(self):
        pass  # TODO: perhaps a jump to the next line of calling the callee from caller! address is on top of stack?

    def find_addr(self, input):
        pass  # TODO: find the adrress of ID in memory

    def set_addr(self, input_token):
        pass