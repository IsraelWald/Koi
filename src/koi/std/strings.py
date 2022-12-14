from ..koi_callable import KoiCallable
from ..koi_class import KoiClass
from ..koi_instance import KoiInstance
from ..koi_runtime_error import KoiRuntimeError
from typing import List
from ..tokens import Token
from .numerable import is_numerable


class StringInstance(KoiInstance):
    def __init__(self, elements: str) -> None:
        super().__init__(KoiClass("String", None, {}))
        self.elements = list(str(elements))
        self.value = elements

    def get(self, name: Token):
        value = self.value
        elements = self.elements
        if name.lexeme == "at":

            class At(KoiCallable):
                def arity(self) -> int:
                    return 1

                def call(self, interpreter, args: List):
                    arg = args[0]
                    if not is_numerable(arg):
                        raise KoiRuntimeError(
                            name, f'"at" only accepts  number index. Got {arg!r}'
                        )
                    index = int(arg)
                    if index > len(elements) - 1:
                        raise KoiRuntimeError(name, "'at' out of bounds error")
                    return elements[index]

                def __repr__(self) -> str:
                    return "<native string method 'at'>"

            return At()
        elif name.lexeme == "alter":

            class Alter(KoiCallable):
                def arity(self) -> int:
                    return 2

                def call(self, interpreter, args: List):
                    arg = args[0]
                    to = args[1]
                    if not is_numerable(arg):
                        raise KoiRuntimeError(
                            name, f"'alter' only accepts a number index. Got {arg!r}"
                        )
                    index = int(arg)
                    if index > len(elements) - 1:
                        raise KoiRuntimeError(name, f"'at' out of bounds error")
                    elements[index] = str(to)

                def __repr__(self) -> str:
                    return "<native string method 'alter'>"

            return Alter()
        elif name.lexeme == "len":

            class Length(KoiCallable):
                def arity(self) -> int:
                    return 0

                def call(self, interpreter, args: List):
                    return len(elements)

                def __repr__(self) -> str:
                    return "<native string method 'len'>"

            return Length()
        elif name.lexeme == "split":

            class Split(KoiCallable):
                def arity(self) -> int:
                    return 1

                def call(self, interpreter, args: List):
                    if args[0].value == "":
                        return "".join(elements).split()
                    return "".join(elements).split(args[0].value)

                def __repr__(self) -> str:
                    return "<native string method split>"

            return Split()
        else:
            raise KoiRuntimeError(name, f"Can't call {name.lexeme!r} on a string")

    def __repr__(self) -> str:
        return "".join(self.elements)


class StringDataType(KoiCallable):
    def arity(self) -> int:
        return 1

    def call(self, interpreter, args: List):
        return StringInstance(args[0])

    def __repr__(self) -> str:
        return "<native data type 'string'>"
