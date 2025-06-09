import sys
from src.lexer.scanner import Scanner
from src.cli.repl import start_repl
from src.utils.file_handler import read_file as read_source_file
from src.parser.parser import Parser
from src.interpreter.interpreter import Interpreter

def read_file(source_file):
    """Lee un archivo y devuelve su contenido como texto."""
    try:
        return read_source_file(source_file)
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return None

def lexical_analysis(source_code):
    """Realiza el análisis léxico del código fuente y retorna los tokens."""
    if not source_code:
        return None
    
    try:
        scanner = Scanner(source_code)
        scanner.escanear_tokens()
        return scanner.tokens
    except Exception as e:
        print(f"Error en el análisis léxico: {e}")
        return None

def syntax_analysis(tokens):
    """Realiza el análisis sintáctico de los tokens."""
    if not tokens:
        return False
    
    try:
        parser = Parser(tokens)
        return parser.parse()
    except Exception as e:
        print(f"Error en el análisis sintáctico: {e}")
        return None

def interpret_ast(ast):
    if not ast or ast is False:
        return False
    
    try:
        interpreter = Interpreter()
        interpreter.interpret(ast)
        return True
    except Exception as e:
        print(f"Error en la interpretación: {e}")
        return False

def process_file(source_file):
    """Procesa un archivo completo: análisis léxico y sintáctico."""
    source_code = read_file(source_file)
    if not source_code:
        return False
    
    tokens = lexical_analysis(source_code)
    if not tokens:
        return False
    
    ast = syntax_analysis(tokens)
    
    return interpret_ast(ast)

def main():
    if len(sys.argv) == 1:
        start_repl()
    elif len(sys.argv) == 2:
        source_file = sys.argv[1]
        result = process_file(source_file)
        if not result:
            print("La compilación ha fallado.")
            sys.exit(1)
    else:
        print("Uso incorrecto. Proporcione un archivo o ejecute sin argumentos para el modo REPL.")
        sys.exit(1)

if __name__ == "__main__":
    main()
