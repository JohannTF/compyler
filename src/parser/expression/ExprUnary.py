from src.parser.expression.expression import Expression
from src.lexer.token import Token
from src.interpreter.visitor_expression import VisitorExpression

class ExprUnary(Expression):
    def __init__(self, operator: Token, right: Expression):
        self.operator = operator
        self.right = right
    
    def accept(self, visitor: VisitorExpression):
        return visitor.visit_unary_expression(self)

    def __str__(self):
        return f"ExprUnary ({self.operator},{self.right})"