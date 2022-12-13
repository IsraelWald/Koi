import sys

from .tokens import Token
from .token_type import TokenType
from .scanner import Scanner
from .parser import Parser
from .koi_runtime_error import KoiRuntimeError
from .interpreter import Interpreter
from .resolver import Resolver


class Koi:
    def __init__(self):
        self.had_error = False
        self.had_runtime_error = False
        self.interpreter: Interpreter = Interpreter()

    def run(self, source: str):
        scanner = Scanner(source, on_error=self.error)
        tokens = scanner.scan_tokens()

        parser = Parser(tokens, on_error=self.token_error)
        statements = parser.parse()
        if self.had_error:
            print("Had error")
            return

        resolver = Resolver(self.interpreter, on_error=self.token_error)
        resolver.resolve(statements)
        if self.had_error:
            print("Had error")
            return
        value = self.interpreter.interpret(statements)
        if value:
            print(value)

    def runtime_error(self, error: KoiRuntimeError):
        message = f"{error.message!r} in line [line{error.token.line}]"
        print(message, file=sys.stderr)
        self.had_runtime_error = True

    def token_error(self, token: Token, message: str):
        if token.tok_type == TokenType.EOF:
            self.report(token.line, " At end ", message)
        else:
            self.report(token.line, f" at {token.lexeme!r} ", message)

    def error(self, line: int, message: str):
        self.report(line, "", message)

    def report(self, line: int, where: str, message: str):
        message = f"[line {line}] Error {where} : {message}"
        print(message, file=sys.stderr)
        self.had_error = True

    @staticmethod
    def _load_file(file: str) -> str:
        with open(file) as f:
            contents = f.readlines()
            lines = "".join(contents)
            return lines

    def run_file(self, file: str):
        lines = self._load_file(file)
        self.run(lines)

        if self.had_error:
            sys.exit(65)
        elif self.had_runtime_error:
            sys.exit(70)

    def run_prompt(self):
        print("Koi v1.0")
        print("Press Ctrl+C or Ctrl+D to exit")

        while True:
            try:
                line = input("> ")
                if line and line[0] == chr(4):
                    raise EOFError
                self.run(line)
                self.had_error = False
            except (KeyboardInterrupt, EOFError):
                self.quit_gracefully()

    def quit_gracefully(self):
        print("So long and thanks for all the fish")
        sys.exit(0)

    @staticmethod
    def main():
        """Run Koi from the console. Accepts one argument as a file that
        will be executed, or no arguments that will run the repl."""
        if len(sys.argv) > 2:
            print(f"Usage: {sys.argv[0]} [script]")
            sys.exit(64)
        elif len(sys.argv) == 2:
            Koi().run_file(sys.argv[1])
        else:
            Koi().run_prompt()
