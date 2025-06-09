from abc import ABC, abstractmethod
from typing import TypeVar, Generic

# Type variable para el tipo de retorno del visitor
T = TypeVar('T')


class VisitorStatement(ABC, Generic[T]):
    
    @abstractmethod
    def visit_block_statement(self, statement) -> T:
        pass
    
    @abstractmethod
    def visit_expression_statement(self, statement) -> T:
        pass
    
    @abstractmethod
    def visit_function_statement(self, statement) -> T:
        pass
    
    @abstractmethod
    def visit_if_statement(self, statement) -> T:
        pass
    
    @abstractmethod
    def visit_loop_statement(self, statement) -> T:
        pass
    
    @abstractmethod
    def visit_print_statement(self, statement) -> T:
        pass
    
    @abstractmethod
    def visit_return_statement(self, statement) -> T:
        pass
    
    @abstractmethod
    def visit_var_statement(self, statement) -> T:
        pass
