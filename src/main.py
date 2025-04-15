import sys
from lexer.scan import Scanner
from interpreter.repl import start_repl
from utils.file_handler import read_file
from parser.parserc import Parser

def procesar_archivo(archivo_fuente):
    try:
        codigo_fuente = read_file(archivo_fuente)
        scanner = Scanner(codigo_fuente)
        scanner.escanear_tokens()
        tokens = scanner.tokens
        for token in tokens:
            print(token)
        return tokens
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")

def main():
    if len(sys.argv) == 1:
        start_repl()
    elif len(sys.argv) == 2:
        archivo_fuente = sys.argv[1]
        #procesar_archivo(archivo_fuente)
        tokens = procesar_archivo(archivo_fuente)
        # Verificar que se hayan leído tokens
        if not tokens:
            print("No se encontraron tokens para analizar")
            return
        
        # Crear el parser y analizar los tokens
        try:
            parser = Parser(tokens)
            parser.parse()
        except Exception as e:
            print(f"Error inesperado: {e}")
    else:
        print("Uso incorrecto. Proporcione un archivo o ejecute sin argumentos para el modo REPL.")
        sys.exit(1)

if __name__ == "__main__":
    main()
