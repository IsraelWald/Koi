from src import Scanner

code = """
var a = 100
while (a) {
    print(f"{a} + 11")
}
"""

lexer = Scanner(code, on_error=lambda *x: print(x))
tokens = lexer.scan_tokens()
print(tokens)
