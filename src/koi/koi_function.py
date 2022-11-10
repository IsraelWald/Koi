from .environment import Environment
from .koi_callable import KoiCallable
from .koi_return_exception import KoiReturnException
from .stmt import Function
from typing import List


class KoiFunction(KoiCallable):
    def __init__(self, declaration: Function, closure: Environment) -> None:
        self.decl = declaration
        self.closure = closure

    def call(self, interpreter, args: List):
        env = Environment(self.closure)
        for decl_token, arg in zip(self.decl.params, args):
            env.define(decl_token.lexeme, arg)
        try:
            interpreter._exec_block(self.decl.body, env)
        except KoiReturnException as return_value:
            return return_value.value
        return None

    def arity(self) -> int:
        return len(self.decl.params)

    def __repr__(self) -> str:
        return f"<function {self.decl.name.lexeme}>"
