"""
Script para realizar únicamente el análisis léxico de un archivo.
"""
import sys
import os
from src.utils import read_file
from src.lexer import Scanner

if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Si no se especifica archivo, usar un archivo de ejemplo
        file_path = "test/lexer/Cadenas.txt"
    else:
        file_path = sys.argv[1]
    
    try:
        # Leer el contenido del archivo
        source_code = read_file(file_path)
        
        # Crear una instancia del escáner léxico
        scanner = Scanner(source_code)
        
        # Escanear los tokens
        scanner.escanear_tokens()
        
        # Obtener y mostrar los tokens generados
        tokens = scanner.tokens
        
        print(f"\nAnálisis léxico:")
        print("-" * 50)
        for token in tokens:
            print(token)
        print("-" * 50)
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
        sys.exit(1)