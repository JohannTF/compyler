from typing import Dict, Any, Optional
from src.lexer.token import Token
from src.interpreter.runtime_error import RuntimeError


class Environment:
    
    def __init__(self, enclosing: Optional['Environment'] = None):
        self.enclosing: Optional['Environment'] = enclosing
        self.values: Dict[str, Any] = {}
    
    def get(self, name: Token) -> Any:
        variable_name: str = name.lexema
        
        if variable_name in self.values:
            return self.values[variable_name]
        
        if self.enclosing is not None:
            return self.enclosing.get(name)
        
        raise RuntimeError(name, f"Undefined variable '{variable_name}'.")
    
    def assign(self, name: Token, value: Any) -> None:
        variable_name: str = name.lexema
        
        if variable_name in self.values:
            self.values[variable_name] = value
            return
        
        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return
        
        raise RuntimeError(name, f"Undefined variable '{variable_name}'.")
    
    def define(self, name: str, value: Any) -> None:
        self.values[name] = value
    
    def __str__(self) -> str:
        result: str = str(self.values)
        if self.enclosing is not None:
            result += " -> " + str(self.enclosing)
        return result
