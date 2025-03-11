from .tokenInfo import TokenInfo
from .token_type import TokenType
from .error_handler import ErrorHandler
from .keywords import Keywords
#from src.utils import file_handler

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
        
        self.tokens.append(TokenInfo(TokenType.EOF, "", None, self.linea))
        return self.tokens
    
    
    def siguiente_token(self):
        """
        Obtiene el siguiente token del código fuente.
        """
        if self.actual >= len(self.codigo_fuente):
            return TokenInfo(TokenType.EOF, "", None, self.linea)
        self.inicio = self.actual
        return self.escanear_token()


    def escanear_token(self):
        """
        Escanea un único token y lo define según su tipo
        """
        c = self.avanzar()
        
        if c.isspace():
            self.manejar_espacios(c)
            return None
        if c.isalpha() or c == "_":
            return self.identificador()
        if c.isdigit():
            return self.numero()
        if c == "":
            return self.cadena()
        if c == '/':
            if self.coincidir('/'):
                # Comentario de una línea
                while self.caracter_actual() != '\n' and not self.fin_archivo():
                    self.avanzar()
                return None
            elif self.coincidir('*'):
                # Comentario de múltiples líneas
                return self.comentario_multilinea()
            else:
                return self.agregar_token(TokenType.SLASH)

        # Operadores de un carácter
        if c == '(': return self.agregar_token(TokenType.LEFT_PAREN)
        if c == ')': return self.agregar_token(TokenType.RIGHT_PAREN)
        if c == '{': return self.agregar_token(TokenType.LEFT_BRACE)
        if c == '}': return self.agregar_token(TokenType.RIGHT_BRACE)
        if c == ',': return self.agregar_token(TokenType.COMMA)
        if c == '.': return self.agregar_token(TokenType.DOT)
        if c == '-': 
            if self.coincidir('-'):
                return self.agregar_token(TokenType.DECREMENT)  # Funcionalidad nueva: operador --
            return self.agregar_token(TokenType.MINUS)
        if c == '+': 
            if self.coincidir('+'):
                return self.agregar_token(TokenType.INCREMENT)  # Funcionalidad nueva: operador ++
            return self.agregar_token(TokenType.PLUS)
        if c == ';': return self.agregar_token(TokenType.SEMICOLON)
        if c == '*': return self.agregar_token(TokenType.STAR)

        # Operadores de dos caracteres
        if c == '!':
            return self.agregar_token(TokenType.BANG_EQUAL if self.coincidir('=') else TokenType.BANG)
        if c == '=':
            return self.agregar_token(TokenType.EQUAL_EQUAL if self.coincidir('=') else TokenType.EQUAL)
        if c == '<':
            return self.agregar_token(TokenType.LESS_EQUAL if self.coincidir('=') else TokenType.LESS)
        if c == '>':
            return self.agregar_token(TokenType.GREATER_EQUAL if self.coincidir('=') else TokenType.GREATER)

        # Operador ternario
        if c == '?': return self.agregar_token(TokenType.QUESTION)
        if c == ':': return self.agregar_token(TokenType.COLON)
        
        # Error léxico: carácter no reconocido
        self.error_lexico(f"Carácter no reconocido: '{c}'")
        return None

    def avanzar(self):
        """
        Avanza al siguiente carácter y devuelve el actual.
        """
        if self.fin_archivo():
            return '\0'
        c = self.codigo_fuente[self.actual]
        self.actual += 1
        return c

    
    def caracter_actual(self):
        """
        Devuelve el carácter actual sin avanzar.
        """
        if self.fin_archivo():
            return '\0'
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
        if c == '\n':
            self.linea += 1

    
    def identificador(self):
        """
        Maneja los identificadores y palabras reservadas.
        """
        while self.caracter_actual().isalnum() or self.caracter_actual() == '_':
            self.avanzar()
        
        # Extraer el texto del identificador
        lexema = self.codigo_fuente[self.inicio:self.actual]
        
        # Verificar si es una palabra reservada
        tipo = self.palabras_reservadas.get(lexema, TokenType.IDENTIFIER)
        
        if tipo == TokenType.IDENTIFIER:
            return self.agregar_token(tipo, lexema, lexema)
        elif tipo == TokenType.TRUE:
            return self.agregar_token(tipo, lexema, True)
        elif tipo == TokenType.FALSE:
            return self.agregar_token(tipo, lexema, False)
        elif tipo == TokenType.NULL:
            return self.agregar_token(tipo, lexema, None)
        else:
            return self.agregar_token(tipo)

    
    def numero(self):
        """
        Maneja los números (enteros, flotantes y de doble precisión).
        """
        # Estado 15 del diagrama: dígitos antes del punto
        while self.caracter_actual().isdigit():
            self.avanzar()
        
        # Verificar si hay un punto decimal seguido de al menos un dígito
        es_decimal = False
        if self.caracter_actual() == '.' and self.mirar_siguiente().isdigit():
            es_decimal = True
            # Consumir el punto
            self.avanzar()
            
            # Estado 16: dígitos después del punto
            while self.caracter_actual().isdigit():
                self.avanzar()
        
        # Verificar si hay un exponente (E o e)
        if (self.caracter_actual() == 'E' or self.caracter_actual() == 'e'):
            # Consumir la E o e
            self.avanzar()
            
            # Verificar si hay un signo (+ o -) antes de los dígitos del exponente
            if self.caracter_actual() in ['+', '-']:
                self.avanzar()
            
            # Debe haber al menos un dígito después del exponente
            if not self.caracter_actual().isdigit():
                self.error_lexico("Se esperaba al menos un dígito después del exponente")
                return None
            
            # Consumir los dígitos del exponente
            while self.caracter_actual().isdigit():
                self.avanzar()
        
        # Extraer el texto del número
        lexema = self.codigo_fuente[self.inicio:self.actual]
        
        # Convertir el lexema al valor literal adecuado
        try:
            if es_decimal or 'e' in lexema.lower():
                literal = float(lexema)
            else:
                literal = int(lexema)
        except ValueError:
            self.error_lexico(f"No se pudo convertir '{lexema}' a un número válido")
            return None
        
        return self.agregar_token(TokenType.NUMBER, lexema, literal)


    
    def cadena(self):
        """
        Maneja las cadenas delimitadas por comillas dobles.
        """
        # Consumir caracteres hasta encontrar la comilla de cierre o un salto de línea
        while self.caracter_actual() != '"' and not self.fin_archivo():
            if self.caracter_actual() == '\n':
                self.error_lexico("Cadena sin terminar: se encontró un salto de línea")
                self.linea += 1
                return None
            self.avanzar()
        
        if self.fin_archivo():
            self.error_lexico("Cadena sin terminar: fin de archivo inesperado")
            return None
        
        # Consumir la comilla de cierre
        self.avanzar()
        
        # Extraer el contenido de la cadena (sin las comillas)
        valor = self.codigo_fuente[self.inicio + 1:self.actual - 1]
        return self.agregar_token(TokenType.STRING, self.codigo_fuente[self.inicio:self.actual], valor)



    def comentario_multilinea(self):
        """
        Maneja comentarios de múltiples líneas /* ... */
        """
        while not self.fin_archivo():
            c = self.avanzar()
            
            if c == '\n':
                self.linea += 1
            elif c == '*' and self.caracter_actual() == '/':
                # Encontramos el cierre del comentario
                self.avanzar()  # Consumir el '/'
                return None
        
        if self.fin_archivo():
            self.error_lexico("Comentario de múltiples líneas sin terminar: fin de archivo inesperado")
            return None

    
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
        if lexema is None:
            lexema = self.codigo_fuente[self.inicio:self.actual]
            
        token = TokenInfo(tipo, lexema, literal, self.linea)
        self.tokens.append(token)
        return token

    
    def error_lexico(self, mensaje):
        """
        Maneja errores léxicos.
        """
        self.error_handler.error_lexico(mensaje, self.linea)
        