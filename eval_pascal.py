'''
An interpreter for a subset of the
Pascal programming language, written in
Python

(with support for unary +/- operators)

Inspired by tutorial from Ruslan Spivak

Author: GotoCode
'''


# Token Types

INTEGER  = 'INTEGER'
PLUS     = 'PLUS'
MINUS    = 'MINUS'
MULTIPLY = 'MULTIPLY'
DIVIDE   = 'DIVIDE'
LPAREN   = 'LPAREN'
RPAREN   = 'RPAREN'
EOF      = 'EOF'

# Pascal token types

BEGIN  = 'BEGIN'
END    = 'END'
ASSIGN = 'ASSIGN'
ID     = 'ID'
DOT    = 'DOT'
SEMI   = 'SEMI'

# A Token is a pair - (type, value)

class Token(object):
    
    def __init__(self, type, value):
        self.type  = type
        self.value = value
    
    def __str__(self):
        return 'Token({type}, {value})'.format(type=self.type, value=self.value)
    
    def __repr__(self):
        return self.__str__()


# Abstract Syntax Tree #

class BinOp(object):
    def __init__(self, left, op, right):
        self.left  = left
        self.op    = op
        self.right = right
    
    def __str__(self):
        return 'BinOp({left}, {op}, {right})'.format(left=str(self.left), 
                                                     op=self.op.type, 
                                                     right=str(self.right))

class IntNode(object):
    def __init__(self, token):
        self.token = token
        self.value = token.value
    
    def __str__(self):
        return 'IntNode(%d)' % self.value

class UnaryOp(object):
    def __init__(self, op, expr):
        self.op   = op
        self.expr = expr
    
    def __str__(self):
        return 'UnaryOp({op}, {expr})'.format(op=self.op.type, expr=str(self.expr))

class CompoundNode(object):
    def __init__(self):
        self.children = []

class Assign(object):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Var(object):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class NoOp(object):
    pass


# AST traversal functions (i.e. evaluation) #

# post-order traversal 
def handle_binop(binop_node):
    
    left_val  = eval_AST(binop_node.left)
    right_val = eval_AST(binop_node.right)
    
    op_type = binop_node.op.type
    
    #print binop_node.op
    
    if op_type == PLUS:
        return left_val + right_val
    elif op_type == MINUS:
        return left_val - right_val
    elif op_type == MULTIPLY:
        return left_val * right_val
    elif op_type == DIVIDE:
        return left_val / right_val
    else:
        raise Exception("Unknown operator found")

def handle_unaryop(unaryop_node):
    
    result = eval_AST(unaryop_node.expr)
    
    op_type = unaryop_node.op.type
    
    if op_type == PLUS:
        return +result
    else:
        return -result


# good ol' fashioned evaluation of arithmetic expressions

def eval_AST(ast):
    if ast is None:
        raise Exception("Invalid AST for input expression")
    else:
        if isinstance(ast, BinOp):
            return handle_binop(ast)
        elif isinstance(ast, UnaryOp):
            return handle_unaryop(ast)
        elif isinstance(ast, IntNode):
            return ast.value


# An Interpreter which converts a single-line
# expression into a stream of tokens

class Interpreter(object):
    
    def __init__(self, text):
        # input expression
        self.text = text
        # pointer to current symbol
        self.pos  = 0
        # character being pointed at by 'pos' index
        self.curr_char = self.text[self.pos]
        # most recent token available for processing
        self.curr_token = self.get_next_token()
        
    def error(self):
        raise Exception('Error parsing input...')
    
    def advance(self):
        '''
        Advance the pos pointer forward by one,
        updating both pos and curr_char
        '''
        self.pos += 1
        
        if self.pos >= len(self.text):
            self.curr_char = None
        else:
            self.curr_char = self.text[self.pos]
    
    def skip_whitespace(self):
        '''
        Skip over chars until first non-whitespace char is found
        '''
        while self.curr_char is not None and self.curr_char.isspace():
            self.advance()
    
    def integer(self):
        '''
        Return an integer value based on multi-digit number
        '''
        result = ''
        
        while self.curr_char is not None and self.curr_char.isdigit():
            result += self.curr_char
            self.advance()
        
        return int(result)
    
    ### LEXER CODE ###
    
    # look ahead at next char of input expression
    def peek(self):
    
        next_pos = self.pos + 1
        
        if next_pos > len(self.text):
            return None
        else:
            return self.text[next_pos]
    
    # create token for variables and reserved keywords
    def _id(self):
    
        RESERVED_KEYWORDS = {'BEGIN':Token('BEGIN', 'BEGIN'),
                             'END':Token('END', 'END')}
        result = ''
        
        while self.curr_char != None and self.curr_char.isalnum():
            result += self.curr_char
            
        return RESERVED_KEYWORDS.get(result, Token(ID, result))
    
    def get_next_token(self):
        '''
        Lexical analyzer which returns a stream of
        tokens corresponding to input expression
        
        RETURN: Token object
        '''
        while self.curr_char is not None:
            
            if self.curr_char.isalpha():
                
                return self._id()
            
            elif self.curr_char == ':' and self.peek() == '=':
                
                self.advance()
                self.advance()
                return Token(ASSIGN, ':=')
            
            elif self.curr_char == '.':
                
                self.advance()
                return Token(DOT, '.')
            
            elif self.curr_char == ';':
                
                self.advance()
                return Token(SEMI, ';')
            
            elif self.curr_char.isspace(): 
            
                self.skip_whitespace()
                continue
                
            elif self.curr_char.isdigit():
            
                return Token(INTEGER, self.integer())
                
            elif self.curr_char == '+':
            
                self.advance()
                return Token(PLUS, '+')
                
            elif self.curr_char == '-':
            
                self.advance()
                return Token(MINUS, '-')
            
            elif self.curr_char == '*':
                
                self.advance()
                return Token(MULTIPLY, '*')
            
            elif self.curr_char == '/':
                
                self.advance()
                return Token(DIVIDE, '/')
            
            elif self.curr_char == '(':
                
                self.advance()
                return Token(LPAREN, '(')
            
            elif self.curr_char == ')':
                
                self.advance()
                return Token(RPAREN, ')')
                
            else:
                self.error()
        
        return Token(EOF, None)
    
    def consume(self, type):
        '''
        If the given type matches that of the
        current token, then consume it, else
        raise an error
        '''
        if type == self.curr_token.type:
            self.curr_token = self.get_next_token()
        else:
            self.error()
    
    ### PARSER CODE ###
    
    def expr(self):
        
        node = self.term()
        
        #print 'Hello!'
        #print self.curr_token
        
        while self.curr_token.type in (PLUS, MINUS):
            
            op = self.curr_token
            
            if self.curr_token.type == PLUS:
                self.consume(PLUS)
            elif self.curr_token.type == MINUS:
                self.consume(MINUS)
            
            node = BinOp(node, op, self.term())
        
        return node
    
    def term(self):
    
        node = self.factor()
        
        while self.curr_token.type in (MULTIPLY, DIVIDE):
            
            op = self.curr_token
            
            if self.curr_token.type == MULTIPLY:
                self.consume(MULTIPLY)
            elif self.curr_token.type == DIVIDE:
                self.consume(DIVIDE)
            
            node = BinOp(node, op, self.factor())
    
        return node
    
    def factor(self):
        
        node = None
        
        #print self.curr_token
        
        if self.curr_token.type == LPAREN:
            self.consume(LPAREN)
            node = self.expr()
            self.consume(RPAREN)
        elif self.curr_token.type == PLUS:
            self.consume(PLUS)
            node = UnaryOp(Token(PLUS, 'PLUS'), self.factor())
        elif self.curr_token.type == MINUS:
            self.consume(MINUS)
            node = UnaryOp(Token(MINUS, 'MINUS'), self.factor())
        else:
            #self.consume(INTEGER)
            node = IntNode(self.curr_token)
            self.consume(INTEGER)
        
        return node
    
    def program(self):
        '''program : compound_statement DOT'''
        node = self.compound_statement()
        self.consume(DOT)
        return node
    
    def compound_statement(self):
        '''compound_statement : BEGIN statement_list END'''
        self.consume(BEGIN)
        node = self.statement_list()
        self.consume(END)
        return node
    
    def statement_list(self):
        '''statement_list : statement | statement SEMI statement_list'''
        s = self.statement()
        
        children = [s]
        
        while self.curr_token.type == SEMI:
            self.consume(SEMI)
            children.append(self.statement())
        
        node = CompoundNode()
        node.children = children
        
        return node
    
    def statement(self):
        '''statement : compound_statement | assignment_statement | empty'''
        
        node = None
        
        if self.curr_token.type == BEGIN:
            node = self.compound_statement()
        elif self.curr_token.type == ID:
            node = self.assignment_statement()
        else:
            node = NoOp()
        
        return node
    
    def assignment_statement(self):
        '''assignment_statement : variable ASSIGN expr'''
        left  = self.variable()
        token = self.curr_token
        self.consume(ASSIGN)
        right = self.expr()
        
        return Assign(left, token, right)
    
    # INTERPRETER CODE #
    
    def eval(self):
    
        ast = self.expr()
        return eval_AST(ast)
    

def main():
    '''
    Main logic for presenting CLI to user of interpreter
    '''
    while True:

        try:
            input_expr = raw_input('calc> ')
        except EOFError:
            print
            break
        
        # ignore any empty lines of input
        if not input_expr:
            continue
        
        interpreter = Interpreter(input_expr)
        result = interpreter.eval()
        
        print result


if __name__ == '__main__':
    main()
