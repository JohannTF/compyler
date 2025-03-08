"""
Módulo que implementa el REPL (Read-Eval-Print Loop) para interacción interactiva.
"""
import sys

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
            
            # Aquí procesamos el código ingresado
            # Por ahora solo haremos análisis léxico
            print(code)
            
        except EOFError:
            # Lanza la excepción con Ctrl + D (Unix o macOs) 
            print()
            break
        except KeyboardInterrupt:
            # Manejo de Ctrl+C
            print("\nOperación cancelada")
        except Exception as e:
            print(f"Error: {e}")