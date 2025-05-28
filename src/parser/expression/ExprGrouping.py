from src.parser.expression.expression import Expression

class ExprGrouping(Expression):
    def __init__(self, expression: Expression):
        self.expression = expression


    def __str__(self):
        return f"ExprGrouping ({self.expression})"