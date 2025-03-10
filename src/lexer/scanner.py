from token import Token
from token_type import TokenType
from error_handler import ErrorHandler
from keywords import Keywords
from src.utils import file_handler

class Scanner:
    """
    Analizador léxico que convierte código fuente en tokens.
    """
    def __init__(self, codigo_fuente):
        self.codigo_fuente = codigo_fuente
        self.tokens = []
        self.inicio = 0
        self.actual = 0
        self.linea = 1
        self.palabras_reservadas = Keywords.get_keywords()
        self.error_handler = ErrorHandler()

    def escanear_tokens(self):
        """
        Escanea todo el código fuente y genera todos los tokens.
        """
        while not self.fin_archivo():
            self.inicio = self.actual
            self.escanear_token()
        self.agregar_token(TokenType.EOF)
    
    
    def siguiente_token(self):
        """
        Obtiene el siguiente token del código fuente.
        """
        if self.fin_archivo():
            return None
        return self.tokens[self.actual]


    def escanear_token(self):
        """
        Escanea un único token y lo define según su tipo
        """
        c = self.avanzar()
        if c == "(":
            self.agregar_token(TokenType.IZQ_PAREN)
        elif c == ")":
            self.agregar_token(TokenType.DER_PAREN)
        elif c == "{":
            self.agregar_token(TokenType.IZQ_LLAVE)
        elif c == "}":
            self.agregar_token(TokenType.DER_LLAVE)
        elif c == ",":
            self.agregar_token(TokenType.COMA)
        elif c == ".":
            self.agregar_token(TokenType.PUNTO)
        elif c == "-":
            self.agregar_token(TokenType.MENOS)
        elif c == "+":
            self.agregar_token(TokenType.MAS)
        elif c == ";":
            self.agregar_token(TokenType.PUNTO_COMA)
        elif c == "*":
            self.agregar_token(TokenType.MULTIPLICACION)
        elif c == "!":
            tipo = TokenType.DIFERENTE if self.coincidir("=") else TokenType.NOT
            self.agregar_token(tipo)
        elif c == "=":
            tipo = TokenType.IGUAL if self.coincidir("=") else TokenType.ASIGNACION
            self.agregar_token(tipo)
        elif c == "<":
            tipo = TokenType.MENOR if self.coincidir("=") else TokenType.MENOR_IGUAL
            self.agregar_token(tipo)
        elif c == ">":
            tipo = TokenType.MAYOR if self.coincidir("=") else TokenType.MAYOR_IGUAL
            self.agregar_token(tipo)
        elif c == "/":
            if self.coincidir("/"):
                while self.caracter_actual() != "\n" and not self.fin_archivo():
                    self.avanzar()
            elif self.coincidir("*"):
                self.comentario_multilinea()
            else:
                self.agregar_token(TokenType.DIVISION)
        elif c in [" ", "\r", "\t"]:
            self.manejar_espacios(c)
        elif c == "\n":
            self.linea += 1
        elif c == "\"":
            self.cadena()
        elif c.isdigit():
            self.numero()
        elif c.isalpha() or c == "_":
            self.identificador()
        else:
            self.error_lexico(f"Carácter inesperado '{c}' en la línea {self.linea}")


    def avanzar(self):
        """
        Avanza al siguiente carácter y devuelve el actual.
        """
        while self.caracter_actual() in [" ", "\r", "\t"]:
            self.avanzar()
        if self.fin_archivo():
            return
        self.actual += 1
        return self.codigo_fuente[self.actual - 1]
        

    
    def caracter_actual(self):
        """
        Devuelve el carácter actual sin avanzar.
        """
        return self.codigo_fuente[self.actual]
        
    
    def fin_archivo(self):
        """
        Verifica si se ha llegado al final del archivo.
        """
        if self.actual >= len(self.codigo_fuente):
            return True
        return False
        
    
    def coincidir(self, esperado):
        """
        Verifica si el carácter actual coincide con el esperado (diagrama de estados)
        """
        if self.fin_archivo():
            return False
        if self.codigo_fuente[self.actual] != esperado:
            return False
        self.actual += 1
        return True
    
    def manejar_espacios(self, c):
        """
        Maneja los espacios en blanco y saltos de línea.
        """
        while c in [" ", "\r", "\t"]:
            self.avanzar()
        if c == "\n":
            self.linea += 1
        

    
    def identificador(self):
        """
        Maneja los identificadores y palabras reservadas.
        """
        
    
    def numero(self):
        """
        Maneja los números (enteros, flotantes y de doble precisión).
        """

    
    def cadena(self):
        """
        Maneja las cadenas delimitadas por comillas dobles.
        """


    def comentario_multilinea(self):
        """
        Maneja comentarios de múltiples líneas /* ... */
        """
        while not (self.caracter_actual() == "*" and self.mirar_siguiente() == "/"):
            if self.caracter_actual() == "\n":
                self.linea += 1
            self.avanzar()
        self.avanzar()
        self.avanzar()

    
    def mirar_siguiente(self):
        """
        Mira el siguiente carácter sin avanzar el puntero.
        """
        if self.actual + 1 >= len(self.codigo_fuente):
            return "\0"
        return self.codigo_fuente[self.actual + 1]
        

    
    def agregar_token(self, tipo, lexema=None, literal=None):
        """
        Agrega un token a la lista de tokens.
        """
        lexema = lexema if lexema is not None else self.codigo_fuente[self.inicio:self.actual]
        self.tokens.append(Token(tipo, lexema, literal, self.linea))
        return f"{tipo} {lexema} {literal} {self.linea}"

    
    def error_lexico(self, mensaje):
        """
        Maneja errores léxicos.
        """
        self.error_handler.error_lexico(mensaje, self.linea)
        self.tokens.clear()
        return f"Error léxico: {mensaje} en la línea {self.linea}"
        