from src.parser.expression.expression import Expression
from src.lexer.token import Token
from src.interpreter.visitor_expression import VisitorExpression

class ExprAssign(Expression):
    def __init__(self, name: Token, value: Expression):
        self.name = name
        self.value = value
    
    def accept(self, visitor: VisitorExpression):
        return visitor.visit_assign_expression(self)

    def __str__(self):
        return f"ExprAssign ({self.name},{self.value})"


        
        