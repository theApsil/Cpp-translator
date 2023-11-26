from enum import Enum


class LexemeType(Enum):
    # Operators
    PLUS = 'LEXEME-PLUS'
    INCREMENT = 'LEXEME-INCREMENT'
    MINUS = 'LEXEME-MINUS'
    DECREMENT = 'LEXEME-DECREMENT'
    MULTIPLICATION = 'LEXEME-MULTIPLICATION'
    DIVISION = 'LEXEME-DIVISION'
    MOD = 'LEXEME-MOD'
    ASSIGNMENT = 'LEXEME-ASSIGNMENT'
    EQUAL = 'LEXEME-EQUAL'
    NOT_EQUAL = 'LEXEME-NOT_EQUAL'
    LESS_THAN = 'LEXEME-LESS_THAN'
    MORE_THAN = 'LEXEME-MORE_THAN'
    LESS_OR_EQUAL = 'LEXEME-LESS_OR_EQUAL'
    MORE_OR_EQUAL = 'LEXEME-MORE_OR_EQUAL'
    NOT = 'LEXEME-NOT'
    AND = 'LEXEME-AND'
    OR = 'LEXEME-OR'

    # Data type
    VOID = 'LEXEME-VOID'
    INT = 'LEXEME-INT'
    LONG = 'LEXEME-LONG'
    SHORT = 'LEXEME-SHORT'
    UNSIGNED = 'LEXEME-UNSIGNED'
    BOOL = 'LEXEME-BOOL'
    FLOAT = 'LEXEME-FLOAT'
    DOUBLE = 'LEXEME-DOUBLE'
    CHAR = 'LEXEME-CHAR'

    # Cycle operators
    FOR = 'LEXEME-FOR'
    WHILE = 'LEXEME-WHILE'

    # Branching operators
    IF = 'LEXEME-IF'
    ELSE = 'LEXEME-ELSE'

    # Reserved constants
    TRUE = 'LEXEME-TRUE'
    FALSE = 'LEXEME-FALSE'

    # Reserved service names
    INCLUDE = 'LEXEME-INCLUDE'
    STD = 'LEXEME-STD'
    MAIN = 'LEXEME-MAIN'
    RETURN = 'LEXEME-RETURN'

    # Reserved functions names
    COUT = 'LEXEME-COUT'
    CIN = 'LEXEME-CIN'
    ABS = 'LEXEME-ABS'
    SQR = 'LEXEME-SQR'
    SQRT = 'LEXEME-SQRT'
    POW = 'LEXEME-POW'
    FLOOR = 'LEXEME-FLOOR'
    CEIL = 'LEXEME-CEIL'

    # Separators
    ROUND_OPEN_BRACKET = 'LEXEME-ROUND_OPEN_BRACKET'
    ROUND_CLOSE_BRACKET = 'LEXEME-ROUND_CLOSE_BRACKET'
    CURLY_OPEN_BRACKET = 'LEXEME-CURLY_OPEN_BRACKET'
    CURLY_CLOSE_BRACKET = 'LEXEME-CURLY_CLOSE_BRACKET'
    SQUARE_OPEN_BRACKET = 'LEXEME-SQUARE_OPEN_BRACKET'
    SQUARE_CLOSE_BRACKET = 'LEXEME-SQUARE_CLOSE_BRACKET'
    SEMICOLON = 'LEXEME-SEMICOLON'
    COLON = 'LEXEME-COLON'

    # Number type
    INT_NUMBER = 'LEXEME-INT_NUMBER'
    REAL_NUMBER = 'LEXEME-REAL_NUMBER'
    EXPONENTIAL_NUMBER = 'LEXEME-EXPONENTIAL_NUMBER'
    # VAR_NAME = 'LEXEME-VAR_NAME'

    # Char data
    CHAR_DATA = 'LEXEME-CHAR_DATA'
    STRING_DATA = 'LEXEME-STRING_DATA'

    WORD = 'LEXEME-WORD'

    UNDEFINED = 'LEXEME-UNDEFINED'

    EOF = 'LEXEME-END_OF_FILE'


DictionaryOfLexemes = {
    # Operators
    '+': LexemeType.PLUS,
    '++': LexemeType.INCREMENT,
    '-': LexemeType.MINUS,
    '--': LexemeType.DECREMENT,
    '*': LexemeType.MULTIPLICATION,
    '/': LexemeType.DIVISION,
    '%': LexemeType.MOD,
    '=': LexemeType.ASSIGNMENT,
    '==': LexemeType.EQUAL,
    '!=': LexemeType.NOT_EQUAL,
    '<': LexemeType.LESS_THAN,
    '>': LexemeType.MORE_THAN,
    '<=': LexemeType.LESS_OR_EQUAL,
    '>=': LexemeType.MORE_OR_EQUAL,
    '!': LexemeType.NOT,
    '&&': LexemeType.AND,
    '||': LexemeType.OR,

    # Data type
    'void': LexemeType.VOID,
    'int': LexemeType.INT,
    'long': LexemeType.LONG,
    'short': LexemeType.SHORT,
    'unsigned': LexemeType.UNSIGNED,
    'bool': LexemeType.BOOL,
    'float': LexemeType.FLOAT,
    'double': LexemeType.DOUBLE,
    'char': LexemeType.CHAR,

    # Cycle operators
    'for': LexemeType.FOR,
    'while': LexemeType.WHILE,

    # Branching operators
    'if': LexemeType.IF,
    'else': LexemeType.ELSE,

    # Reserved constants
    'true': LexemeType.TRUE,
    'false': LexemeType.FALSE,

    # Reserved service names
    'include': LexemeType.INCLUDE,
    'std': LexemeType.STD,
    'main': LexemeType.MAIN,
    'return': LexemeType.RETURN,

    # Reserved functions names
    'cout': LexemeType.COUT,
    'cin': LexemeType.CIN,
    'abs': LexemeType.ABS,
    'sqr': LexemeType.SQR,
    'sqrt': LexemeType.SQRT,
    'pow': LexemeType.POW,
    'floor': LexemeType.FLOOR,
    'ceil': LexemeType.CEIL,

    # Separators
    '(': LexemeType.ROUND_OPEN_BRACKET,
    ')': LexemeType.ROUND_CLOSE_BRACKET,
    '{': LexemeType.CURLY_OPEN_BRACKET,
    '}': LexemeType.CURLY_CLOSE_BRACKET,
    '[': LexemeType.SQUARE_OPEN_BRACKET,
    ']': LexemeType.SQUARE_CLOSE_BRACKET,
    ';': LexemeType.SEMICOLON,
    ':': LexemeType.COLON,

}