from src.parser.expression.expression import Expression
from src.lexer.token import Token

class ExprVariable(Expression):
    """
    Clase que representa una expresión lógica con un operador entre dos expresiones.
    """
    
    def __init__(self, name: 'Token'):
        """
        Constructor para la expresión lógica.
        
        Args:
            operator (Token): El token del operador lógico.
            right (Expression): La expresión del lado derecho.
        """
        self.name = name