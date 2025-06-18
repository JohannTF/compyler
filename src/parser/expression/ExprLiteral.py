from src.parser.expression.expression import Expression
from src.interpreter.visitor_expression import VisitorExpression

class ExprLiteral(Expression):
    def __init__(self, value: object):
        self.value = value
        
    def accept(self, visitor: VisitorExpression):
        return visitor.visit_literal_expression(self)

    def __str__(self):
        return f"ExprLiteral ({self.value})"
    