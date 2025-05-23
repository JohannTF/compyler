from src.parser.expression.expression import Expression
from src.lexer.token import Token

class ExprBinary(Expression):
    def __init__(self, left: Expression, operator: Token, right: Expression):
        self.left = left
        self.operator = operator
        self.right = right
    
