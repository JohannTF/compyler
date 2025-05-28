from src.parser.statement.statement import Statement
from src.parser.expression.expression import Expression

class StmtIf(Statement):
    """
    Clase que representa una expresión lógica con un operador entre dos expresiones.
    """
    
    def __init__(self, condition: Expression, thenBranch: Statement, elseBranch: Statement):
        """
        Constructor para la expresión lógica.
        
        Args:
            condition (Expression): La condición del bucle.
            thenBranch (Statement): El bloque de código que se ejecuta si la condición es verdadera.
            elseBranch (Statement): El bloque de código que se ejecuta si la condición es falsa.
        """
        self.condition = condition
        self.thenBranch = thenBranch
        self.elseBranch = elseBranch