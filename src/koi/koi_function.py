from .environment import Environment
from .koi_callable import KoiCallable
from .koi_return_exception import KoiReturnException
from .stmt import Function
from typing import List


class KoiFunction(KoiCallable):
    def __init__(self, declaration: Function, closure: Environment, is_initializer: bool) -> None:
        self.decl = declaration
        self.closure = closure
        self.is_initializer = is_initializer

    def call(self, interpreter, args: List):
        env = Environment(self.closure)
        for decl_token, arg in zip(self.decl.params, args):
            env.define(decl_token.lexeme, arg)
        try:
            interpreter._exec_block(self.decl.body, env)
        except KoiReturnException as return_value:
            return return_value.value
        if self.is_initializer:
            return self.closure.get_at(0, "this")
        return None

    def arity(self) -> int:
        return len(self.decl.params)

    def bind(self, instance):
        env = Environment(self.closure)
        env.define("this", instance)
        return KoiFunction(self.decl, env)

    def __repr__(self) -> str:
        return f"<function {self.decl.name.lexeme}>"
