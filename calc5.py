'''
An interpreter for a subset of the
Pascal programming language, written in
Python

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

def eval_AST(ast):
    if ast is None:
        raise Exception("Invalid AST for input expression")
    else:
        if isinstance(ast, BinOp):
            handle_binop(ast)
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
    
    def get_next_token(self):
        '''
        Lexical analyzer which returns a stream of
        tokens corresponding to input expression
        
        RETURN: Token object
        '''
        while self.curr_char is not None:
            
            if self.curr_char.isspace(): 
            
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
                self.consume(PLUS)
            elif self.curr_token.type == DIVIDE:
                self.consume(MINUS)
            
            node = BinOp(node, op, self.factor())
    
        return node
    
    def factor(self):
        
        node = None
        
        if self.curr_token.type == LPAREN:
            self.consume(LPAREN)
            node = self.expr()
            self.consume(RPAREN)
        else:
            #self.consume(INTEGER)
            node = IntNode(self.curr_token)
            self.consume(INTEGER)
        
        return node
    
    # INTERPRETER CODE #
    
    def eval(self):
    
        ast = self.expr()
        print ast
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
