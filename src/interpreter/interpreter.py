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
    
    def visit_unary_expression(self, expression: ExprUnary) -> Any:
        pass
    
    def visit_binary_expression(self, expression: ExprBinary) -> Any:
        pass
    
    def visit_variable_expression(self, expression: ExprVariable) -> Any:
        return self.environment.get(expression.name)
    
    def visit_assign_expression(self, expression: ExprAssign) -> Any:
        value = self._evaluate(expression.value)
        self.environment.assign(expression.name, value)
        return value
    
    """
    
    def visit_arithmetic_expression(self, expression: ExprArithmetic) -> Any:
        def visit_arithmetic_expression(self, expression: ExprArithmetic) -> Any:
        left = self._evaluate(expression.left)
        right = self._evaluate(expression.right)

        operator = expression.operator.lexema

        if operator == "+":
            return left + right
        elif operator == "-":
            return left - right
        elif operator == "*":
            return left * right
        elif operator == "/":
            if right == 0:
                raise RuntimeError(expression.operator, "Division by zero.")
            return left / right
        elif operator == "%":
            return left % right
        elif operator == "**":
            return left ** right
        else:
            raise RuntimeError(expression.operator, f"Unknown operator '{operator}'")
"""
    
    """
    def visit_logical_expression(self, expression: ExprLogical) -> Any:
        left = self._evaluate(expression.left)

        if expression.operator.lexema == "or":
            if self._is_truthy(left):
                return left
        else:  
            if not self._is_truthy(left):
                return left

        return self._evaluate(expression.right)

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