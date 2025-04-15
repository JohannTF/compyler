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
                     "LEFT_PAREN", "MINUS", "BANG"]:
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
    
    def expression(self):
        # EXPRESSION -> ASSIGNMENT
        self.assignment()
    
    def assignment(self):
        # ASSIGNMENT -> LOGIC_OR ASSIGNMENT_OPC
        self.logic_or()
        self.assignment_opc()
    
    def assignment_opc(self):
        # ASSIGNMENT_OPC -> = EXPRESSION
        #                -> Ɛ
        if self.preanalisis.tipo == "EQUAL":
            self.coincidir("EQUAL")
            self.expression()
        # Si no es =, es épsilon
    
    def logic_or(self):
        # LOGIC_OR -> LOGIC_AND LOGIC_OR'
        self.logic_and()
        self.logic_or_prime()
    
    def logic_or_prime(self):
        # LOGIC_OR' -> or LOGIC_OR
        #          -> Ɛ
        if self.preanalisis.tipo == "OR":
            self.coincidir("OR")
            self.logic_or()
        # Si no es or, es épsilon
    
    def logic_and(self):
        # LOGIC_AND -> EQUALITY LOGIC_AND'
        self.equality()
        self.logic_and_prime()
    
    def logic_and_prime(self):
        # LOGIC_AND' -> and LOGIC_AND
        #           -> Ɛ
        if self.preanalisis.tipo == "AND":
            self.coincidir("AND")
            self.logic_and()
        # Si no es and, es épsilon
    
    def equality(self):
        # EQUALITY -> COMPARISON EQUALITY'
        self.comparison()
        self.equality_prime()
    
    def equality_prime(self):
        # EQUALITY' -> != EQUALITY
        #          -> == EQUALITY
        #          -> Ɛ
        tipo = self.preanalisis.tipo
        
        if tipo == "BANG_EQUAL":
            self.coincidir("BANG_EQUAL")
            self.equality()
        elif tipo == "EQUAL_EQUAL":
            self.coincidir("EQUAL_EQUAL")
            self.equality()
        # Si no es != o ==, es épsilon
    
    def comparison(self):
        # COMPARISON -> TERM COMPARISON'
        self.term()
        self.comparison_prime()
    
    def comparison_prime(self):
        # COMPARISON' -> > COMPARISON
        #            -> >= COMPARISON
        #            -> < COMPARISON
        #            -> <= COMPARISON
        #            -> Ɛ
        tipo = self.preanalisis.tipo
        
        if tipo == "GREATER":
            self.coincidir("GREATER")
            self.comparison()
        elif tipo == "GREATER_EQUAL":
            self.coincidir("GREATER_EQUAL")
            self.comparison()
        elif tipo == "LESS":
            self.coincidir("LESS")
            self.comparison()
        elif tipo == "LESS_EQUAL":
            self.coincidir("LESS_EQUAL")
            self.comparison()
        # Si no es >, >=, < o <=, es épsilon
    
    def term(self):
        # TERM -> FACTOR TERM'
        self.factor()
        self.term_prime()
    
    def term_prime(self):
        # TERM' -> - TERM
        #      -> + TERM
        #      -> Ɛ
        tipo = self.preanalisis.tipo
        
        if tipo == "MINUS":
            self.coincidir("MINUS")
            self.term()
        elif tipo == "PLUS":
            self.coincidir("PLUS")
            self.term()
        # Si no es - o +, es épsilon
    
    def factor(self):
        # FACTOR -> UNARY FACTOR'
        self.unary()
        self.factor_prime()
    
    def factor_prime(self):
        # FACTOR' -> / FACTOR
        #        -> * FACTOR
        #        -> Ɛ
        tipo = self.preanalisis.tipo
        
        if tipo == "SLASH":
            self.coincidir("SLASH")
            self.factor()
        elif tipo == "STAR":
            self.coincidir("STAR")
            self.factor()
        # Si no es / o *, es épsilon
    
    def unary(self):
        # UNARY -> ! UNARY
        #       -> - UNARY
        #       -> CALL
        tipo = self.preanalisis.tipo
        
        if tipo == "BANG":
            self.coincidir("BANG")
            self.unary()
        elif tipo == "MINUS":
            self.coincidir("MINUS")
            self.unary()
        else:
            self.call()
    
    def call(self):
        # CALL -> PRIMARY CALL'
        if self.preanalisis.tipo == "IDENTIFIER":
            self.coincidir("IDENTIFIER")
            if self.preanalisis.tipo == "LEFT_PAREN":
                self.call_prime()
        else: 
            self.primary()
    
    def call_prime(self):
        # CALL' -> ( ARGUMENTS )
        #      -> Ɛ
        if self.preanalisis.tipo == "LEFT_PAREN":
            self.coincidir("LEFT_PAREN")
            self.arguments()
            self.coincidir("RIGHT_PAREN")
        # Si no es (, es épsilon
    
    def primary(self):
        # PRIMARY -> true | false | null | number | string | id | ( EXPRESSION )
        tipo = self.preanalisis.tipo
        
        if tipo == "TRUE":
            self.coincidir("TRUE")
        elif tipo == "FALSE":
            self.coincidir("FALSE")
        elif tipo == "NULL":
            self.coincidir("NULL")
        elif tipo in ["INT", "FLOAT"]:
            self.coincidir(tipo)
        elif tipo == "STRING":
            self.coincidir("STRING")
        elif tipo == "IDENTIFIER":
            self.coincidir("IDENTIFIER")
        elif tipo == "LEFT_PAREN":
            self.coincidir("LEFT_PAREN")
            self.expression()
            self.coincidir("RIGHT_PAREN")
        else:
            self.error(["TRUE", "FALSE", "NULL", "INT", "FLOAT", "STRING", "IDENTIFIER", "LEFT_PAREN"])
    
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
    
    def arguments(self):
        # ARGUMENTS -> EXPRESSION ARGUMENTS'
        #          -> Ɛ
        if self.preanalisis.tipo != "RIGHT_PAREN":
            self.expression()
            self.arguments_prime()
        # Si es ), es épsilon
    
    def arguments_prime(self):
        # ARGUMENTS' -> , EXPRESSION ARGUMENTS'
        #           -> Ɛ
        if self.preanalisis.tipo == "COMMA":
            self.coincidir("COMMA")
            self.expression()
            self.arguments_prime()
        # Si no es ,, es épsilon