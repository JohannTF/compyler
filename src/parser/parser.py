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