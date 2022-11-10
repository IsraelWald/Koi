from .expr import ExprVisitor
from .stmt import Block, Stmt, StmtVisitor


class Resolver(ExprVisitor, StmtVisitor):
    def __init__(self, interpreter) -> None:
        self.interpreter = interpreter

    def visit_block_stmt(self, stmt: Block):
        self._begin_scope()
        self.resolve(stmt.statements)
        self._end_scope()
        return None

    def resolve(self, stmts):
        for stmt in stmts:
            self._resolve_stmt(stmt)

    def _resolve_stmt(self, stmt: Stmt):
        stmt.accept(self)


# https://craftinginterpreters.com/resolving-and-binding.html
