from src.parser.expression.expression import Expression
from src.parser.statement.statement import Statement

class StmtExpression(Statement):
    def __init__(self, expression: Expression):
        self.expression = expression

    def __str__(self):
        return f"StmtExpression ({self.expression})"



 