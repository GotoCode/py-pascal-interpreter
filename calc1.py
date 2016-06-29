'''
An interpreter for a subset of the
Pascal programming language, written in
Python

Inspired by tutorial by Ruslan Spivak

Author: GotoCode
'''


# Token Types

INTEGER = 'INTEGER'
PLUS    = 'PLUS'
MINUS   = 'MINUS'
EOF     = 'EOF'


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
        # 'clean up' the input string
        self.remove_whitespace()
        # pointer to current symbol
        self.pos  = 0
        # most recent token available for processing
        self.curr_token = None
    
    def error(self):
        raise Exception('Error parsing input...')
    
    def get_next_token(self):
        '''
        Lexical analyzer which returns a stream of
        tokens corresponding to input expression
        
        RETURN: Token object
        '''
        text = self.text
        
        # if we reached end-of-input, return EOF
        if self.pos >= len(text):
            return Token(EOF, None)
        
        # convert current (character) symbol to appropriate token
        
        symbol = text[self.pos]
        
        if symbol.isdigit():
            
            # extract multi-digit integer
            num_str  = ''
            
            while self.pos < len(text) and text[self.pos].isdigit():
                num_str  += text[self.pos]
                self.pos += 1
            
            token = Token(INTEGER, int(num_str))
            
        elif symbol == '+':
            token = Token(PLUS, symbol)
            self.pos += 1
        elif symbol == '-':
            token = Token(MINUS, symbol)
        else:
            token = None
        
        if not token:
            self.error()
        else:
            return token
    
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
        
        try:
            self.consume(PLUS)
        except:
            self.consume(MINUS)
        
        # second int operand
        second = self.curr_token.value
        self.consume(INTEGER)
        
        # based on pattern return appropriate evaluation
        if op.type == PLUS:
            out_val = first + second
        else:
            out_val = first - second
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
