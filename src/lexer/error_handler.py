class ErrorHandler:
    """
    Clase responsable de manejar y reportar errores durante el análisis léxico.
    """
    def __init__(self):
        self.errores = []
        self.had_error = False
    
    def error_lexico(self, mensaje, linea):
        """
        Registra un error léxico en una línea específica.
        """
        error_msg = f"Error léxico en línea {linea}: {mensaje}"
        self.errores.append(error_msg)
        self.had_error = True
        print(error_msg)
    
    def get_errors(self):
        """
        Devuelve la lista de errores encontrados.
        """
        return self.errores
    
    def has_errors(self):
        """
        Indica si se encontraron errores durante el análisis.
        """
        return self.had_error