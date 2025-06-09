from typing import List
from src.parser.expression.expression import Expression
from src.lexer.token import Token
from src.interpreter.visitor_expression import VisitorExpression

class ExprCallFunction(Expression):
    def __init__(self, callee: Expression, arguments: List[Expression]):
        self.callee = callee
        self.arguments = arguments
        
    def accept(self, visitor: VisitorExpression):
        return visitor.visit_call_expression(self)

    def __str__(self):
        return f"ExprCallFunction ({self.callee},{self.arguments})"