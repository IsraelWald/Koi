from .environment import Environment
from .koi_callable import KoiCallable
from .koi_return_exception import KoiReturnException
from .stmt import Function
from typing import List

class KoiFunction(KoiCallable):
    def __init__(self, declaration: Function) -> None:
        self.decl = declaration

    def call(self, interpreter, args: List):
        env = Environment(interpreter.globals)
        for idx, param in enumerate(self.decl.params):
            env.define(param.lexeme, args[idx])

        try:
            interpreter._exec_block(self.decl.body, env)
        except KoiReturnException as return_value:
            return return_value.value
        return None

    def arity(self) -> int:
        return len(self.decl.params)

    def __repr__(self) -> str:
        return f"<function {self.decl.name.lexeme}>"
