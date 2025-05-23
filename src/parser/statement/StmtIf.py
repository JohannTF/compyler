from src.parser.statement.statement import Statement
from src.parser.expression.expression import Expression

class StmtLoop(Statement):
    """
    Clase que representa una expresión lógica con un operador entre dos expresiones.
    """
    
    def __init__(self, condition: 'Expression', thenBranch: 'Statement', elseBranch: 'Statement'):
        """
        Constructor para la expresión lógica.
        
        Args:
            operator (Token): El token del operador lógico.
            right (Expression): La expresión del lado derecho.
        """
        self.condition = condition
        self.thenBranch = thenBranch
        self.elseBranch = elseBranch
        