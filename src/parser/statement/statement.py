from abc import ABC, abstractmethod
from src.interpreter.visitor_statement import VisitorStatement

class Statement(ABC):
    
    @abstractmethod
    def accept(self, visitor: VisitorStatement):
        pass