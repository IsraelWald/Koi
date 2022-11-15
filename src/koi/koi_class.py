from .koi_callable import KoiCallable
from .koi_instance import KoiInstance

from typing import List, Dict, Any


class KoiClass(KoiCallable):
    def __init__(self, name, methods: Dict[str, Any]) -> None:
        self.name = name
        self.methods = methods

    def find_method(self, name: str):
        try:
            return self.methods[name]
        except KeyError:
            return None

    def __repr__(self) -> str:
        return f"<class {self.name!r}>"

    def call(self, interpreter, args: List):
        instance = KoiInstance(self)
        return instance

    def arity(self) -> int:
        return 0
