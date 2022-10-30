from src import Scanner, Parser, AstPrinter

code = """
var a = 100
while (a) {
    print(f"{a} + 11")
}
"""

test_code = " 12+12"

lexer = Scanner(test_code, on_error=lambda *x: print(x))
tokens = lexer.scan_tokens()
parser = Parser(tokens, on_error=lambda *x: print(x))
expr = parser.parse()
printer = AstPrinter()
print(printer.print(expr))
