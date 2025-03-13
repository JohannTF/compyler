# token_type.py
class TokenType:
    """
    Enumeración de los tipos de token soportados por el analizador léxico.
    """
    # Palabras Reservadas
    ELSE = "ELSE"
    FALSE = "FALSE"
    FOR = "FOR"
    FUN = "FUN"
    IF = "IF"
    NULL = "NULL"
    PRINT = "PRINT"
    RETURN = "RETURN"
    TRUE = "TRUE"
    VAR = "VAR"
    WHILE = "WHILE"
    
    
    """ OPERADORES """
    # Operadores Aritméticos
    MINUS = "MINUS"                # -
    PLUS = "PLUS"                  # +
    SLASH = "SLASH"                # /
    STAR = "STAR"                  # *

    # Operadores Relacionales
    BANG_EQUAL = "BANG_EQUAL"      # !=
    EQUAL_EQUAL = "EQUAL_EQUAL"    # ==
    GREATER = "GREATER"            # >
    GREATER_EQUAL = "GREATER_EQUAL"# >=
    LESS = "LESS"                  # <
    LESS_EQUAL = "LESS_EQUAL"      # <=

    # Operadores Lógicos
    AND = "AND"
    OR = "OR"

    # Operador de Asignación
    EQUAL = "EQUAL"                # =
    
    # Operador de negación
    BANG = "BANG"                  # !
    
    # Adicionales
    INCREMENT = "INCREMENT"        # ++
    DECREMENT = "DECREMENT"        # --
    
    # Literales
    IDENTIFIER = "IDENTIFIER"
    
    # Tipos de dato
    INT = "INT"
    FLOAT = "FLOAT"
    STRING = "STRING"
    BOOLEAN = "BOOLEAN"
    
    # Signos de puntuación
    LEFT_PAREN = "LEFT_PAREN"      # (
    RIGHT_PAREN = "RIGHT_PAREN"    # )
    LEFT_BRACE = "LEFT_BRACE"      # {
    RIGHT_BRACE = "RIGHT_BRACE"    # }
    COMMA = "COMMA"                # ,
    SEMICOLON = "SEMICOLON"        # ;

    # Token de fin de archivo
    EOF = "EOF"