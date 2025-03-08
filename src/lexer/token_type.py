# token_type.py
class TokenType:
    """
    Enumeración de los tipos de token soportados por el analizador léxico.
    """
    # Tokens de un solo carácter
    LEFT_PAREN = "LEFT_PAREN"      # (
    RIGHT_PAREN = "RIGHT_PAREN"    # )
    LEFT_BRACE = "LEFT_BRACE"      # {
    RIGHT_BRACE = "RIGHT_BRACE"    # }
    COMMA = "COMMA"                # ,
    DOT = "DOT"                    # .
    MINUS = "MINUS"                # -
    PLUS = "PLUS"                  # +
    SEMICOLON = "SEMICOLON"        # ;
    SLASH = "SLASH"                # /
    STAR = "STAR"                  # *
    
    # Tokens de uno o dos caracteres
    BANG = "BANG"                  # !
    BANG_EQUAL = "BANG_EQUAL"      # !=
    EQUAL = "EQUAL"                # =
    EQUAL_EQUAL = "EQUAL_EQUAL"    # ==
    GREATER = "GREATER"            # >
    GREATER_EQUAL = "GREATER_EQUAL"# >=
    LESS = "LESS"                  # <
    LESS_EQUAL = "LESS_EQUAL"      # <=
    
    # Funcionalidades adicionales
    INCREMENT = "INCREMENT"        # ++
    DECREMENT = "DECREMENT"        # --
    QUESTION = "QUESTION"          # ?
    COLON = "COLON"                # :
    
    # Literales
    IDENTIFIER = "IDENTIFIER"
    STRING = "STRING"
    NUMBER = "NUMBER"
    
    # Palabras clave
    AND = "AND"
    CLASS = "CLASS"
    ELSE = "ELSE"
    FALSE = "FALSE"
    FUN = "FUN"
    FOR = "FOR"
    IF = "IF"
    NULL = "NULL"
    OR = "OR"
    PRINT = "PRINT"
    RETURN = "RETURN"
    SUPER = "SUPER"
    THIS = "THIS"
    TRUE = "TRUE"
    VAR = "VAR"
    WHILE = "WHILE"
    
    # Funcionalidades adicionales: tipado estático
    INT = "INT"
    FLOAT = "FLOAT"
    STRING = "STRING"
    BOOLEAN = "BOOLEAN"
    
    # Funcionalidad adicional: entrada del teclado
    INPUT = "INPUT"
    
    # Token de fin de archivo
    EOF = "EOF"