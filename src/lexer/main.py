# main.py
from scan import Scanner

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
    // Este es un ejemplo de código para probar el scanner
    /* Este es un comentario
       de múltiples líneas
     */
    var x = 10;
    float y = 3.14;
    string nombre = "Hola mundo";
    
    if (x > 5) {
        print "x es mayor que 5";
    } else {
        print "x es menor o igual que 5";
    }
    
    // Probar operadores incremento/decremento
    x++;
    y--;
    
    // Probar operador ternario
    var resultado = (x > 10) ? "mayor" : "menor o igual";
    
    // Probar la función input (nueva funcionalidad)
    string entrada = input("Ingrese su nombre: ");
    
    // Probar valores booleanos y null
    boolean flag = true;
    var nada = null;
    
    // Probar número con exponente
    var cientifico = 1.5E2;
    """
    
    # Demostración del método escanear_tokens()
    print("==== Demostración de escanear_tokens() ====")
    analizar_codigo(codigo_ejemplo)
    
    
    
    
    
    # === A esta parte del código aún no le hagas caso porque no la he checado jeje
    print("\n==== Demostración de siguiente_token() ====")
    ejemplo_siguiente_token(codigo_ejemplo)
