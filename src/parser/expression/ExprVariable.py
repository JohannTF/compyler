from src.parser.expression.expression import Expression
from src.lexer.token import Token

class ExprVariable(Expression):
    """
    Clase que representa una expresión lógica con un operador entre dos expresiones.
    """
    
    def __init__(self, name: Token):
        """
        Constructor para la expresión lógica.
        
        Args:
            name (Token): El token que representa el nombre de la variable.
        """
        self.name = name

    def __str__(self):
        return f"ExprVariable ({self.name})"

        