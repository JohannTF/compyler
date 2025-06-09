from src.parser.expression.expression import Expression
from src.lexer.token import Token  
from src.interpreter.visitor_expression import VisitorExpression


class ExprArithmetic(Expression):
    def __init__(self, left: Expression, operator: Token, right: Expression):
        self.left = left   
        self.operator = operator  
        self.right = right   
        
    def accept(self, visitor: VisitorExpression):
        return visitor.visit_arithmetic_expression(self)

    def __str__(self):
        return f"ExprArithmetic ({self.left},{self.operator},{self.right})"
        