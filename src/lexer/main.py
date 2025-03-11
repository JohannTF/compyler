from scanner import Scanner

def analizar_codigo(codigo_fuente):
    """
    Analiza una cadena de código fuente y muestra los tokens generados.
    
    Args:
        codigo_fuente: Cadena con el código fuente a analizar.
    """
    scanner = Scanner(codigo_fuente)
    tokens = scanner.escanear_tokens()
    
    print("Tokens generados:")
    for token in tokens:
        print(token)
    
    if scanner.error_handler.has_errors():
        print("\nSe encontraron errores durante el análisis:")
        for error in scanner.error_handler.get_errors():
            print(error)
    else:
        print("\nAnálisis léxico completado sin errores.")

def ejemplo_siguiente_token(codigo_fuente):
    """
    Demuestra el uso del método siguiente_token() para obtener tokens uno por uno.
    
    Args:
        codigo_fuente: Cadena con el código fuente a analizar.
    """
    scanner = Scanner(codigo_fuente)
    
    print("Obteniendo tokens uno por uno:")
    token = scanner.siguiente_token()
    while token and token.tipo != "EOF":
        print(token)
        token = scanner.siguiente_token()
    
    print(token)  # Imprimir token EOF

if __name__ == "__main__":
    # Ejemplo de uso con código embebido
    codigo_ejemplo = """
    // Prueba operadores logicos:
    5 and 5
    5 and5
    edad and(mes or anio)
    5 or 5
    5 or5
    """
    
    # Demostración del método escanear_tokens()
    print("==== Demostración de escanear_tokens() ====")
    analizar_codigo(codigo_ejemplo)
    
    
    
    
    
    # === A esta parte del código aún no le hagas caso porque no la he checado jeje
    print("\n==== Demostración de siguiente_token() ====")
    ejemplo_siguiente_token(codigo_ejemplo)
