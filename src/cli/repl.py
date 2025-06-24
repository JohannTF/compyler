"""
Módulo que implementa el REPL (Read-Eval-Print Loop) para interacción interactiva.
"""
from src.lexer.scanner import Scanner
from src.parser.parser import Parser
from src.interpreter.interpreter import Interpreter


def start_repl():
    """
    Inicia un REPL para interactuar con el intérprete.
    """
    print("Compilador")
    print("Escribe 'exit;', 'quit;', 'out;', 'bye;' o '0;' para salir")
    print()
    
    interpreter = Interpreter()
    
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
                    
            # Parser
            try:
                parser = Parser(tokens)
                ast = parser.parse()
                
                # Interpretar el AST resultante
                if ast:
                    interpreter.interpret(ast) 

            except Exception as e:
                print(f"Error: {e}")
            
        except EOFError:
            print()
            break
        except KeyboardInterrupt:
            print("\nOperación cancelada")
        except Exception as e:
            print(f"Error inesperado: {e}")