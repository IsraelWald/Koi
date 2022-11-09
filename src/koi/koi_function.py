from .environment import Environment
from .koi_callable import KoiCallable
from .stmt import Function
from typing import List, TYPE_CHECKING

class KoiFunction(KoiCallable):
    def __init__(self, declaration: Function) -> None:
        self.decl = declaration

    def call(self, interpreter, args: List):
        env = Environment(interpreter.globals)
        for idx, param in enumerate(self.decl.params):
            env.define(param.lexeme, args[idx])

        interpreter._exec_block(self.decl.body, env)
        return None

    def arity(self) -> int:
        return len(self.decl.params)

    def __repr__(self) -> str:
        return f"<function {self.decl.name.lexeme}>"
