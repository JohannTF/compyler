from typing import List

from src.lexer.token import Token

# Expressions 
from src.parser.expression.ExprAssign import ExprAssign
from src.parser.expression.ExprLogical import ExprLogical
from src.parser.expression.ExprBinary import ExprBinary
from src.parser.expression.ExprLiteral import ExprLiteral
from src.parser.expression.ExprUnary import ExprUnary
from src.parser.expression.ExprVariable import ExprVariable
from src.parser.expression.ExprGrouping import ExprGrouping
from src.parser.expression.ExprCallFunction import ExprCallFunction
from src.parser.expression.expression import Expression
from src.parser.statement.stmt_var import StmtVar


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.preanalisis = self.tokens[0] if tokens else None
        
    def parse(self):
        try:
            self.program()
            if self.preanalisis.tipo == "EOF":
                print("Programa válido")
                return True
            else:
                self.error(["EOF"])
                return False
        except SyntaxError as e:
            print(e)
            return False
            
    def error(self, expected):
        expected_str = " o ".join(expected)
        raise SyntaxError(f"Error sintáctico en la línea {self.preanalisis.linea}. Se esperaba {expected_str} pero se recibió {self.preanalisis.tipo}")

    def coincidir(self, token_type):
        if self.preanalisis.tipo == token_type:
            self.avanzar()
        else:
            self.error([token_type])
    
    def avanzar(self):
        self.current += 1
        if self.current < len(self.tokens):
            self.preanalisis = self.tokens[self.current]
    
    def previous(self) -> Token:
        return self.tokens[self.current - 1] if self.current > 0 else None
    
    # Implementación de los no terminales según la gramática
    def program(self):
        # PROGRAM -> DECLARATION
        self.declaration()
    
    def declaration(self):
        # DECLARATION -> FUN_DECL DECLARATION
        #             -> VAR_DECL DECLARATION
        #             -> STATEMENT DECLARATION
        #             -> Ɛ
        if self.preanalisis is None:
            return
        
        tipo = self.preanalisis.tipo
        
        if tipo == "FUN":
            self.fun_decl()
            self.declaration()
        elif tipo == "VAR":
            self.var_decl()
            self.declaration()
        elif tipo in ["IF", "FOR", "PRINT", "RETURN", "WHILE", "LEFT_BRACE", 
                     "IDENTIFIER", "STRING", "INT", "FLOAT", "TRUE", "FALSE", "NULL",
                     "LEFT_PAREN", "MINUS", "BANG", "INCREMENT", "DECREMENT"]:
            self.statement()
            self.declaration()
        # Si no coincide con ningún primero, es épsilon
        
    def fun_decl(self):
        # FUN_DECL -> fun id ( PARAMETERS ) BLOCK
        self.coincidir("FUN")
        self.coincidir("IDENTIFIER")
        self.coincidir("LEFT_PAREN")
        self.parameters()
        self.coincidir("RIGHT_PAREN")
        self.block()
    
    def var_decl(self):
        # VAR_DECL -> var id VAR_INIT ;
        self.coincidir("VAR")
        self.coincidir("IDENTIFIER")
        self.var_init()
        self.coincidir("SEMICOLON")
    
    def var_init(self):
        # VAR_INIT -> = EXPRESSION
        #          -> Ɛ
        if self.preanalisis.tipo == "EQUAL":
            self.coincidir("EQUAL")
            self.expression()
        # Si no es =, es épsilon
    
    def statement(self):
        # STATEMENT -> EXPR_STMT
        #           -> FOR_STMT
        #           -> IF_STMT
        #           -> PRINT_STMT
        #           -> RETURN_STMT
        #           -> WHILE_STMT
        #           -> BLOCK
        tipo = self.preanalisis.tipo
        
        if tipo == "FOR":
            self.for_stmt()
        elif tipo == "IF":
            self.if_stmt()
        elif tipo == "PRINT":
            self.print_stmt()
        elif tipo == "RETURN":
            self.return_stmt()
        elif tipo == "WHILE":
            self.while_stmt()
        elif tipo == "LEFT_BRACE":
            self.block()
        else:
            # Si no coincide con ninguna de las anteriores, debe ser una expresión
            self.expr_stmt()
    
    def expr_stmt(self):
        # EXPR_STMT -> EXPRESSION ;
        self.expression()
        self.coincidir("SEMICOLON")
    
    def for_stmt(self):
        # FOR_STMT -> for ( FOR_STMT_INIT FOR_STMT_COND FOR_STMT_INC ) STATEMENT
        self.coincidir("FOR")
        self.coincidir("LEFT_PAREN")
        self.for_stmt_init()
        self.for_stmt_cond()
        self.for_stmt_inc()
        self.coincidir("RIGHT_PAREN")
        self.statement()
    
    def for_stmt_init(self):
        # FOR_STMT_INIT -> VAR_DECL
        #               -> EXPR_STMT
        #               -> ;
        tipo = self.preanalisis.tipo
        
        if tipo == "VAR":
            self.var_decl()
        elif tipo == "SEMICOLON":
            self.coincidir("SEMICOLON")
        else:
            self.expr_stmt()
    
    def for_stmt_cond(self):
        # FOR_STMT_COND -> EXPRESSION ;
        #               -> ;
        if self.preanalisis.tipo != "SEMICOLON":
            self.expression()
        self.coincidir("SEMICOLON")
    
    def for_stmt_inc(self):
        # FOR_STMT_INC -> EXPRESSION
        #              -> Ɛ
        if self.preanalisis.tipo != "RIGHT_PAREN":
            self.expression()
        # Si no es expresión, es épsilon
    
    def if_stmt(self):
        # IF_STMT -> if ( EXPRESSION ) STATEMENT ELSE_STATEMENT
        self.coincidir("IF")
        self.coincidir("LEFT_PAREN")
        self.expression()
        self.coincidir("RIGHT_PAREN")
        self.statement()
        self.else_statement()
    
    def else_statement(self):
        # ELSE_STATEMENT -> else STATEMENT
        #                -> Ɛ
        if self.preanalisis.tipo == "ELSE":
            self.coincidir("ELSE")
            self.statement()
        # Si no es else, es épsilon
    
    def print_stmt(self):
        # PRINT_STMT -> print EXPRESSION ;
        self.coincidir("PRINT")
        self.expression()
        self.coincidir("SEMICOLON")
    
    def return_stmt(self):
        # RETURN_STMT -> return RETURN_EXP_OPC ;
        self.coincidir("RETURN")
        self.return_exp_opc()
        self.coincidir("SEMICOLON")
    
    def return_exp_opc(self):
        # RETURN_EXP_OPC -> EXPRESSION
        #                -> Ɛ
        if self.preanalisis.tipo not in ["SEMICOLON"]:
            self.expression()
        # Si es punto y coma, es épsilon
    
    def while_stmt(self):
        # WHILE_STMT -> while ( EXPRESSION ) STATEMENT
        self.coincidir("WHILE")
        self.coincidir("LEFT_PAREN")
        self.expression()
        self.coincidir("RIGHT_PAREN")
        self.statement()
    
    def block(self):
        # BLOCK -> { DECLARATION }
        self.coincidir("LEFT_BRACE")
        self.declaration()
        self.coincidir("RIGHT_BRACE")
    
    def expression(self) -> Expression:
        # EXPRESSION -> ASSIGNMENT
        return self.assignment()
    
    def assignment(self) -> Expression:
        # ASSIGNMENT -> LOGIC_OR ASSIGNMENT_OPC
        izquierda: Expression = self.logic_or()
        return self.assignment_opc(izquierda)
    
    def assignment_opc(self, izquierda: Expression) -> Expression:
        # ASSIGNMENT_OPC -> = EXPRESSION
        #                -> Ɛ
        if self.preanalisis.tipo == "EQUAL":
            self.coincidir("EQUAL")
            valor: Expression = self.expression()
            return ExprAssign(izquierda, valor)
        # Si no es =, es épsilon
        return izquierda
    
    def logic_or(self) -> Expression:
        # LOGIC_OR -> LOGIC_AND LOGIC_OR'
        izquierda: Expression = self.logic_and()
        return self.logic_or_prime(izquierda) 
    
    def logic_or_prime(self, izquierda: Expression) -> Expression:
        # LOGIC_OR' -> or LOGIC_OR
        #          -> Ɛ
        if self.preanalisis.tipo == "OR":
            self.coincidir("OR")
            operador: Token = self.previous()
            derecha: Expression = self.logic_or()
            return ExprLogical(izquierda, operador, derecha)
        # Si no es or, es épsilon
        return izquierda
    
    def logic_and(self) -> Expression:
        # LOGIC_AND -> EQUALITY LOGIC_AND'
        izquierda: Expression = self.equality()
        return self.logic_and_prime(izquierda)
    
    def logic_and_prime(self, izquierda: Expression) -> Expression:
        # LOGIC_AND' -> and LOGIC_AND
        #           -> Ɛ
        if self.preanalisis.tipo == "AND":
            self.coincidir("AND")
            operador: Token = self.previous()
            derecha: Expression = self.logic_and()
            return ExprLogical(izquierda, operador, derecha)
        # Si no es and, es épsilon
        return izquierda
    
    def equality(self) -> Expression:
        # EQUALITY -> COMPARISON EQUALITY'
        izquierda: Expression = self.comparison()
        return self.equality_prime(izquierda)
    
    def equality_prime(self, izquierda: Expression) -> Expression:
        # EQUALITY' -> != EQUALITY
        #          -> == EQUALITY
        #          -> Ɛ
        tipo = self.preanalisis.tipo
        
        if tipo == "BANG_EQUAL":
            self.coincidir("BANG_EQUAL")
            operador: Token = self.previous()
            derecha: Expression = self.equality()
            return ExprBinary(izquierda, operador, derecha)
        elif tipo == "EQUAL_EQUAL":
            self.coincidir("EQUAL_EQUAL")
            operador: Token = self.previous()
            derecha: Expression = self.equality()
            return ExprBinary(izquierda, operador, derecha)
        # Si no es != o ==, es épsilon
        return izquierda
    
    def comparison(self) -> Expression:
        # COMPARISON -> TERM COMPARISON'
        izquierda: Expression = self.term()
        return self.comparison_prime(izquierda)
    
    def comparison_prime(self, izquierda: Expression) -> Expression:
        # COMPARISON' -> > COMPARISON
        #            -> >= COMPARISON
        #            -> < COMPARISON
        #            -> <= COMPARISON
        #            -> Ɛ
        tipo = self.preanalisis.tipo
        
        if tipo == "GREATER":
            self.coincidir("GREATER")
            operador: Token = self.previous()
            derecha:Expression = self.comparison()
            return ExprBinary(izquierda, operador, derecha)
        elif tipo == "GREATER_EQUAL":
            self.coincidir("GREATER_EQUAL")
            operador: Token = self.previous()
            derecha: Expression = self.comparison()
            return ExprBinary(izquierda, operador, derecha)
        elif tipo == "LESS":
            self.coincidir("LESS")
            operador: Token= self.previous()
            derecha: Expression = self.comparison()
            return ExprBinary(izquierda, operador, derecha)
        elif tipo == "LESS_EQUAL":
            self.coincidir("LESS_EQUAL")
            operador: Token = self.previous()
            derecha: Expression = self.comparison()
            return ExprBinary(izquierda, operador, derecha)
        # Si no es >, >=, < o <=, es épsilon
        return izquierda
    
    def term(self) -> Expression:
        # TERM -> FACTOR TERM'
        izquierda: Expression = self.factor()
        return self.term_prime(izquierda)
    
    def term_prime(self, izquierda: Expression) -> Expression:
        # TERM' -> - TERM
        #      -> + TERM
        #      -> Ɛ
        tipo = self.preanalisis.tipo
        
        if tipo == "MINUS":
            self.coincidir("MINUS")
            operador: Token = self.previous()
            derecha: Expression = self.term()
            return ExprBinary(izquierda, operador, derecha)
        elif tipo == "PLUS":
            self.coincidir("PLUS")
            operador: Token = self.previous()
            derecha: Expression = self.term()
            return ExprBinary(izquierda, operador, derecha)
        # Si no es - o +, es épsilon
        return izquierda
      
    def factor(self) -> Expression:
        # FACTOR -> UNARY FACTOR'
        izquierda: Expression = self.unary()
        return self.factor_prime(izquierda)
    
    def factor_prime(self, izquierda: Expression) -> Expression:
        # FACTOR' -> / FACTOR
        #        -> * FACTOR
        #        -> Ɛ
        tipo = self.preanalisis.tipo
        
        if tipo == "SLASH":
            self.coincidir("SLASH")
            operador: Token = self.previous()
            derecha: Expression = self.factor()
            return ExprBinary(izquierda, operador, derecha)
        elif tipo == "STAR":
            self.coincidir("STAR")
            operador: Token = self.previous()
            derecha: Expression = self.factor()
            return ExprBinary(izquierda, operador, derecha)
        # Si no es / o *, es épsilon
        return izquierda
    
    def unary(self) -> Expression:
        # UNARY -> ! UNARY
        #       -> - UNARY
        #       -> ++ UNARY
        #       -> -- UNARY
        #       -> CALL
        tipo = self.preanalisis.tipo
        
        if tipo == "BANG":
            self.coincidir("BANG")
            operador: Token = self.previous()
            derecha: Expression = self.unary()
            return ExprUnary(operador, derecha)
        elif tipo == "MINUS":
            self.coincidir("MINUS")
            operador: Token = self.previous()
            derecha: Expression = self.unary()
            return ExprUnary(operador, derecha)
        elif tipo == "INCREMENT":
            self.coincidir("INCREMENT")
            operador: Token = self.previous()
            self.coincidir("IDENTIFIER")
            derecha: Expression = self.previous()
            return ExprUnary(operador, derecha)
        elif tipo == "DECREMENT": 
            self.coincidir("DECREMENT")
            operador: Token = self.previous()
            self.coincidir("IDENTIFIER")
            derecha: Expression = self.previous()
            return ExprUnary(operador, derecha)
        else:
            return self.call()
      
    def call(self) -> Expression:
        # CALL -> PRIMARY CALL'
        expresion: Expression = self.primary()
        return self.call_prime(expresion)
    
    def call_prime(self, callee: Expression) -> Expression:
        # CALL' -> ( ARGUMENTS )
        #       -> ++ (postfijo)
        #       -> -- (postfijo)
        #       -> Ɛ
        tipo = self.preanalisis.tipo
        
        if tipo == "LEFT_PAREN":
            self.coincidir("LEFT_PAREN")
            argumentos: List[Expression] = self.arguments()
            self.coincidir("RIGHT_PAREN")
            return ExprCallFunction(callee, argumentos)
        elif tipo == "INCREMENT":
            self.coincidir("INCREMENT")
            return ExprUnary(self.previous(), callee)
        elif tipo == "DECREMENT":
            self.coincidir("DECREMENT")
            return ExprUnary(self.previous(), callee)
        # Si no es ninguno de estos, es épsilon
        return callee
    
    def primary(self) -> Expression:
        # PRIMARY -> true | false | null | number | string | id | ( EXPRESSION )
        tipo = self.preanalisis.tipo
        
        if tipo == "TRUE":
            self.coincidir("TRUE")
            return ExprLiteral(self.previous().literal)
        elif tipo == "FALSE":
            self.coincidir("FALSE")
            return ExprLiteral(self.previous().literal)
        elif tipo == "NULL":
            self.coincidir("NULL")
            return ExprLiteral(self.previous().literal)
        elif tipo in ["INT", "FLOAT"]:
            self.coincidir(tipo)
            return ExprLiteral(self.previous().literal)
        elif tipo == "STRING":
            self.coincidir("STRING")
            return ExprLiteral(self.previous().literal)
        elif tipo == "IDENTIFIER":
            self.coincidir("IDENTIFIER")
            return ExprVariable(self.previous().literal)
        elif tipo == "LEFT_PAREN":
            self.coincidir("LEFT_PAREN")
            expresion: Expression = self.expression()
            self.coincidir("RIGHT_PAREN")
            return expresion
        else:
            self.error(["TRUE", "FALSE", "NULL", "INT", "FLOAT", "STRING", "IDENTIFIER", "LEFT_PAREN"])
            return ExprLiteral(None)
    
    def parameters(self):
        # PARAMETERS -> id PARAMETERS'
        #           -> Ɛ
        if self.preanalisis.tipo == "IDENTIFIER":
            self.coincidir("IDENTIFIER")
            self.parameters_prime()
        # Si no es id, es épsilon
    
    def parameters_prime(self):
        # PARAMETERS' -> , id PARAMETERS'
        #            -> Ɛ
        if self.preanalisis.tipo == "COMMA":
            self.coincidir("COMMA")
            self.coincidir("IDENTIFIER")
            self.parameters_prime()
        # Si no es ,, es épsilon
    
    def arguments(self) -> List[Expression]:
        # ARGUMENTS -> EXPRESSION ARGUMENTS'
        #          -> Ɛ
        args: List[Expression] = []
        if self.preanalisis.tipo != "RIGHT_PAREN":
            args.append(self.expression())
            self.arguments_prime(args)
        return args
        # Si es ), es épsilon
    
    def arguments_prime(self, args: List[Expression]):
        # ARGUMENTS' -> , EXPRESSION ARGUMENTS'
        #           -> Ɛ
        if self.preanalisis.tipo == "COMMA":
            self.coincidir("COMMA")
            args.append(self.expression())
            self.arguments_prime(args)
        # Si no es , es épsilon