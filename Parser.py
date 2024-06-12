import re

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f'Token({self.type}, {repr(self.value)})'

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None

    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def generate_tokens(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.advance()
            elif self.current_char.isdigit():
                yield self.generate_number()
            elif self.current_char.isalpha() or self.current_char == '_':
                yield self.generate_identifier()
            elif self.current_char == '+':
                yield Token('ADD', '+')
                self.advance()
            elif self.current_char == '-':
                yield Token('SUB', '-')
                self.advance()
            elif self.current_char == '*':
                yield Token('MUL', '*')
                self.advance()
            elif self.current_char == '/':
                yield Token('DIV', '/')
                self.advance()
            elif self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    yield Token('EQ', '==')
                else:
                    yield Token('ASSIGN', '=')
            elif self.current_char == '(':
                yield Token('LPAREN', '(')
                self.advance()
            elif self.current_char == ')':
                yield Token('RPAREN', ')')
                self.advance()
            elif self.current_char == '{':
                yield Token('LBRACE', '{')
                self.advance()
            elif self.current_char == '}':
                yield Token('RBRACE', '}')
                self.advance()
            elif self.current_char == ';':
                yield Token('SEMICOLON', ';')
                self.advance()
            else:
                raise Exception(f'Illegal character: {self.current_char}')

    def generate_number(self):
        num_str = ''
        while self.current_char is not None and self.current_char.isdigit():
            num_str += self.current_char
            self.advance()
        return Token('NUMBER', int(num_str))

    def generate_identifier(self):
        id_str = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            id_str += self.current_char
            self.advance()
        if id_str == 'var':
            return Token('VAR', id_str)
        else:
            return Token('ID', id_str)

class ASTNode:
    def __init__(self, type, children=None):
        self.type = type
        self.children = children if children is not None else []

    def __repr__(self):
        return f'ASTNode({self.type}, {self.children})'

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = next(self.tokens, None)

    def eat(self, token_type):
        if self.current_token is not None and self.current_token.type == token_type:
            self.current_token = next(self.tokens, None)
        else:
            raise SyntaxError(f'Expected {token_type}, got {self.current_token.type if self.current_token else None}')

    def parse(self):
        program_ast = self.program()
        if self.current_token is not None:
            raise SyntaxError(f'Unexpected token: {self.current_token.type}')
        return program_ast

    def program(self):
        declarations = []
        while self.current_token is not None:
            declarations.append(self.declaration())
        return ASTNode('PROGRAM', declarations)

    def declaration(self):
        if self.current_token.type == 'VAR':
            return self.variable_declaration()
        else:
            raise SyntaxError(f'Unexpected token: {self.current_token.type}')

    def variable_declaration(self):
        self.eat('VAR')
        identifier = self.current_token.value
        self.eat('ID')
        self.eat('ASSIGN')
        value = self.expression()
        self.eat('SEMICOLON')
        return ASTNode('VAR_DECL', [identifier, value])

    def expression(self):
        result = self.term()
        while self.current_token.type in ('ADD', 'SUB'):
            token = self.current_token
            if token.type == 'ADD':
                self.eat('ADD')
            elif token.type == 'SUB':
                self.eat('SUB')
            result = ASTNode(token.value, [result, self.term()])
        return result

    def term(self):
        result = self.factor()
        while self.current_token.type in ('MUL', 'DIV'):
            token = self.current_token
            if token.type == 'MUL':
                self.eat('MUL')
            elif token.type == 'DIV':
                self.eat('DIV')
            result = ASTNode(token.value, [result, self.factor()])
        return result

    def factor(self):
        token = self.current_token
        if token.type == 'NUMBER':
            self.eat('NUMBER')
            return ASTNode('NUMBER', [token.value])
        elif token.type == 'ID':
            identifier = token.value
            self.eat('ID')
            return ASTNode('ID', [identifier])
        elif token.type == 'LPAREN':
            self.eat('LPAREN')
            result = self.expression()
            self.eat('RPAREN')
            return result
        else:
            raise SyntaxError(f'Unexpected token: {token.type}')

def main():
    text = """
    var x = 10;
    var y = 5;
    var resultado = x + y;
    """
    print("Tokens:")
    lexer = Lexer(text)
    tokens = lexer.generate_tokens()
    for token in tokens:
        print(token)

    print("\nAbstract Syntax Tree:")
    lexer = Lexer(text)
    tokens = lexer.generate_tokens()
    parser = Parser(tokens)
    program_ast = parser.parse()
    print(program_ast)

    print("\nGrammar:")
    print("""
    programa       -> declaracao programa
                    | ε

    declaracao     -> declaracao_variavel

    declaracao_variavel -> 'var' identificador '=' expressao ';'

    expressao      -> termo ('+' termo | '-' termo)*

    termo          -> fator ('' fator | '/' fator)

    fator          -> numero
                    | identificador
                    | '(' expressao ')'

    identificador  -> ID

    numero         -> NUMBER
    """)

if __name__ == "__main__":
    main()
