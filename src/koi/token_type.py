import enum


class TokenType(enum.Enum):
    """
    Tokens that are used in the language. The mapping from Enum to character
    will be done in the scanner.
    """

    # Single char tokens
    LEFT_PAREN = enum.auto()
    RIGHT_PAREN = enum.auto()
    LEFT_BRACE = enum.auto()
    RIGHT_BRACE = enum.auto()
    COMMA = enum.auto()
    DOT = enum.auto()
    MINUS = enum.auto()
    PLUS = enum.auto()
    SEMICOLON = enum.auto()
    SLASH = enum.auto()
    STAR = enum.auto()
    # One or two char tokens
    BANG = enum.auto()
    BANG_EQUAL = enum.auto()
    EQUAL = enum.auto()
    EQUAL_EQUAL = enum.auto()
    GREATER = enum.auto()
    GREATER_EQUAL = enum.auto()
    LESS = enum.auto()
    LESS_EQUAL = enum.auto()
    # Literals
    IDENTIFIER = enum.auto()
    STRING = enum.auto()
    NUMBER = enum.auto()
    # Keywords
    AND = enum.auto()
    OR = enum.auto()
    NOT = enum.auto()
    IF = enum.auto()
    ELSE = enum.auto()
    CLASS = enum.auto()
    TRUE = enum.auto()
    FALSE = enum.auto()
    NIL = enum.auto()
    FUNC = enum.auto()
    FOR = enum.auto()
    WHILE = enum.auto()
    PRINT = enum.auto()
    RETURN = enum.auto()
    SUPER = enum.auto()
    THIS = enum.auto()
    VAR = enum.auto()

    EOF = enum.auto()
