'''
A simple interpreter for addition and subtraction

Inspired by tutorial from Ruslan Spivak

Author: GotoCode
'''

# input string --> lexer  --> token stream
# token stream --> parser --> *recognition*
# *after recognition* --> interpreter --> value


### Token types ###

INTEGER = 'INTEGER'
EOF     = 'EOF'
PLUS    = 'PLUS'
MINUS   = 'MINUS'


### Token - {type:t, value:v} ###

def make_token(type, value):

    return {'type' : type, 
            'value': value}


### LEXER CODE ###

def skip_whitespace(text, pos):
    
    while pos < len(text) and text[pos].isspace():
        pos += 1
    
    return pos

def make_integer(text, pos):
    
    result = ''
    while pos < len(text) and text[pos].isdigit():
        result += text[pos]
        pos += 1
    return (pos, result)

def make_lexer(text):
    
    pos       = 0
    
    # return appropriate token based on current_char
    while pos < len(text):
        
        curr_char = text[pos]
        
        if curr_char.isspace():
        
            pos = skip_whitespace(text, pos)
            
        elif curr_char.isdigit():
            
            (pos, int_string) = make_integer(text, pos)
            yield make_token(INTEGER, int(int_string))
        
        elif curr_char == '-':
            pos += 1
            yield make_token(MINUS, '-')
        
        elif curr_char == '+':
            pos += 1
            yield make_token(PLUS, '+')
        
        else:
            raise Exception('Unrecognized char at index: %d' % pos)
    
    # once out of bounds, any further calls yield EOF token
    while True:
        yield make_token(EOF, None)


### PARSER / INTERPRETER CODE ###

def eval(text):
    
    lexer = make_lexer(text)
    
    curr_token = lexer.next()
    
    if curr_token['type'] != INTEGER:
        raise Exception('Syntax Error')
    
    result = curr_token['value']
    
    curr_token = lexer.next()
    
    while curr_token['type'] != EOF:
        
        if curr_token['type'] == PLUS:
            result += lexer.next()['value']
        else:
            result -= lexer.next()['value']
        
        curr_token = lexer.next()
    
    return result


def main():
    #try:
    while True:
        input_str = raw_input('calc> ')
        result = eval(input_str)
        print result
    #except:
    #    print 'Goodbye!\n'


if __name__ == '__main__':
    main()

