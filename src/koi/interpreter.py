from .std.clock import Clock
from .environment import Environment
from .koi_callable import KoiCallable
from .koi_function import KoiFunction
from .expr import (
    Assign,
    ExprVisitor,
    Get,
    Grouping,
    Literal,
    Expr,
    Call,
    Logical,
    Set,
    Super,
    This,
    Unary,
    Binary,
    Variable,
)
from .stmt import (
    Class,
    Expression,
    Function,
    If,
    Print,
    Return,
    StmtVisitor,
    Stmt,
    Block,
    Var,
    While,
)
from .token_type import TokenType
from .koi_runtime_error import KoiRuntimeError

from typing import List


class Interpreter(ExprVisitor, StmtVisitor):
    def __init__(self) -> None:
        self.globals = Environment()
        self.env = self.globals

        self.globals.define("clock", Clock())

    def interpret(self, statements: List[Stmt]):
        try:
            for stmt in statements:
                self._execute(stmt)
        except KoiRuntimeError as error:
            print(error)
            raise SystemExit

    def _execute(self, statement: Stmt):
        try:
            return statement.accept(self)
        except KoiRuntimeError as error:
            print(error)
        except Exception as e:
            print(e)
            # raise e
            raise SystemExit

    def _stringify(self, value):
        if value is None:
            return "nil"
        elif value is True:
            return "true"
        elif value is False:
            return "false"
        elif isinstance(value, (float, int)):
            return str(value)
        return str(value)

    def visit_literal_expr(self, expr: Literal):
        return expr.value

    def visit_grouping_expr(self, expr: Grouping):
        return self._evaluate(expr.expression)

    def visit_unary_expr(self, expr: Unary):
        right = self._evaluate(expr.right)

        if expr.operator.tok_type == TokenType.MINUS:
            self._check_number_operand(expr.operator, right)
            return -int(right)
        elif expr.operator.tok_type == TokenType.BANG:
            return not self._is_truthy(right)

        return None

    def visit_binary_expr(self, expr: Binary):
        left = self._evaluate(expr.left)
        right = self._evaluate(expr.right)

        match expr.operator.tok_type:
            case TokenType.MINUS:
                self._check_number_operands(expr.operator, left, right)
                return float(left) - float(right)
            case TokenType.MOD:
                return float(left) % float(right)
            case TokenType.PLUS:
                if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                    return float(left) + float(right)
                elif isinstance(left, str) and isinstance(right, str):
                    return str(left) + str(right)
                else:
                    raise KoiRuntimeError(
                        expr.operator, "Both operands must be either numbers or string"
                    )
            case TokenType.SLASH:
                if right == 0:
                    raise KoiRuntimeError(right, f"Cannot divide {left} by zero")
                self._check_number_operands(expr.operator, left, right)
                return float(left) / float(right)
            case TokenType.STAR:
                self._check_number_operands(expr.operator, left, right)
                return float(left) * float(right)
            case TokenType.GREATER:
                self._check_number_operands(expr.operator, left, right)
                return float(left) > float(right)
            case TokenType.GREATER_EQUAL:
                self._check_number_operands(expr.operator, left, right)
                return float(left) >= float(right)
            case TokenType.LESS:
                self._check_number_operands(expr.operator, left, right)
                return float(left) < float(right)
            case TokenType.LESS_EQUAL:
                self._check_number_operands(expr.operator, left, right)
                return float(left) <= float(right)
            case TokenType.BANG_EQUAL:
                return not self._is_equal(left, right)
            case TokenType.EQUAL_EQUAL:
                return self._is_equal(left, right)

        return None

    def visit_expression_stmt(self, stmt: Expression):
        self._stringify(self._evaluate(stmt.expression))
        return None

    def visit_print_stmt(self, stmt: Print):
        value = self._evaluate(stmt.expression)
        print(self._stringify(value))
        return None

    def _evaluate(self, expr: Expr):
        return expr.accept(self)

    def _is_truthy(self, obj) -> bool:
        if obj is None:
            return False
        elif isinstance(obj, bool):
            return bool(obj)
        return True

    def _is_equal(self, left, right) -> bool:
        if left is None and right is None:
            return True
        elif left is None:
            return False

        return left == right

    def _check_number_operand(self, operator, operand):
        if isinstance(operand, (int, float)):
            return
        raise KoiRuntimeError(operator, f"Operand {operand} must be a number")

    def _check_number_operands(self, operator, left, right):
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return
        raise KoiRuntimeError(operator, "Operands must be numbers")

    def visit_assign_expr(self, expr: Assign):
        value = self._evaluate(expr.value)
        self.env.assign(expr.name, value)
        return value

    def visit_block_stmt(self, stmt: Block):
        self._exec_block(stmt.statements, Environment(self.env))
        return None

    def _exec_block(self, statements: List[Stmt], env: Environment):
        previous: Environment = self.env
        try:
            self.env = env
            for stmt in statements:
                self._execute(stmt)
        finally:
            self.env = previous

    def visit_call_expr(self, expr: Call):
        fn = self._evaluate(expr.callee)
        args = [self._evaluate(arg) for arg in expr.arguments]
        if not isinstance(fn, KoiCallable):
            raise KoiRuntimeError(expr.paren, "Can only call functions and classes")
        # fn = KoiCallable(callee)
        if len(args) != fn.arity():
            raise KoiRuntimeError(
                expr.paren, f"Expected {fn.arity()} arguments but got {len(args)}"
            )
        return fn.call(self, args)

    def visit_var_stmt(self, stmt: Var):
        value = None
        if stmt.initializer is not None:
            value = self._evaluate(stmt.initializer)
        self.env.define(stmt.name.lexeme, value)
        return None

    def visit_class_stmt(self, stmt: Class):
        return super().visit_class_stmt(stmt)

    def visit_super_expr(self, expr: Super):
        return super().visit_super_expr(expr)

    def visit_this_expr(self, expr: This):
        return super().visit_this_expr(expr)

    def visit_variable_expr(self, expr: Variable):
        return self.env.get(expr.name)

    def visit_function_stmt(self, stmt: Function):
        fn = KoiFunction(stmt)
        self.env.define(stmt.name.lexeme, fn)
        return None

    def visit_get_expr(self, expr: Get):
        return super().visit_get_expr(expr)

    def visit_if_stmt(self, stmt: If):
        if self._is_truthy(self._evaluate(stmt.condition)):
            self._execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self._execute(stmt.else_branch)
        return None

    def visit_return_stmt(self, stmt: Return):
        return super().visit_return_stmt(stmt)

    def visit_set_expr(self, expr: Set):
        return super().visit_set_expr(expr)

    def visit_logical_expr(self, expr: Logical):
        left = self._evaluate(expr.left)
        if expr.operator.tok_type == TokenType.OR:
            if self._is_truthy(left):
                return left
        else:
            if not self._is_truthy(left):
                return left
        return self._evaluate(expr.right)

    def visit_while_stmt(self, stmt: While):
        while self._is_truthy(self._evaluate(stmt.condition)):
            self._execute(stmt.body)
        return None
