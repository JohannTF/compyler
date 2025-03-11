from tokenInfo import TokenInfo
from token_type import TokenType
from error_handler import ErrorHandler
from keywords import Keywords

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
            return TokenInfo(TokenType.EOF)
        self.inicio = self.actual    
        return self.tokens[self.actual]


    def escanear_token(self):
        """
        Escanea un único token y lo define según su tipo
        """
        c = self.avanzar()
        if c == "(":
            self.agregar_token(TokenType.LEFT_PAREN)
        elif c == ")":
            self.agregar_token(TokenType.RIGHT_PAREN)
        elif c == "{":
            self.agregar_token(TokenType.LEFT_BRACE)
        elif c == "}":
            self.agregar_token(TokenType.RIGHT_BRACE)
        elif c == ",":
            self.agregar_token(TokenType.COMMA)
        elif c == ".":
            self.agregar_token(TokenType.DOT)
        elif c == "-":
            self.agregar_token(TokenType.MINUS)
        elif c == "+":
            self.agregar_token(TokenType.PLUS)
        elif c == ";":
            self.agregar_token(TokenType.SEMICOLON)
        elif c == "*":
            self.agregar_token(TokenType.STAR)
        elif c == "!":
            tipo = TokenType.BANG if self.coincidir("=") else TokenType.BANG_EQUAL
            self.agregar_token(tipo)
        elif c == "=":
            tipo = TokenType.EQUAL if self.coincidir("=") else TokenType.EQUAL_EQUAL
            self.agregar_token(tipo)
        elif c == "<":
            tipo = TokenType.LESS if self.coincidir("=") else TokenType.LESS_EQUAL
            self.agregar_token(tipo)
        elif c == ">":
            tipo = TokenType.GREATER if self.coincidir("=") else TokenType.GREATER_EQUAL
            self.agregar_token(tipo)
        elif c == "/":
            if self.coincidir("/"):
                while self.caracter_actual() != "\n" and not self.fin_archivo():
                    self.avanzar()
            elif self.coincidir("*"):
                self.comentario_multilinea()
            else:
                self.agregar_token(TokenType.SLASH)
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


    # Por modificar (espacios)
    def avanzar(self):
        """
        Avanza al siguiente carácter y devuelve el actual.
        """
        while self.caracter_actual() in [" ", "\r", "\t"]:
            self.actual += 1
            self.avanzar()
        if self.fin_archivo():
            return
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
        return self.actual >= len(self.codigo_fuente)
        
    
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
        while self.actual < len(self.codigo_fuente) and (self.caracter_actual().isalnum() or self.caracter_actual() == "_"):
            self.avanzar()

        # Obtener el texto del identificador
        texto = self.codigo_fuente[self.inicio:self.actual]

        # Verificar si es una palabra reservada
        if texto in self.palabras_reservadas:
            tipo = self.palabras_reservadas[texto]
        else:
            tipo = TokenType.IDENTIFICADOR

        self.agregar_token(tipo)


    def numero(self):
        """
        Maneja los números (enteros, flotantes y de doble precisión).
        """
        # Procesar la parte entera
        while self.actual < len(self.codigo_fuente) and self.caracter_actual().isdigit():
            self.avanzar()

        # Verificar si hay un punto decimal seguido de dígitos
        if self.actual < len(self.codigo_fuente) and self.caracter_actual() == "." and self.mirar_siguiente().isdigit():
            # Consumir el punto
            self.avanzar()

            # Consumir los dígitos después del punto
            while self.actual < len(self.codigo_fuente) and self.caracter_actual().isdigit():
                self.avanzar()

            # Convertir a flotante
            valor = float(self.codigo_fuente[self.inicio:self.actual])
            self.agregar_token(TokenType.NUMERO, literal=valor)
        else:
            # Es un entero
            valor = int(self.codigo_fuente[self.inicio:self.actual])
            self.agregar_token(TokenType.NUMERO, literal=valor)


    def cadena(self):
        """
        Maneja las cadenas delimitadas por comillas dobles.
        """
        # Avanzar hasta encontrar la comilla de cierre o el final del archivo
        while self.actual < len(self.codigo_fuente) and self.caracter_actual() != "\"" and not self.fin_archivo():
            if self.caracter_actual() == "\n":
                self.linea += 1
            self.avanzar()

        # Si se llegó al final del archivo sin encontrar la comilla de cierre
        if self.fin_archivo() or self.caracter_actual() != "\"":
            self.error_lexico("Cadena sin terminar")
            return

        # Consumir la comilla de cierre
        self.avanzar()

        # Obtener el valor de la cadena (sin las comillas)
        valor = self.codigo_fuente[self.inicio + 1:self.actual - 1]
        self.agregar_token(TokenType.CADENA, literal=valor)


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
        self.tokens.append(TokenInfo(tipo, lexema, literal, self.linea))
        # return f"{tipo} {lexema} {literal} {self.linea}"

    
    def error_lexico(self, mensaje):
        """
        Maneja errores léxicos.
        """
        self.error_handler.error_lexico(mensaje, self.linea)
        self.tokens.clear()
        return f"Error léxico: {mensaje} en la línea {self.linea}"
