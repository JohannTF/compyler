from src.parser.expression.expression import Expression
from src.lexer.token import Token

class ExprAssign(Expression):
    def __init__(self, name: Token, value: Expression):
        self.name = name
        self.value = value

    def __str__(self):
        return f"ExprAssign ({self.name},{self.value})"


        
        