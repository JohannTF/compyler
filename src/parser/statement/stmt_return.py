from src.parser.expression.expression import Expression
from src.parser.statement.statement import Statement

class StmtReturn(Statement):
    def __init__(self, value: Expression):
        self.value = value

    def __str__(self):
        return f"StmtReturn ({self.value})"
 