from src.parser.expression.expression import Expression
from src.parser.statement.statement import Statement
from src.interpreter.visitor_statement import VisitorStatement

class StmtReturn(Statement):
    def __init__(self, value: Expression):
        self.value = value
    
    def accept(self, visitor: VisitorStatement):
        return visitor.visit_return_statement(self)

    def __str__(self):
        return f"StmtReturn ({self.value})"
 