from src.parser.expression.expression import Expression
from src.interpreter.visitor_expression import VisitorExpression

class ExprGrouping(Expression):
    def __init__(self, expression: Expression):
        self.expression = expression

    def accept(self, visitor: VisitorExpression):
        return visitor.visit_grouping_expression(self)

    def __str__(self):
        return f"ExprGrouping ({self.expression})"