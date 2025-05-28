from src.parser.expression.expression import Expression
from src.lexer.token import Token  


class ExprArithmetic(Expression):
    def __init__(self, left: Expression, operator: Token, right: Expression):
        self.left = left   
        self.operator = operator  
        self.right = right   

    def __str__(self):
        return f"ExprArithmetic ({self.left},{self.operator},{self.right})"
        