from .koi_callable import KoiCallable
from .koi_instance import KoiInstance

from typing import List


class KoiClass(KoiCallable):
    def __init__(self, name) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f"<class {self.name!r}>"

    def call(self, interpreter, args: List):
        instance = KoiInstance(self)
        return instance

    def arity(self) -> int:
        return 0
