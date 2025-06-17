from typing import Any, List, Dict
from src.interpreter.visitor_expression import VisitorExpression
from src.interpreter.visitor_statement import VisitorStatement
from src.interpreter.environment import Environment
from src.interpreter.runtime_error import RuntimeError
from src.parser.expression.expression import Expression
from src.parser.statement.statement import Statement

# Expressions
from src.parser.expression.ExprLiteral import ExprLiteral
from src.parser.expression.ExprGrouping import ExprGrouping
from src.parser.expression.ExprUnary import ExprUnary
from src.parser.expression.ExprBinary import ExprBinary
from src.parser.expression.ExprAritmetic import ExprArithmetic
from src.parser.expression.ExprVariable import ExprVariable
from src.parser.expression.ExprAssign import ExprAssign
from src.parser.expression.ExprLogical import ExprLogical
from src.parser.expression.ExprCallFunction import ExprCallFunction

# Statements
from src.parser.statement.stmt_expression import StmtExpression
from src.parser.statement.stmt_var import StmtVar
from src.parser.statement.StmtPrint import StmtPrint
from src.parser.statement.stmt_block import StmtBlock
from src.parser.statement.StmtIf import StmtIf
from src.parser.statement.StmtLoop import StmtLoop
from src.parser.statement.stmt_function import StmtFunction
from src.parser.statement.stmt_return import StmtReturn


class Interpreter(VisitorExpression[Any], VisitorStatement[None]):
    
    def __init__(self):
        self.globals = Environment()
        self.environment = self.globals
    
    def interpret(self, statements: List[Statement]) -> None:
        try:
            for statement in statements:
                self._execute(statement)
        except RuntimeError as error:
            print(f"Runtime Error: {error.message}")
            if hasattr(error.token, 'linea'):
                print(f"Línea: {error.token.linea}")
    
    def _evaluate(self, expression: Expression) -> Any:
        return expression.accept(self)
    
    def _execute(self, statement: Statement):
        statement.accept(self)
    
    # EXPRESSIONS
    
    def visit_literal_expression(self, expression: ExprLiteral) -> Any:
        return expression.value
    
    def visit_grouping_expression(self, expression: ExprGrouping) -> Any:
        return self._evaluate(expression.expression)
    
    """
    # Recuerda identar un tab justo despues de la definición de la función como en el resto de funciones
    def visit_unary_expression(self, expression: ExprUnary) -> Any:
    # Los operadores no se almacenan lexemas, sino en el atributo 'tipos' (Puedes checar que tipos hay en src\lexer\token_type.py)
    operator = expression.operator.tipo
    right = self._evaluate(expression.right)

    # Y, dado que no son lexemas, debes colocar el texto que aparece en src\lexer\token_type.py para identificar el tipo de operador al que pertenece
    # Este es solo un ejemplo pero, aplica lo mismo para el resto de operadores...
    if operator == "MINUS":
        # Previo a retornar '-right', verifica si se trata de un entero o un flotante el valor
        if isinstance(right, (int, float)):
            return -right
        else:
            raise RuntimeError(expression.operator, "Operand must be a number.")
    elif operator == "BANG":
        # Esta bien el método is_thruty para verificar que efectivamente sea un booleano, solo no olvides implementarlo al final de este archivo
        return not self._is_truthy(right)
        
    # Lo mismo aplica para incrementos y decrementos...
    elif operator in ("++", "--"):
        if not isinstance(expression.right, ExprVariable):
            raise RuntimeError(expression.operator, "El operador de incremento/decremento solo puede aplicarse a variables.")

        # Aquí, podrias aprovechar que ya tienes la función visit_variable_expression para evitar repetir código...
        # Obtener nombre de variable y valor actual
        var_name = expression.right.name
        current_value = self.environment.get(var_name)

        if not isinstance(current_value, (int, float)):
            raise RuntimeError(expression.operator, "El operador de incremento/decremento solo funciona con números.")

        new_value = current_value + 1 if operator == "++" else current_value - 1
        self.environment.assign(var_name, new_value)

        # Si es prefijo: retornar el nuevo valor
        # Si es postfijo: retornar el valor original
        return new_value if expression.is_prefix else current_value
    else:
        raise RuntimeError(expression.operator, f"Operador unario desconocido: {operator}")
     """
    
    """
    def visit_binary_expression(self, expression: ExprBinary) -> Any:
        # Lo mismo que en visit_unary_expression...
        left = self._evaluate(expression.left)
        right = self._evaluate(expression.right)
        operator = expression.operator.tipo

        if operator == "PLUS":
            # Antes de evaluar la expresión, verifica que sea un valor entero o flotante (y solo para este caso, puede ser también una string)
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return left + right
            if isinstance(left, str) and isinstance(right, str):
                return left + right
            raise RuntimeError(expression.operator, "Operands must be two numbers or two strings")
        # Lo mismo para las validaciones del resto de simbolos...
        # Procura dejar un espacio entre elif's
        elif operator == "-":
            return left - right
            
        elif operator == "*":
            return left * right
            
        elif operator == "/":
            if right == 0:
                raise RuntimeError(expression.operator, "División entre cero.")
            return left / right
        elif operator == ">":
            return left > right
        elif operator == ">=":
            return left >= right
        elif operator == "<":
            return left < right
        elif operator == "<=":
            return left <= right
        elif operator == "==":
            return left == right
        elif operator == "!=":
            return left != right
        else:
            raise RuntimeError(expression.operator, f"Operador desconocido: {operator}")
    """
    
    def visit_variable_expression(self, expression: ExprVariable) -> Any:
        return self.environment.get(expression.name)
    
    def visit_assign_expression(self, expression: ExprAssign) -> Any:
        value = self._evaluate(expression.value)
        self.environment.assign(expression.name, value)
        return value
    
    """
    # Elimine una delcaración de función que tenias repetida
    def visit_arithmetic_expression(self, expression: ExprArithmetic) -> Any:
        left = self._evaluate(expression.left)
        right = self._evaluate(expression.right)
        # Lo mismo con los operadores que en la del visit_unary_expression
        operator = expression.operator.tipo

        # No olvides implementar un método para verificar antes de retornar el resultado que sean de tipo entero flotantes o string según corresponda.
        if operator == "PLUS":
            return left + right
        elif operator == "MINUS":
            return left - right
        elif operator == "*":
            return left * right
        elif operator == "/":
            if right == 0:
                raise RuntimeError(expression.operator, "Division entre cero.")
            return left / right
        else:
            raise RuntimeError(expression.operator, f"operador desconocido '{operator}'")
    """
    
    """
    # Lo mismo que en las anteriores sugerencias
    def visit_logical_expression(self, expression: ExprLogical) -> Any:
        left = self._evaluate(expression.left)

        if expression.operator.tipo == "OR":
            # No olvides impelemntar el método _is_truthy
            if self._is_truthy(left):
                return left
        # En lugar del else, te sugiero cambiar por else if. Así, aseguramos que forzosamente debe matchear con AND o OR, y en caso de no hacerlo lanzar la excepción 
        elif expression.operator.tipo == "AND"
            if not self._is_truthy(left):
                return left
            return self._evaluate(expression.right)
        raise RuntimeError(expression.operator, f"Unknown logical operator: {operator_type}")
    """
        
    def visit_call_expression(self, expression: ExprCallFunction) -> Any:
        pass
        
    
    # STATEMENTS
    
    def visit_expression_statement(self, statement: StmtExpression) -> None:
        pass
    
    def visit_print_statement(self, statement: StmtPrint) -> None:
        pass
    
    def visit_var_statement(self, statement: StmtVar) -> None:
        pass
    
    def visit_block_statement(self, statement: StmtBlock) -> None:
        pass
    
    def visit_if_statement(self, statement: StmtIf) -> None:
        pass
    
    def visit_loop_statement(self, statement: StmtLoop) -> None:
        pass
    
    def visit_function_statement(self, statement: StmtFunction) -> None:
        pass
    
    def visit_return_statement(self, statement: StmtReturn) -> None:
        pass