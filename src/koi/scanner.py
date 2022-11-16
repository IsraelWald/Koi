from typing import Any, List

from .token import Token
from .token_type import TokenType


class Scanner:
    tokens: List
    start: int = 0
    current: int = 0
    line: int = 0
    keywords = {
        "and": TokenType.AND,
        "or": TokenType.OR,
        "not": TokenType.NOT,
        "if": TokenType.IF,
        "else": TokenType.ELSE,
        "class": TokenType.CLASS,
        "true": TokenType.TRUE,
        "false": TokenType.FALSE,
        "nil": TokenType.NIL,
        "inherits": TokenType.INHERITS,
        "fun": TokenType.FUNC,
        "for": TokenType.FOR,
        "while": TokenType.WHILE,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "var": TokenType.VAR,
    }

    def __init__(self, source: str, on_error=None) -> None:
        """
        Create a new Scanner that will scan `source`.
        `on_error` will be called when an error is encountered.
        """
        self.source = source
        self.on_error = on_error
        self.tokens = []

    def scan_tokens(self) -> List[Token]:
        while not self._is_at_end():
            # We're at the start of the next lexeme
            self.start = self.current
            self._scan_tokens()
        # Add an EOF as the last token
        self.tokens.append(
            Token(token_type=TokenType.EOF, lexeme="", literal=None, line=self.line)
        )
        return self.tokens

    def _operator_slash(self):
        if self._match("/"):  # We got a '//'
            # A comment goes until the end of the line
            while self._peek() != "\n" and not self._is_at_end():
                self._advance()
        else:  # We got a '/'
            self._add_token(TokenType.SLASH)

    def _operator_newline(self):
        self.line += 1

    def _string(self):
        while self._peek() != '"' and not self._is_at_end():
            if self._peek() == "\n":
                self.line += 1
            self._advance()

        # Unterminated string
        if self._is_at_end():
            self.on_error(self.line, "Unterminated string")  # type: ignore
            return

        # Advance past the "
        self._advance()

        # Rip off the surrounding ""
        string_value = self.source[self.start + 1 : self.current - 1]
        self._add_token(TokenType.STRING, string_value)

    def _number(self):
        while self._peek().isdigit():
            self._advance()

        # Look for a decimal
        if self._peek() == "." and self._peek_next().isdigit():
            # Eat the '.'
            self._advance()
            # Eat the decimal
            while self._peek().isdigit():
                self._advance()

        number_value = self.source[self.start : self.current]
        self._add_token(TokenType.NUMBER, float(number_value))

    def _identifier(self):
        while self._peek().isalnum() or self._peek() == "_":
            self._advance()

        # Check if identifier is a keyword
        text = self.source[self.start : self.current]
        token_type = self.keywords.get(text, TokenType.IDENTIFIER)

        self._add_token(token_type)

    def _scan_tokens(self):
        """Scan tokens"""
        # Get the first token
        c = self._advance()

        match c:
            case "(":
                self._add_token(TokenType.LEFT_PAREN)
            case ")":
                self._add_token(TokenType.RIGHT_PAREN)
            case "{":
                self._add_token(TokenType.LEFT_BRACE)
            case "}":
                self._add_token(TokenType.RIGHT_BRACE)
            case ",":
                self._add_token(TokenType.COMMA)
            case ".":
                self._add_token(TokenType.DOT)
            case "-":
                self._add_token(TokenType.MINUS)
            case "+":
                self._add_token(TokenType.PLUS)
            case ";":
                self._add_token(TokenType.SEMICOLON)
            case "*":
                self._add_token(TokenType.STAR)
            case "%":
                self._add_token(TokenType.MOD)
            case "!":
                self._add_token(
                    TokenType.BANG_EQUAL if self._match("=") else TokenType.BANG
                )
            case "=":
                self._add_token(
                    TokenType.EQUAL_EQUAL if self._match("=") else TokenType.EQUAL
                )
            case "<":
                self._add_token(
                    TokenType.LESS_EQUAL if self._match("=") else TokenType.LESS
                )
            case ">":
                self._add_token(
                    TokenType.GREATER_EQUAL if self._match("=") else TokenType.GREATER
                )
            case "/":
                self._operator_slash()
            case " ":
                return None
            case "\r":
                return None
            case "\t":
                return None
            case "\n":
                self._operator_newline()
            case '"':
                self._string()
            case _:
                if c.isdigit():
                    # A digit, make a number
                    self._number()
                elif c.isalpha() or c == "_":
                    # A letter, make an identifier
                    self._identifier()
                elif self.on_error:
                    self.on_error(self.line, f"Unexpected char {c}")  # type: ignore
                else:
                    raise

    def _is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def _advance(self) -> str:
        self.current += 1
        return self.source[self.current - 1]

    def _peek(self) -> str:
        if self._is_at_end():
            return "\0"
        return self.source[self.current]

    def _peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def _add_token(self, token_type: TokenType, literal: Any = None) -> None:
        text = self.source[self.start : self.current]
        self.tokens.append(
            Token(token_type=token_type, lexeme=text, literal=literal, line=self.line)
        )

    def _match(self, expected: str) -> bool:
        if self._is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True
