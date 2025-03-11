class TokenInfo:
    """
    Clase que representa un token identificado por el analizador léxico.
    """
    def __init__(self, tipo, lexema=None, literal=None, linea=None):
        self.tipo = tipo
        self.lexema = lexema
        self.literal = literal
        self.linea = linea
    
    def __str__(self):
        if self.tipo == "EOF":
            return f"< {self.tipo}, lexema: $, , >"
        elif self.tipo == "IDENTIFIER":
            return f"< {self.tipo}, lexema: {self.lexema}, linea: {self.linea} >"
        elif self.tipo in ["NUMBER", "STRING", "TRUE", "FALSE", "NULL"]:
            return f"< {self.tipo}, lexema: {self.lexema}, literal: {self.literal}, linea: {self.linea} >"
        else:
            return f"< {self.tipo}, linea: {self.linea} >"