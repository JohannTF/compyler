"""
Módulo que implementa el REPL (Read-Eval-Print Loop) para interacción interactiva.
"""
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.lexer.scanner import Scanner
from src.parser.parser import Parser


def start_repl(version="0.1.0"):
    """
    Inicia un REPL para interactuar con el intérprete.
    
    Args:
        version (str): Versión del intérprete a mostrar
    """
    print(f"Compilador v{version}")
    print("Escribe 'exit;', 'quit;', 'out;', 'bye;' o '0;' para salir")
    print()
    
    while True:
        try:
            code = input(">>> ")

            if code.lower() in {"exit;", "quit;", "out;", "bye;", "0;"}:
                print("Goodbye!")
                break
            
            # Procesamos el código con el analizador léxico
            scanner = Scanner(code)
            scanner.escanear_tokens()
            tokens = scanner.tokens
                
            # Verificar que se hayan leído tokens
            if not tokens:
                print("No se encontraron tokens para analizar")
                return
                    
            # Crear el parser y analizar la lista de tokens
            try:
                parser = Parser(tokens)
                parser.parse()
            except Exception as e:
                print(f"Error inesperado: {e}")
            
        except EOFError:
            print()
            break
        except KeyboardInterrupt:
            print("\nOperación cancelada")
        except Exception as e:
            print(f"Error: {e}")