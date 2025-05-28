from typing import List

from src.parser.statement.statement import Statement
from src.lexer.token import Token
from src.parser.statement.stmt_block import StmtBlock

class StmtFunction(Statement):
    def __init__(self, name: Token, params: List[Token], body: StmtBlock):
        self.name = name
        self.params = params
        self.body = body
    def __str__(self):
        return f"StmtFunction ({self.name},{self.params},{self.body})"
        
        