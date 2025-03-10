from src.utils.file_handler import read_file
from src.lexer.scanner import Scanner
from token_type import TokenType

def main():
    # Ruta al archivo de código fuente a analizar
    archivo_fuente = "test_files/codigo_fuente_ejemplo.txt"
    
    # Leer el contenido del archivo
    codigo_fuente = read_file(archivo_fuente)
    
    # Crear una instancia del escáner léxico
    scanner = Scanner(codigo_fuente)
    
    # Escanear los tokens
    scanner.escanear_tokens()
    
    # Obtener y mostrar los tokens generados
    tokens = scanner.tokens
    for token in tokens:
        print(token)

if __name__ == "__main__":
    main()