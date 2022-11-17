from ..koi_callable import KoiCallable
from typing import List
from pathlib import Path

base_path = Path.cwd()


class ReadFile(KoiCallable):
    def arity(self) -> int:
        return 1

    def call(self, interpreter, args: List):
        file_path = base_path / Path(args[0])
        return file_path.read_text()

    def __repr__(self) -> str:
        return "<native function read_file(filename)>"


class WriteFile(KoiCallable):
    def arity(self) -> int:
        return 2

    def call(self, interpreter, args: List):
        file_path = base_path / Path(args[0])
        content = args[1]
        file_path.write_text(content)

    def __repr__(self) -> str:
        return f"<native function write_file(filepath, content)>"
