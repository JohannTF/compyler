from src.parser.statement.statement import Statement
from src.parser.expression.expression import Expression
from src.interpreter.visitor_statement import VisitorStatement

class StmtIf(Statement):
    
    def __init__(self, condition: Expression, thenBranch: Statement, elseBranch: Statement):
        self.condition = condition
        self.thenBranch = thenBranch
        self.elseBranch = elseBranch
    
    def accept(self, visitor: VisitorStatement):
        return visitor.visit_if_statement(self)

    def __str__(self):
        return f"StmtIf ({self.condition},{self.thenBranch},{self.elseBranch})"

      