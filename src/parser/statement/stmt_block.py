from typing import List

from src.parser.statement.statement import Statement

class StmtBlock(Statement):
    def __init__(self, statements: List[Statement]):
        self.statements = statements
    def __str__(self):
        return f"StmtBlock ({self.statements})"
        