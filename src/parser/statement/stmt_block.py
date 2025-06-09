from typing import List

from src.parser.statement.statement import Statement
from src.interpreter.visitor_statement import VisitorStatement

class StmtBlock(Statement):
    def __init__(self, statements: List[Statement]):
        self.statements = statements
    
    def accept(self, visitor: VisitorStatement):
        return visitor.visit_block_statement(self)
    
    def __str__(self):
        return f"StmtBlock ({self.statements})"
        