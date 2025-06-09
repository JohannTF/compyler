from abc import ABC, abstractmethod
from src.interpreter.visitor_expression import VisitorExpression

class Expression(ABC):
    
    @abstractmethod
    def accept(self, visitor: VisitorExpression):
        pass