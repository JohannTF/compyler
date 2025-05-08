"""
Script para ejecutar únicamente el REPL o leer un archivo.
"""
import sys
from src.interpreter import start_repl
from src.utils import read_file
from src.lexer import Scanner
from src.parser import Parser

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Iniciando modo REPL...")
        start_repl()
    elif len(sys.argv) == 2:
        file_path = sys.argv[1]
        try:
            # Leer archivo
            source_code = read_file(file_path)
            
            # Análisis léxico
            scanner = Scanner(source_code)
            scanner.escanear_tokens()
            tokens = scanner.tokens
            
            # Análisis sintáctico
            parser = Parser(tokens)
            if parser.parse():
                print(f"OK")
            else:
                print(f"ERROR")
                sys.exit(1)
        except Exception as e:
            print(f"Error al procesar el archivo: {e}")
            sys.exit(1)
    else:
        sys.exit(1)