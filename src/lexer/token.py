class Token:
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
            return f"< {self.tipo}, $, , >"
        elif self.tipo in ["IDENTIFIER", "NUMBER", "STRING"]:
            return f"< {self.tipo}, {self.lexema}, {self.literal}, {self.linea} >"
        elif self.tipo in ["TRUE", "FALSE", "NULL"]:
            return f"< {self.tipo}, {self.lexema}, {self.literal}, {self.linea} >"
        else:
            return f"< {self.tipo}, , , {self.linea} >"