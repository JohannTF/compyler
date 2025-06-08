from typing import List
from src.parser.expression.expression import Expression
from src.lexer.token import Token

class ExprCallFunction(Expression):
    def __init__(self, callee: Expression, arguments: List[Expression]):
        self.callee = callee
        self.arguments = arguments


    def __str__(self):
        return f"ExprCallFunction ({self.calle},{self.arguments})"