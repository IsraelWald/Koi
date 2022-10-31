from typing import List

# https://www.craftinginterpreters.com/parsing-expressions.html#syntax-errors
from .expr import Binary, Grouping, Literal, Unary
from .stmt import Expression, Stmt
from .token_type import TokenType
from .token import Token
from .stmt import Print


class ParseError(Exception):
    def __init__(self, token: Token, message: str):
        self.token = token
        self.message = message
        super().__init__(self.message)


class Parser:
    def __init__(self, tokens: List[Token], on_error=None):
        self.tokens = tokens
        self.current = 0
        self.on_error = on_error

    def parse(self) -> List[Stmt]:
        statements: List[Stmt] = []
        while not self.is_at_end():
            statements.append(self._statement())
        return statements

    def _statement(self) -> Stmt:
        if self.match(TokenType.PRINT):
            return self._print_statement()
        return self._expression_statement()

    def _print_statement(self) -> Stmt:
        value = self._expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value")
        return Print(value)

    def _expression_statement(self) -> Stmt:
        expr = self._expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value")
        return Expression(expr)

    def _expression(self):
        return self.equality()

    def equality(self):
        expr = self.comparison()

        while self.match(TokenType.BANG, TokenType.BANG_EQUAL):
            op = self.previous()
            right = self.comparison()
            expr = Binary(expr, op, right)

        return expr

    def comparison(self):
        expr = self.term()

        while self.match(
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ):
            op = self.previous()
            right = self.term()
            expr = Binary(expr, op, right)
        return expr

    def term(self):
        expr = self.factor()

        while self.match(TokenType.MINUS, TokenType.PLUS):
            op = self.previous()
            right = self.factor()
            expr = Binary(expr, op, right)

        return expr

    def factor(self):
        expr = self.unary()

        while self.match(TokenType.SLASH, TokenType.STAR, TokenType.MOD):
            op = self.previous()
            right = self.unary()
            expr = Binary(expr, op, right)

        return expr

    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS):
            op = self.previous()
            right = self.unary()
            return Unary(op, right)
        else:
            return self.primary()

    def primary(self):
        if self.match(TokenType.FALSE):
            return Literal(False)
        elif self.match(TokenType.TRUE):
            return Literal(True)
        elif self.match(TokenType.NIL):
            return Literal(None)
        elif self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)
        elif self.match(TokenType.LEFT_PAREN):
            expr = self.equality()
            self.consume(TokenType.RIGHT_PAREN, "Expected ')' after expression")
            return Grouping(expr)

        raise self._error(self.peek(), "Expected Expression")

    def consume(self, tok_type: TokenType, message: str):
        if self.check(tok_type):
            return self.advance()
        raise self._error(self.peek(), message)

    def match(self, *token_types: List[TokenType]):
        for token_type in token_types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def check(self, tok_type: TokenType):
        if self.is_at_end():
            return False
        return self.peek().tok_type == tok_type

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self) -> bool:
        return self.peek().tok_type == TokenType.EOF

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def _error(self, token: Token, message: str):
        self.on_error(token, message)
        raise ParseError(token, message)

    def _synchronize(self):
        self.advance()

        while not self.is_at_end():
            if self.previous().tok_type == TokenType.SEMICOLON:
                return
            match self.peek().tok_type:
                case TokenType.CLASS | TokenType.FUNC | TokenType.VAR | TokenType.FOR | TokenType.IF | TokenType.WHILE | TokenType.PRINT | TokenType.RETURN:
                    return
            self.advance()
