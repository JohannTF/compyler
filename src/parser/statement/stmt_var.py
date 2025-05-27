from src.lexer.token import Token
from src.parser.expression.expression import Expression
from src.parser.statement.statement import Statement

class StmtVar(Statement):
    """Clase que representa una declaración de variable con un nombre y un inicializador."""
    
    def __init__(self, name: Token, initializer: Expression):
        """Constructor para la declaración de variable.

        Args:
            name (Token): El token que representa el nombre de la variable.
            initializer (Expression): La expresión que inicializa la variable.
        """
        self.name = name
        self.initializer = initializer