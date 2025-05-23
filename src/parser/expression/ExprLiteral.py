from src.parser.expression.expression import Expression
from typing import Any

class ExprLiteral(Expression):
    def __init__(self, value: object):
        self.value = value