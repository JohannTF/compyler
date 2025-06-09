from src.parser.statement.statement import Statement
from src.parser.expression.expression import Expression
from src.interpreter.visitor_statement import VisitorStatement

class StmtLoop(Statement):
    
    def __init__(self, condition: Expression, body: Statement):
        self.condition = condition
        self.body = body
    
    def accept(self, visitor: VisitorStatement):
        return visitor.visit_loop_statement(self)

    def __str__(self):
        return f"StmtLoop ({self.condition},{self.body})"
        
   