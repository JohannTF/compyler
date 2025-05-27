from src.parser.statement.statement import Statement
from src.parser.expression.expression import Expression

class StmtLoop(Statement):
    """
    Clase que representa una expresión lógica con un operador entre dos expresiones.
    """
    
    def __init__(self, condition: Expression, body: Statement):
        """
        Constructor para la expresión lógica.
        
        Args:
            condition (Expression): La condición del bucle.
            body (Statement): El bloque de código que se ejecuta mientras la condición sea verdadera.
        """
        self.condition = condition
        self.body = body