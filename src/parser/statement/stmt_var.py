from src.lexer.token import Token
from src.parser.expression.expression import Expression
from src.parser.statement.statement import Statement
from src.interpreter.visitor_statement import VisitorStatement

class StmtVar(Statement):    
    def __init__(self, name: Token, initializer: Expression):
        self.name = name
        self.initializer = initializer
    
    def accept(self, visitor: VisitorStatement):
        return visitor.visit_var_statement(self)

    def __str__(self):
        return f"StmtVar ({self.name},{self.initializer})"
        
 