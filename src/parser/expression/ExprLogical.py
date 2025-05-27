from src.parser.expression.expression import Expression
from src.lexer.token import Token

class ExprLogical(Expression):
    """
    Clase que representa una expresión lógica con un operador entre dos expresiones.
    """
    
    def __init__(self, left: Expression, operator: Token, right: Expression):
        """
        Constructor para la expresión lógica.
        
        Args:
            left (Expression): La expresión del lado izquierdo.
            operator (Token): El token del operador lógico.
            right (Expression): La expresión del lado derecho.
        """
        self.left = left
        self.operator = operator
        self.right = right