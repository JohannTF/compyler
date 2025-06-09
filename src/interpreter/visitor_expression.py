from abc import ABC, abstractmethod
from typing import TypeVar, Generic

# Type variable para el tipo de retorno del visitor
T = TypeVar('T')


class VisitorExpression(ABC, Generic[T]):

    @abstractmethod
    def visit_assign_expression(self, expression) -> T:
        pass
    
    @abstractmethod
    def visit_arithmetic_expression(self, expression) -> T:
        pass
    
    @abstractmethod
    def visit_binary_expression(self, expression) -> T:
        pass
    
    @abstractmethod
    def visit_call_expression(self, expression) -> T:
        pass
    
    @abstractmethod
    def visit_grouping_expression(self, expression) -> T:
        pass
    
    @abstractmethod
    def visit_literal_expression(self, expression) -> T:
        pass
    
    @abstractmethod
    def visit_logical_expression(self, expression) -> T:
        pass
    
    @abstractmethod
    def visit_unary_expression(self, expression) -> T:
        pass
    
    @abstractmethod
    def visit_variable_expression(self, expression) -> T:
        pass
