import enum
from typing_extensions import Self


class TokenType(enum.Enum):
    """
    Tokens that are used in the language. The mapping from Enum to character
    will be done in the scanner.
    """

    # Single char tokens
    LEFT_PAREN: Self
    RIGHT_PAREN: Self
    LEFT_BRACE: Self
    RIGHT_BRACE: Self
    COMMA: Self
    DOT: Self
    MINUS: Self
    PLUS: Self
    SEMICOLON: Self
    SLASH: Self
    STAR: Self
    # One or two char tokens
    BANG: Self
    BANG_EQUAL: Self
    EQUAL: Self
    EQUAL_EQUAL: Self
    GREATER: Self
    GREATER_EQUAL: Self
    LESS: Self
    LESS_EQUAL: Self
    # Literals
    IDENTIFIER: Self
    STRING: Self
    NUMBER: Self
    # Keywords
    AND: Self
    OR: Self
    NOT: Self
    IF: Self
    ELSE: Self
    CLASS: Self
    TRUE: Self
    FALSE: Self
    NIL: Self
    FUNC: Self
    FOR: Self
    WHILE: Self
    PRINT: Self
    RETURN: Self
    SUPER: Self
    THIS: Self
    VAR: Self

    EOF: Self
