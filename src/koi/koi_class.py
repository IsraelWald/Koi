from .koi_callable import KoiCallable
from .koi_instance import KoiInstance
from .koi_function import KoiFunction

from typing import List, Dict, Any
from typing_extensions import Self


class KoiClass(KoiCallable):
    def __init__(self, name, superclass: Self, methods: Dict[str, Any]) -> None:
        self.name = name
        self.methods = methods
        self.superclass = superclass

    def find_method(self, name: str):
        try:
            return self.methods[name]
        except KeyError:
            return None

    def __repr__(self) -> str:
        return f"<class {self.name!r}>"

    def call(self, interpreter, args: List):
        instance = KoiInstance(self)
        initializer: KoiFunction = self.find_method("init")
        if initializer is not None:
            initializer.bind(instance).call(interpreter, args)
        return instance

    def arity(self) -> int:
        initializer: KoiFunction = self.find_method("init")
        if initializer:
            return initializer.arity()
        return 0
