class KoiInstance:
    def __init__(self, klass) -> None:
        self.klass = klass

    def __repr__(self) -> str:
        return f"<instance of class {self.klass.name!r}>"
