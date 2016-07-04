
'''
An interpreter which handles operator precedence
'''

EOF     = 'EOF'
INTEGER = 'N'
PLUS    = '+'
MINUS   = '-'
TIMES   = '*'
DIVIDE  = '/'
LPAREN  = '('
RPAREN  = ')'


class Token(object):
    
    def __init__(self, type, value):
        self.type  = type
        self.value = value
    
    def __str__(self):
        return 'Token({type}, {value})'.format(type=self.type, value=self.value)


class Interpreter(object):
    
    def __init__(self, text):
        self.text       = text
        self.pos        = 0
        self.curr_char  = self.text[self.pos]
        self.curr_token = self.get_next_token()
    
    def advance(self):
        self.pos += 1
        if self.pos >= len(self.text):
            self.curr_char = None
        else:
            self.curr_char = self.text[self.pos]
    
    def consume(self, type):
        if self.curr_token.type == type:
            self.curr_token = self.get_next_token()
        else:
            raise Exception('Syntax error... %s', self.curr_token.type)
    
    def skip_whitespace(self):
        
        while self.pos < len(self.text) and self.curr_char.isspace():
            self.advance()
    
    def integer(self):
        
        result = ''
        while self.pos < len(self.text) and self.curr_char.isdigit():
            result += self.curr_char
            self.advance()
        return int(result)
    
    ## LEXER CODE ##
    
    def get_next_token(self):
        
        while self.curr_char is not None:
            
            if self.curr_char.isspace():
            
                self.skip_whitespace()
                continue
                
            elif self.curr_char.isdigit():
            
                self.curr_token = Token(INTEGER, self.integer())
                return self.curr_token
                
            elif self.curr_char == '+':
            
                self.curr_token = Token(PLUS, '+')
                self.advance()
                return self.curr_token
                
            elif self.curr_char == '-':
            
                self.curr_token = Token(MINUS, '-')
                self.advance()
                return self.curr_token
                
            elif self.curr_char == '*':
            
                self.curr_token = Token(TIMES, '*')
                self.advance()
                return self.curr_token
                
            elif self.curr_char == '/':
            
                self.curr_token = Token(DIVIDE, '/')
                self.advance()
                return self.curr_token
            
            elif self.curr_char == '(':
            
                self.curr_token = Token(LPAREN, '(')
                self.advance()
                return self.curr_token

            elif self.curr_char == ')':
            
                self.curr_token = Token(RPAREN, ')')
                self.advance()
                return self.curr_token
                
            else:
            
                raise Exception('Error')
        
        self.curr_token = Token(EOF, None)
        return self.curr_token

    # rule for +/-
    def expr(self):
        # expr : term ((+/-) term)*
        result = self.term()
        
        while self.curr_token.type in (PLUS, MINUS):
            
            op = self.curr_token
            
            if op.type == PLUS:
                self.consume(PLUS)
                result += self.term()
            elif op.type == MINUS:
                self.consume(MINUS)
                result -= self.term()
            
        return result
    
    # rule for TIMES/DIVIDE
    def term(self):
        # term : group ((TIMES/DIVIDE) group)*
        result = self.factor()
        
        while self.curr_token.type in (TIMES, DIVIDE):
            
            op = self.curr_token
            
            if op.type == TIMES:
                self.consume(TIMES)
                result *= self.factor()
            elif op.type == DIVIDE:
                self.consume(DIVIDE)
                result /= self.factor()
        
        return result
        
    # rule for base integer / parenthesized expression
    def factor(self):
        
        curr_token = self.curr_token
        result = None
        
        if curr_token.type == LPAREN:
            
            self.consume(LPAREN)
            result = self.expr()
            self.consume(RPAREN)
            
        else:
            
            self.consume(INTEGER)
            result = curr_token.value

        return result


def main():

    try:
    
        while True:
        
            input_str = raw_input('calc> ')
            if input_str == '': continue
            result    = Interpreter(input_str).expr()
            print result
    
    except EOFError:
        
        print 'Goodbye!\n'


if __name__ == '__main__':
    main()
