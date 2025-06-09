from src.parser.expression.expression import Expression
from src.lexer.token import Token
from src.interpreter.visitor_expression import VisitorExpression

class ExprVariable(Expression):
    def __init__(self, name: Token):
        self.name = name
    
    def accept(self, visitor: VisitorExpression):
        return visitor.visit_variable_expression(self)

    def __str__(self):
        return f"ExprVariable ({self.name})"

        