from typing import List

from .expr import Binary, Grouping, Literal, Unary
from .token_type import TokenType
from .token import Token


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0

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

        while self.match(TokenType.SLASH, TokenType.STAR):
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
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expected ')' after expression")
            return Grouping(expr)

    def consume(self, tok_type, message):
        if self.check(tok_type):
            return self.advance()
        raise self.error(self.peek(), message)

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

    def is_at_end(self):
        return self.peek().tok_type == TokenType.EOF

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]
