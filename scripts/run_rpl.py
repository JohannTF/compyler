#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para ejecutar únicamente el REPL o leer un archivo.
"""
import sys
import os

# Añadimos el directorio raíz al path para importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.interpreter.repl import start_repl
from src.utils.file_handler import read_file

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Iniciando modo REPL...")
        start_repl()
    elif len(sys.argv) == 2:
        file_path = sys.argv[1]
        try:
            content = read_file(file_path)
            print(content)
        except Exception as e:
            print(f"Error al leer el archivo: {e}")
    else:
        print("Hay más de un parámetro. Retornando a la terminal...")
        sys.exit(1)