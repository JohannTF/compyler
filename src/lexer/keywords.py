# keywords.py
from .token_type import TokenType

class Keywords:
    """
    Maneja las palabras reservadas del lenguaje.
    """
    @staticmethod
    def get_keywords():
        """
        Devuelve un diccionario con las palabras reservadas y sus tipos de token correspondientes.
        """
        return {
            "and": TokenType.AND,
            "else": TokenType.ELSE,
            "false": TokenType.FALSE,
            "for": TokenType.FOR,
            "fun": TokenType.FUN,
            "if": TokenType.IF,
            "null": TokenType.NULL,
            "or": TokenType.OR,
            "print": TokenType.PRINT,
            "return": TokenType.RETURN,
            "true": TokenType.TRUE,
            "var": TokenType.VAR,
            "while": TokenType.WHILE, 
            "boolean": TokenType.BOOLEAN,
        }