from src.lexer.token import Token
from src.parser.expression.expression import Expression
from src.parser.statement.statement import Statement

class StmtVar(Statement):
    def __init__(self, name: Token, initializer: Expression):
        self.name = name
        self.initializer = initializer