from typing import List

# https://www.craftinginterpreters.com/parsing-expressions.html#syntax-errors
from .expr import Binary, Grouping, Literal, Logical, Unary, Expr, Variable, Assign
from .stmt import Expression, Stmt, Var, Block, If, While
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
            statements.append(self._declaration())
        return statements

    def _declaration(self) -> Stmt:
        try:
            if self.match(TokenType.VAR):
                return self._var_declaration()
            return self._statement()
        except ParseError:
            self._synchronize()
            return None

    def _var_declaration(self) -> Stmt:
        name: Token = self.consume(TokenType.IDENTIFIER, "Expected identifier")
        init_val: Expr | None = None
        if self.match(TokenType.EQUAL):
            init_val = self._expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after variable declaration.")
        return Var(name, init_val)

    def _statement(self) -> Stmt:
        if self.match(TokenType.PRINT):
            return self._print_statement()
        if self.match(TokenType.IF):
            return self._if_statement()
        if self.match(TokenType.LEFT_BRACE):
            return Block(self._block())
        if self.match((TokenType.WHILE)):
            return self._while_statement()
        return self._expression_statement()

    def _while_statement(self):
        self.consume(TokenType.LEFT_PAREN, "Expected '(' after while keyword")
        condition: Expr = self._expression()
        self.consume(TokenType.RIGHT_PAREN, "Expected ')' after while condition")
        body: Stmt = self._statement()

        return While(condition, body)

    def _if_statement(self):
        self.consume(TokenType.LEFT_PAREN, "Expected '(' after keyword 'if'")
        condition: Expr = self._expression()
        self.consume(TokenType.RIGHT_PAREN, "Expected ')' after if condition")

        then_branch: Expr = self._statement()
        else_branch = None
        if self.match(TokenType.ELSE):
            else_branch = self._statement()

        return If(condition, then_branch, else_branch)

    def _block(self) -> List[Stmt]:
        statements: List[Stmt] = []

        while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
            statements.append(self._declaration())
        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block")
        return statements

    def _print_statement(self) -> Stmt:
        value = self._expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value")
        return Print(value)

    def _expression_statement(self) -> Stmt:
        expr = self._expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value")
        return Expression(expr)

    def _expression(self):
        return self._assignment()

    def _assignment(self):
        expr = self._or()

        if self.match(TokenType.EQUAL):
            equals = self.previous()
            value = self._assignment()

            if isinstance(expr, Variable):
                name = expr.name
                return Assign(name, value)
            self._error(equals, "Invalid assignment target")
        return expr

    def _or(self) -> Expr:
        expr: Expr = self._and()

        while self.match(TokenType.OR):
            op: Token = self.previous()
            right: Expr = self._and()
            expr = Logical(expr, op, right)

        return expr

    def _and(self) -> Expr:
        expr: Expr = self._equality()

        while self.match(TokenType.AND):
            op: Token = self.previous()
            right: Expr = self._equality()
            expr = Logical(expr, op, right)

        return expr

    def _equality(self):
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
            TokenType.EQUAL_EQUAL,
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
        elif self.match(TokenType.IDENTIFIER):
            return Variable(self.previous())
        elif self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)
        elif self.match(TokenType.LEFT_PAREN):
            expr = self._equality()
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
