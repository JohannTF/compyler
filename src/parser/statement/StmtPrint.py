from src.parser.statement.statement import Statement
from src.parser.expression.expression import Expression

class StmtPrint(Statement):
    """
    Clase que representa una expresión lógica con un operador entre dos expresiones.
    """
    
    def __init__(self, expression: Expression):
        """
        Constructor para la expresión lógica.
        
        Args:
            expression (Expression): La expresión que se va a imprimir.
        """
        self.expression = expression


    def __str__(self):
        return f"StmtPrint ({self.expression})"


