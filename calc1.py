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

