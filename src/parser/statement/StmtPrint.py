from src.parser.statement.statement import Statement
from src.parser.expression.expression import Expression
from src.interpreter.visitor_statement import VisitorStatement

class StmtPrint(Statement):
    def __init__(self, expression: Expression):
        self.expression = expression
        
    def accept(self, visitor: VisitorStatement):
        return visitor.visit_print_statement(self)

    def __str__(self):
        return f"StmtPrint ({self.expression})"


