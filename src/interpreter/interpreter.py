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

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value
        super().__init__()

class Function:
    def __init__(self, declaration: StmtFunction, closure: Environment):
        self.declaration = declaration
        self.closure = closure
    
    def call(self, interpreter, arguments: List[Any]) -> Any:
        # Crear nuevo entorno para la función
        environment = Environment(self.closure)
        
        # Vincular parámetros con argumentos
        for i, param in enumerate(self.declaration.params):
            if i < len(arguments):
                environment.define(param.lexema, arguments[i])
            else:
                environment.define(param.lexema, None)
        
        try:
            # Ejecutar el cuerpo de la función
            interpreter.execute_block(self.declaration.body.statements, environment)
        except ReturnException as return_exception:
            return return_exception.value
        
        # Si no hay return explícito, retornar None
        return None

class Interpreter(VisitorExpression[Any], VisitorStatement[None]):
    def __init__(self):
        self.globals = Environment()
        self.environment = self.globals
    
    def interpret(self, statements: List[Statement]) -> None:
        try:
            for statement in statements:
                self._execute(statement)
        except RuntimeError as error:
            line_info = ""
            if hasattr(error, 'token') and hasattr(error.token, 'linea'):
                line_info = f" At line {error.token.linea}"
            print(f"Runtime Error: {error.message}{line_info}")
        except Exception as e:
            print(f"Unexpected error in interpreter: {e}")
    
    def _evaluate(self, expression: Expression) -> Any:
        return expression.accept(self)
    
    def _execute(self, statement: Statement):
        statement.accept(self)

    # EXPRESSIONS
    
    def visit_literal_expression(self, expression: ExprLiteral) -> Any:
        return expression.value
    
    def visit_grouping_expression(self, expression: ExprGrouping) -> Any:
        return self._evaluate(expression.expression)
    
    def visit_unary_expression(self, expression: ExprUnary) -> Any:
        operator = expression.operator.tipo
        right = self._evaluate(expression.right)

        if operator == "MINUS":
            if isinstance(right, (int, float)):
                return -right
            else:
                raise RuntimeError(expression.operator, "Operand must be a number")
       
        elif operator == "BANG":
            return not self._is_truthy(right)
       
        elif operator in ("INCREMENT", "DECREMENT"):
            if not isinstance(expression.right, ExprVariable):
                raise RuntimeError(expression.operator, "Increment/decrement operator can only be applied to variables.")
            
            var_name = expression.right.name
            current_value = self.visit_variable_expression(expression.right)

            if not isinstance(current_value, (int, float)):
                raise RuntimeError(expression.operator, "Increment/decrement operator only works with numbers.")
            
            new_value = current_value + 1 if operator == "INCREMENT" else current_value - 1
            self.environment.assign(var_name, new_value)

            return new_value
        else:
            raise RuntimeError(expression.operator, f"Unknown unary operator: {operator}")

    def visit_binary_expression(self, expression: ExprBinary) -> Any:
        left = self._evaluate(expression.left)
        right = self._evaluate(expression.right)
        operator = expression.operator.tipo
        
        if operator == "PLUS":
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return left + right
            elif isinstance(left, str) and isinstance(right, str):
                return left + right
            elif isinstance(left, str) and isinstance(right, (int, float)):
                return left + self._stringify(right)
            elif isinstance(left, (int, float)) and isinstance(right, str):
                return self._stringify(left) + right
            else:
                raise RuntimeError(expression.operator, "Operands must be two numbers or two strings.")
        
        elif operator == "MINUS":
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return left - right
            else:
                raise RuntimeError(expression.operator, "Operands must be numbers.")
        
        elif operator == "STAR":
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return left * right
            else:
                raise RuntimeError(expression.operator, "Operands must be numbers.")
        
        elif operator == "SLASH":
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                if right == 0:
                    raise RuntimeError(expression.operator, "Division by zero.")
                return left / right
            else:
                raise RuntimeError(expression.operator, "Operands must be numbers.")
       
        elif operator == "GREATER":
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return left > right
            else:
                raise RuntimeError(expression.operator, "Operands must be numbers.")
        
        elif operator == "GREATER_EQUAL":
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return left >= right
            else:
                raise RuntimeError(expression.operator, "Operands must be numbers.")
        
        elif operator == "LESS":
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return left < right
            else:
                raise RuntimeError(expression.operator, "Operands must be numbers.")
        
        elif operator == "LESS_EQUAL":
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return left <= right
            else:
                raise RuntimeError(expression.operator, "Operands must be numbers.")
        
        elif operator == "EQUAL_EQUAL":
            return left == right
        
        elif operator == "BANG_EQUAL":
            return left != right
        else:
            raise RuntimeError(expression.operator, f"Unknown operator: {operator}")

    def visit_arithmetic_expression(self, expression: ExprArithmetic) -> Any:
        left = self._evaluate(expression.left)
        right = self._evaluate(expression.right)

        operator = expression.operator.tipo

        if operator == "PLUS":
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return left + right
            elif isinstance(left, str) and isinstance(right, str):
                return left + right
            elif isinstance(left, str) and isinstance(right, (int, float)):
                return left + self._stringify(right)
            elif isinstance(left, (int, float)) and isinstance(right, str):
                return self._stringify(left) + right
            else:
                raise RuntimeError(expression.operator, "Operands must be two numbers or two strings.")
        
        elif operator == "MINUS":
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return left - right
            else:
                raise RuntimeError(expression.operator, "Operands must be numbers.")
       
        elif operator == "STAR":
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return left * right
            else:
                raise RuntimeError(expression.operator, "Operands must be numbers.")
        
        elif operator == "SLASH":
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                if right == 0:
                    raise RuntimeError(expression.operator, "Division by zero.")
                return left / right
            else:
                raise RuntimeError(expression.operator, "Operands must be numbers.")
        else:
            raise RuntimeError(expression.operator, f"Unknown operator '{operator}'")
            
    def visit_variable_expression(self, expression: ExprVariable) -> Any:
        return self.environment.get(expression.name)
    
    def visit_assign_expression(self, expression: ExprAssign) -> Any:
        value = self._evaluate(expression.value)
        self.environment.assign(expression.name, value)
        return value
    
    def visit_logical_expression(self, expression: ExprLogical) -> Any:
        left = self._evaluate(expression.left)

        if expression.operator.tipo == "OR":
            if self._is_truthy(left):
                return left
            else:
                return self._evaluate(expression.right)
        elif expression.operator.tipo == "AND":  
            if not self._is_truthy(left):
                return left
            else:
                return self._evaluate(expression.right)
        else:
            raise RuntimeError(expression.operator, f"Unknown logical operator: {expression.operator.tipo}")
    
    def visit_call_expression(self, expression: ExprCallFunction) -> Any:
        callee = self._evaluate(expression.callee)
        
        arguments = []
        for argument in expression.arguments:
            arguments.append(self._evaluate(argument))
        
        if not isinstance(callee, Function):
            raise RuntimeError(expression.paren, "Can only call functions and classes.")
        
        function = callee
        if len(arguments) != len(function.declaration.params):
            raise RuntimeError(expression.paren, f"Expected {len(function.declaration.params)} arguments but got {len(arguments)}.")
        
        return function.call(self, arguments)

    # STATEMENTS
    
    def visit_expression_statement(self, statement: StmtExpression) -> None:
        self._evaluate(statement.expression)
        return None
    
    def visit_print_statement(self, statement: StmtPrint) -> None:
        value = self._evaluate(statement.expression)
        print(self._stringify(value))
        return None
    
    def visit_var_statement(self, statement: StmtVar) -> None:
        value = None
        if statement.initializer is not None:
            value = self._evaluate(statement.initializer)
        self.environment.define(statement.name.lexema, value)
        return None
    
    def visit_block_statement(self, statement: StmtBlock) -> None:
        self.execute_block(statement.statements, Environment(self.environment))
        return None
    
    def visit_if_statement(self, statement: StmtIf) -> None:
        condition = self._evaluate(statement.condition)
        if self._is_truthy(condition):
            self._execute(statement.thenBranch)
        elif statement.elseBranch is not None:
            self._execute(statement.elseBranch)
        return None
    
    def visit_loop_statement(self, statement: StmtLoop) -> None:
        while self._is_truthy(self._evaluate(statement.condition)):
            if isinstance(statement.body, StmtBlock):
                for stmt in statement.body.statements:
                    self._execute(stmt)
            else:
                self._execute(statement.body)
        return None
    
    def visit_function_statement(self, statement: StmtFunction) -> None:
        function = Function(statement, self.environment)
        self.environment.define(statement.name.lexema, function)
        return None
    
    def visit_return_statement(self, statement: StmtReturn) -> None:
        value = None
        if statement.value is not None:
            value = self._evaluate(statement.value)
        
        # Proper way to handle return is with custom exception
        raise ReturnException(value)
    
    # FUNCIONES AUXILIARES
    
    def execute_block(self, statements: List[Statement], environment: Environment) -> None:
        previous = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self._execute(statement)
        finally:
            self.environment = previous
    
    def _is_truthy(self, obj: Any) -> bool:
        if obj is None:
            return False
        if isinstance(obj, bool):
            return obj
        if isinstance(obj, str):
            return len(obj) > 0
        if isinstance(obj, (int, float)):
            return obj != 0
        return True

    def _stringify(self, obj: Any) -> str:
        if obj is None:
            return "null"
        if isinstance(obj, bool):
            return "true" if obj else "false"
        if isinstance(obj, str):
            return f'{obj}'
        if isinstance(obj, float):
            text = str(obj)
            if text.endswith(".0"):
                text = text[:-2]
            return text
        return str(obj)
