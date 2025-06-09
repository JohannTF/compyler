from src.parser.expression.expression import Expression
from src.lexer.token import Token
from src.interpreter.visitor_expression import VisitorExpression

class ExprBinary(Expression):
    def __init__(self, left: Expression, operator: Token, right: Expression):
        self.left = left
        self.operator = operator
        self.right = right
    
    def accept(self, visitor: VisitorExpression):
        return visitor.visit_binary_expression(self)

    def __str__(self):
        return f"ExprBinary ({self.left},{self.operator},{self.right})"
        