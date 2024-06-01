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
            elif self.current_char == '"':
                yield self.generate_string()
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
            elif self.current_char == '%':
                yield Token('MOD', '%')
                self.advance()
            elif self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    yield Token('EQ', '==')
                else:
                    yield Token('ASSIGN', '=')
            elif self.current_char == '!':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    yield Token('NEQ', '!=')
                else:
                    yield Token('NOT', '!')
            elif self.current_char == '<':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    yield Token('LTE', '<=')
                else:
                    yield Token('LT', '<')
            elif self.current_char == '>':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    yield Token('GTE', '>=')
                else:
                    yield Token('GT', '>')
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
            elif self.current_char == ',':
                yield Token('COMMA', ',')
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
        elif id_str == 'function':
            return Token('FUNCTION', id_str)
        elif id_str == 'return':
            return Token('RETURN', id_str)
        elif id_str == 'if':
            return Token('IF', id_str)
        elif id_str == 'else':
            return Token('ELSE', id_str)
        elif id_str == 'while':
            return Token('WHILE', id_str)
        elif id_str == 'for':
            return Token('FOR', id_str)
        elif id_str == 'break':
            return Token('BREAK', id_str)
        elif id_str == 'continue':
            return Token('CONTINUE', id_str)
        elif id_str == 'class':
            return Token('CLASS', id_str)
        elif id_str == 'and':
            return Token('AND', '&&')
        elif id_str == 'or':
            return Token('OR', '||')
        else:
            return Token('ID', id_str)

    def generate_string(self):
        string = ''
        self.advance()  # Skip the opening quote
        while self.current_char is not None and self.current_char != '"':
            string += self.current_char
            self.advance()
        self.advance()  # Skip the closing quote
        return Token('STRING', string)

class ASTNode:
    pass

class ProgramNode(ASTNode):
    def __init__(self, declarations):
        self.declarations = declarations

class VariableDeclarationNode(ASTNode):
    def __init__(self, identifier, value=None):
        self.identifier = identifier
        self.value = value

class FunctionDeclarationNode(ASTNode):
    def __init__(self, identifier, parameters, body):
        self.identifier = identifier
        self.parameters = parameters
        self.body = body

class ReturnStatementNode(ASTNode):
    def __init__(self, expression):
        self.expression = expression

class BinaryOpNode(ASTNode):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class UnaryOpNode(ASTNode):
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand

class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value

class StringNode(ASTNode):
    def __init__(self, value):
        self.value = value

class IdentifierNode(ASTNode):
    def __init__(self, name):
        self.name = name

class IfStatementNode(ASTNode):
    def __init__(self, condition, if_body, else_body=None):
        self.condition = condition
        self.if_body = if_body
        self.else_body = else_body

class WhileStatementNode(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class ForStatementNode(ASTNode):
    def __init__(self, init, condition, update, body):
        self.init = init
        self.condition = condition
        self.update = update
        self.body = body

class BreakStatementNode(ASTNode):
    pass

class ContinueStatementNode(ASTNode):
    pass

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = None

    def parse(self):
        self.advance()
        return self.program()

    def advance(self):
        self.current_token = next(self.lexer, None)

    def eat(self, token_type):
        if self.current_token is not None and self.current_token.type == token_type:
            self.advance()
        else:
            raise SyntaxError(f'Expected {token_type} but got {self.current_token.type}')

    def program(self):
        declarations = []
        while self.current_token is not None:
            declarations.append(self.declaration())
        return ProgramNode(declarations)

    def declaration(self):
        token = self.current_token
        if token.type == 'VAR':
            return self.variable_declaration()
        elif token.type == 'FUNCTION':
            return self.function_declaration()
        elif token.type == 'CLASS':
            return self.class_declaration()
        elif token.type == 'IF':
            return self.if_statement()
        elif token.type == 'WHILE':
            return self.while_statement()
        elif token.type == 'FOR':
            return self.for_statement()
        elif token.type == 'BREAK':
            return self.break_statement()
        elif token.type == 'CONTINUE':
            return self.continue_statement()
        else:
            return self.expression()

    def variable_declaration(self):
        self.eat('VAR')
        identifier = self.current_token.value
        self.eat('ID')
        if self.current_token.type == 'ASSIGN':
            self.eat('ASSIGN')
            value = self.expression()
        else:
            value = None
        self.eat('SEMICOLON')
        return VariableDeclarationNode(identifier, value)

    def function_declaration(self):
        self.eat('FUNCTION')
        identifier = self.current_token.value
        self.eat('ID')
        self.eat('LPAREN')
        parameters = self.parameters()
        self.eat('RPAREN')
        self.eat('LBRACE')
        body = []
        while self.current_token.type != 'RBRACE':
            body.append(self.declaration())
        self.eat('RBRACE')
        return FunctionDeclarationNode(identifier, parameters, body)

    def parameters(self):
        parameters = []
        if self.current_token.type != 'RPAREN':
            parameters.append(self.current_token.value)
            self.eat('ID')
            while self.current_token.type == 'COMMA':
                self.eat('COMMA')
                parameters.append(self.current_token.value)
                self.eat('ID')
        return parameters

    def expression(self):
        return self.expression_logical()

    def expression_logical(self):
        node = self.expression_relational()
        while self.current_token.type in {'AND', 'OR'}:
            op = self.current_token.type
            self.advance()
            right = self.expression_relational()
            node = BinaryOpNode(op, node, right)
        return node

    def expression_relational(self):
        node = self.expression_additive()
        while self.current_token.type in {'LT', 'LTE', 'GT', 'GTE', 'EQ', 'NEQ'}:
            op = self.current_token.type
            self.advance()
            right = self.expression_additive()
            node = BinaryOpNode(op, node, right)
        return node

    def expression_additive(self):
        node = self.expression_multiplicative()
        while self.current_token.type in {'ADD', 'SUB'}:
            op = self.current_token.type
            self.advance()
            right = self.expression_multiplicative()
            node = BinaryOpNode(op, node, right)
        return node

    def expression_multiplicative(self):
        node = self.expression_unary()
        while self.current_token.type in {'MUL', 'DIV', 'MOD'}:
            op = self.current_token.type
            self.advance()
            right = self.expression_unary()
            node = BinaryOpNode(op, node, right)
        return node

    def expression_unary(self):
        if self.current_token.type in {'ADD', 'SUB', 'NOT'}:
            op = self.current_token.type
            self.advance()
            operand = self.expression_unary()
            return UnaryOpNode(op, operand)
        return self.primary()

    def primary(self):
        token = self.current_token
        if token.type == 'NUMBER':
            self.eat('NUMBER')
            return NumberNode(token.value)
        elif token.type == 'STRING':
            self.eat('STRING')
            return StringNode(token.value)
        elif token.type == 'ID':
            self.eat('ID')
            return IdentifierNode(token.value)
        elif token.type == 'LPAREN':
            self.eat('LPAREN')
            expr = self.expression()
            self.eat('RPAREN')
            return expr
        else:
            raise SyntaxError(f'Unexpected token: {token.type}')

    def if_statement(self):
        self.eat('IF')
        self.eat('LPAREN')
        condition = self.expression()
        self.eat('RPAREN')
        self.eat('LBRACE')
        if_body = []
        while self.current_token.type != 'RBRACE':
            if_body.append(self.declaration())
        self.eat('RBRACE')
        else_body = []
        if self.current_token.type == 'ELSE':
            self.eat('ELSE')
            self.eat('LBRACE')
            while self.current_token.type != 'RBRACE':
                else_body.append(self.declaration())
            self.eat('RBRACE')
        return IfStatementNode(condition, if_body, else_body)

    def while_statement(self):
        self.eat('WHILE')
        self.eat('LPAREN')
        condition = self.expression()
        self.eat('RPAREN')
        self.eat('LBRACE')
        body = []
        while self.current_token.type != 'RBRACE':
            body.append(self.declaration())
        self.eat('RBRACE')
        return WhileStatementNode(condition, body)

    def for_statement(self):
        self.eat('FOR')
        self.eat('LPAREN')
        init = self.declaration() if self.current_token.type == 'VAR' else None
        condition = self.expression()
        self.eat('SEMICOLON')
        update = self.expression() if self.current_token.type != 'RPAREN' else None
        self.eat('RPAREN')
        self.eat('LBRACE')
        body = []
        while self.current_token.type != 'RBRACE':
            body.append(self.declaration())
        self.eat('RBRACE')
        return ForStatementNode(init, condition, update, body)

    def break_statement(self):
        self.eat('BREAK')
        self.eat('SEMICOLON')
        return BreakStatementNode()

    def continue_statement(self):
        self.eat('CONTINUE')
        self.eat('SEMICOLON')
        return ContinueStatementNode()

def main():
    text = """
    var x = 5;
    var y = 10;
    function add(a, b) {
        return a + b;
    }
    if (x < y) {
        var z = add(x, y);
    }
    """

    lexer = Lexer(text)
    tokens = lexer.generate_tokens()
    parser = Parser(iter(tokens))
    ast = parser.parse()

    # Imprime a AST para verificação
    print_ast(ast)

def print_ast(node, level=0):
    indent = "  " * level
    if isinstance(node, ProgramNode):
        print(f"{indent}Program")
        for declaration in node.declarations:
            print_ast(declaration, level + 1)
    elif isinstance(node, VariableDeclarationNode):
        print(f"{indent}VariableDeclaration(identifier={node.identifier}, value={node.value})")
        if node.value:
            print_ast(node.value, level + 1)
    elif isinstance(node, FunctionDeclarationNode):
        print(f"{indent}FunctionDeclaration(identifier={node.identifier}, parameters={node.parameters})")
        for statement in node.body:
            print_ast(statement, level + 1)
    elif isinstance(node, ReturnStatementNode):
        print(f"{indent}ReturnStatement")
        print_ast(node.expression, level + 1)
    elif isinstance(node, BinaryOpNode):
        print(f"{indent}BinaryOp(op={node.op})")
        print_ast(node.left, level + 1)
        print_ast(node.right, level + 1)
    elif isinstance(node, UnaryOpNode):
        print(f"{indent}UnaryOp(op={node.op})")
        print_ast(node.operand, level + 1)
    elif isinstance(node, NumberNode):
        print(f"{indent}Number(value={node.value})")
    elif isinstance(node, StringNode):
        print(f"{indent}String(value={node.value})")
    elif isinstance(node, IdentifierNode):
        print(f"{indent}Identifier(name={node.name})")
    elif isinstance(node, IfStatementNode):
        print(f"{indent}IfStatement")
        print_ast(node.condition, level + 1)
        for statement in node.if_body:
            print_ast(statement, level + 1)
        if node.else_body:
            for statement in node.else_body:
                print_ast(statement, level + 1)
    elif isinstance(node, WhileStatementNode):
        print(f"{indent}WhileStatement")
        print_ast(node.condition, level + 1)
        for statement in node.body:
            print_ast(statement, level + 1)
    elif isinstance(node, ForStatementNode):
        print(f"{indent}ForStatement")
        if node.init:
            print(f"{indent}  Init")
            print_ast(node.init, level + 1)
        print(f"{indent}  Condition")
        print_ast(node.condition, level + 1)
        if node.update:
            print(f"{indent}  Update")
            print_ast(node.update, level + 1)
        for statement in node.body:
            print_ast(statement, level + 1)
    elif isinstance(node, BreakStatementNode):
        print(f"{indent}BreakStatement")
    elif isinstance(node, ContinueStatementNode):
        print(f"{indent}ContinueStatement")

if __name__ == "__main__":
    main()