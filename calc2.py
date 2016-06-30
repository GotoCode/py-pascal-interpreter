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


# An Interpreter which converts a single-line
# expression into a stream of tokens

class Interpreter(object):
    
    def __init__(self, text):
        # input expression
        self.text = text
        # pointer to current symbol
        self.pos  = 0
        # most recent token available for processing
        self.curr_token = None
        # character being pointed at by 'pos' index
        self.curr_char = self.text[self.pos]
        
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

    def eval(self):
        '''
        Evaluate the given input expression
        '''
        self.curr_token = self.get_next_token()
        
        # Check for pattern 'INTEGER PLUS INTEGER'
        
        # first int operand
        first = self.curr_token.value
        self.consume(INTEGER)
        
        # plus/minus operator
        op = self.curr_token
        
        if op.type == PLUS:
            self.consume(PLUS)
        elif op.type == MINUS:
            self.consume(MINUS)
        elif op.type == MULTIPLY:
            self.consume(MULTIPLY)
        else:
            self.consume(DIVIDE)
        
        # second int operand
        second = self.curr_token.value
        self.consume(INTEGER)
        
        # based on pattern return appropriate result
        if op.type == PLUS:
            out_val = first + second
        elif op.type == MINUS:
            out_val = first - second
        elif op.type == MULTIPLY:
            out_val = first * second
        else:
            out_val = first / second
        
        return out_val
    
    
    def remove_whitespace(self):
        '''
        "cleans up" the input string by extracting
        only those non-whitespace characters from it
        '''
        result_text = ''
        
        for i in range(len(self.text)):
            if not self.text[i].isspace():
                result_text += self.text[i]
        
        self.text = result_text


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
