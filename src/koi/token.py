class Token:
    def __init__(self, token_type, lexeme, literal, line):
        self.tok_type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __repr__(self):
        return f"({self.tok_type}, {self.lexeme!r}{f', {self.literal}' if self.literal else ''})"
