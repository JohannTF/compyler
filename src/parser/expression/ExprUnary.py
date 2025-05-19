import expression as Expression
import src.lexer.token as Token

class ExprUnary(Expression):
    """
    Clase que representa una expresión lógica con un operador entre dos expresiones.
    """
    
    def __init__(self, operator: 'Token', right: 'Expression'):
        """
        Constructor para la expresión lógica.
        
        Args:
            operator (Token): El token del operador lógico.
            right (Expression): La expresión del lado derecho.
        """
        self.operator = operator
        self.right = right