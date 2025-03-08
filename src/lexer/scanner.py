from token import Token
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
    
    
    def siguiente_token(self):
        """
        Obtiene el siguiente token del código fuente.
        """


    def escanear_token(self):
        """
        Escanea un único token y lo define según su tipo
        """


    def avanzar(self):
        """
        Avanza al siguiente carácter y devuelve el actual.
        """

    
    def caracter_actual(self):
        """
        Devuelve el carácter actual sin avanzar.
        """
    
    def fin_archivo(self):
        """
        Verifica si se ha llegado al final del archivo.
        """

    
    def coincidir(self, esperado):
        """
        Verifica si el carácter actual coincide con el esperado (diagrama de estados)
        """

    
    def manejar_espacios(self, c):
        """
        Maneja los espacios en blanco y saltos de línea.
        """

    
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

    
    def mirar_siguiente(self):
        """
        Mira el siguiente carácter sin avanzar el puntero.
        """

    
    def agregar_token(self, tipo, lexema=None, literal=None):
        """
        Agrega un token a la lista de tokens.
        """

    
    def error_lexico(self, mensaje):
        """
        Maneja errores léxicos.
        """