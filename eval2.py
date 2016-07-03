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
TIMES   = 'TIMES'
DIVIDE  = 'DIVIDE'


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

def consume(lexer, type):

    curr_token = lexer.next()
    if curr_token.type != EOF and curr_token.type == type:
        return curr_token.value
    else:
        raise Exception('Syntax error...')

def make_lexer(text):
    
    pos = 0
    
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
        
        elif curr_char == '*':
            pos += 1
            yield make_token(TIMES, '*')
        
        elif curr_char == '/':
            pos += 1
            yield make_token(DIVIDE, '/')
        
        else:
            raise Exception('Unrecognized char at index: %d' % pos)
    
    # once out of bounds, any further calls yield EOF token
    while True:
        yield make_token(EOF, None)


### PARSER / INTERPRETER CODE ###

def expr(lexer):
    # expr : term ((+/-) term)*
    
    result = term(lexer)
    
    op = lexer.next()
    
    while op.type in (PLUS, MINUS):
        if   op.value == '+':
            result += term(lexer)
        elif op.value == '-':
            result -= term(lexer)
    
    return result

def term(lexer):
    # term : factor ((TIMES/DIVIDE) factor)*
    
    result = factor(lexer)
    
    op = lexer.next()
    
    while op.type in (TIMES, DIVIDE):
        if op.value == '*':
            result *= factor(lexer)
        elif op.value == '/':
            result /= factor(lexer)
    
    return result

def factor(lexer):

    return consume(lexer, INTEGER)


def main():

    while True:
        input_str = raw_input('calc> ')
        lexer     = make_lexer(input_str)
        result    = expr(lexer)
        print result


if __name__ == '__main__':
    main()

