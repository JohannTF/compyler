import statement as Statement
import expression as Expression

class StmtLoop(Statement):
    """
    Clase que representa una expresión lógica con un operador entre dos expresiones.
    """
    
    def __init__(self, condition: 'Expression', body: 'Statement'):
        """
        Constructor para la expresión lógica.
        
        Args:
            operator (Token): El token del operador lógico.
            right (Expression): La expresión del lado derecho.
        """
        self.condition = condition
        self.body = body