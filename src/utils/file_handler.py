"""
Manejo de archivos y entrada/salida.
"""
import sys

def read_file(file_name) -> str:
    """
    Lee el contenido de un archivo de texto.
    
    Args:
        file_name (str): Ruta al archivo a leer
        
    Returns:
        str: Contenido del archivo
        
    Raises:
        FileNotFoundError: Si el archivo no existe
        Exception: Para otros errores de lectura
    """
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: El archivo '{file_name}' no existe")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)