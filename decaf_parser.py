import re
import sys

lines   = []
tokens  = []
original = []
pos     = -1
tabs    = 0

def error_handle():        
    global tokens, pos, lines, tabs

    line_no = get_line()
    token   = lines[pos].split()[0]
    line    = original[int(line_no) - 1]
    print("\n*** Error line " + line_no + ".")
    print(line)
    result = line.find(token) 
    print( " " * (result) + '^'*len(token)) 

    print("*** syntax error\n\n")
    sys.exit()

def get_spaces(line):
    if int(line) < 10:
        sp = 2
    elif int(line) < 100:
        sp = 1
    else:
        sp = 0
    return sp

def get_line():
    global lines
    line = re.findall(r"line \d+",lines[pos])[0].split()[-1]
    return line

def next_token():
    global tokens, pos
    if pos + 1 < len(tokens):
        pos += 1
    else:
        error_handle()

def check_next():
    global tokens, pos
    if pos + 1 > len(tokens):
        error_handle()

class ProgramNode:

    def __init__(self):
        self.programNode = ["\n"+" "*3 + 'Program:']
        self.decls = []
        
    def program(self):
        global tokens, pos, tabs
        
        if not tokens:
            print("Empty program is syntactically incorrect.")
            return
        else:
            #Keep adding decl to the program
            while (pos + 1) < len(tokens):
                self.decls.append(DeclNode().decl())

        self.programNode.append(self.decls)
        self.print_data(self.programNode)

        return self.decls

    def load_data(self, raw_dir = '', lex_dir = ''):
        global lines, tokens, original, tabs
        try:
            if lex_dir:
                f = open(lex_dir)
                lines = f.read().split('\n')
                #Loop for getting constants: string, int, double
                for line in lines:
                    if line:
                        if re.findall(r'\(.*?\)', line):
                            tokens.append(line.split('(')[0].split()[-1])
                        else:
                            tokens.append(line.split()[-1])
                #Remove extra ' on tokens
                tokens = [token.replace("'", '') for token in tokens]
                f.close()
            if raw_dir:
                f = open(raw_dir)
                original = f.read().split('\n')
                f.close() 
        except FileNotFoundError as e:
            print(e)
            
    def print_data(self, prog):
        global tabs

        for node in prog:
            if isinstance(node, list):
                self.print_data(node)
            else:
                print(node)

class DeclNode:
    def __init__(self):
        self.variabledecl = []
        self.variablefunct = []

    def decl(self):
        global tokens, pos, tabs
        #Check declaration type

        if pos + 1 < len(tokens):
            if re.match(r"T_Int|T_Double|T_String|T_Bool|T_Void", tokens[pos + 1]):
                if pos + 2 < len(tokens):
                    if tokens[pos + 2] == 'T_Identifier':
                        if pos + 3 < len(tokens):
                            if tokens[pos + 3] == '(':
                                #Function declaration
                                tabs += 3
                                self.variablefunct = self.functionDecl()
                                tabs -= 3
                                return self.variablefunct
                            else:
                                #Variable declaration
                                tabs += 3
                                self.variabledecl = self.variableDecl()
                                tabs -= 3
                                return self.variabledecl           
                        else:
                            pos += 2
                            error_handle()
                    else:
                        pos += 1
                        error_handle() 
                else:
                    pos += 1
                    error_handle()
            else:
                pos += 1
                error_handle()
        else:
            error_handle()
            

    def functionDecl(self):
        global tokens, pos, lines, tabs
        
        next_token()

        line = get_line()


        fnDecl = [" "*get_spaces(line) + line + " "*tabs + "FnDecl:"]
        #Get line #, type of function, and identifier
        
        tabs += 3
        fnDecl.append(" "*3 + " "*tabs + "(return type) Type: " + re.findall(r"int|double|string|bool|void", lines[pos].split()[0])[0])
        
        if tokens[pos + 1] == 'T_Identifier':
            next_token()
            line = get_line()
            fnDecl.append(" "*get_spaces(line) + line + " "*tabs +"Identifier: " + lines[pos].split()[0])
        else:
            next_token()
            error_handle()               

        #Formals
        if tokens[pos + 1] == '(':
            if tokens[pos + 2] != ')':
                fnDecl.append(self.formals())
            else:
                #consume ( and )
                pos += 2
        else:
            next_token()
            error_handle()
            
        #Statement block
        if tokens[pos + 1] == '{':
            fnDecl.append(" "*3 + " "*tabs +'(body) StmtBlock:')
            fnDecl.append(StatementNode().stmtBlock())
        else:
            next_token()
            error_handle()
            
        return fnDecl

    def variableDecl(self):
        global tokens, pos, lines, tabs     
        
        var = []
        line = re.findall(r"line \d+",lines[pos + 1])[0].split()[-1]
        var.append(" "*get_spaces(line) + line + " "*tabs + "VarDecl:")

        var.append(self.variable())  
        if tokens[pos + 1] == ';':
            next_token()
            return var
        else:
            next_token()
            error_handle()
            
    
    def variable(self):
        global tokens, pos, lines, tabs

        next_token()
        var = []
        tabs += 3
        var.append(" "*3 + " "*tabs +"Type: " + re.findall(r"int|double|string|bool|void", lines[pos].split()[0])[0])

        if tokens[pos + 1] == 'T_Identifier':
            next_token()
            line = get_line()
            var.append(" "*get_spaces(line) + line + " "*tabs +"Identifier: " + lines[pos].split()[0]) 
        else:
            next_token() 
            error_handle()
        
        tabs -= 3   
        return var
    
    #List of variables seperated by comma
    def formals(self):
        global tokens, pos, lines, tabs
        formals = []
        next_token()
        line = get_line()
        formals.append(" "*get_spaces(line) + line + " "*tabs +'(formals) VarDecl:')

        formals.append(self.variable())

        while tokens[pos + 1] == ',':
            next_token()
            line = get_line()
            formals.append(" "*get_spaces(line) + line + " "*tabs +'(formals) VarDecl:')
            formals.append(self.variable()) 
        
        #Consume )
        if tokens[pos + 1] == ')':
            next_token()   
        else:
            next_token()
            error_handle()
                           
        return formals

class StatementNode:
    def __init__(self):
        self.stmts = []
        self.variabledecl = []
        self.variablestmt = []

    def stmtBlock(self):
        global tokens, pos, lines, tabs

        #Consume {
        next_token()
        tabs += 3 

        if tokens[pos + 1] == '}':
            next_token()
            return     

        while re.match(r"T_Int|T_Double|T_String|T_Bool|T_Void", tokens[pos + 1]):      
            self.variabledecl.append(DeclNode().variableDecl())

        while tokens[pos + 1] != '}': 
            self.variablestmt.append(self.stmt())

        #redundant?
        if tokens[pos + 1] == '}':
            next_token()
        else:
            next_token()
            error_handle()

        self.stmts.append(self.variabledecl)
        self.stmts.append(self.variablestmt)   
        tabs -= 3 
        return self.stmts
    
    def stmt(self):
        global tokens, pos, lines, tabs

        stmt = []

        if tokens[pos + 1] == 'T_If':
            stmt.append(" "*3 + " "*tabs + 'ifStmt:')
            tabs += 3
            stmt.append(self.ifStmt())
            tabs -= 3
        elif tokens[pos + 1] == 'T_While':
            stmt.append(" "*3 + " "*tabs + 'WhileStmt:')
            tabs += 3
            stmt.append(self.whileStmt())     
            tabs -= 3       
        elif tokens[pos + 1] == 'T_For':
            stmt.append(" "*3 + " "*tabs + 'ForStmt:')
            tabs += 3
            stmt.append(self.forStmt())   
            tabs -= 3              
        elif tokens[pos + 1] == 'T_Break':
            next_token()  
            stmt.append(" "*3 + " "*tabs + 'BreakStmt:')
            if tokens[pos + 1] == ';':
                next_token()                              
            else:
                next_token()
                error_handle()
        elif tokens[pos + 1] == 'T_Return':
            next_token() 
            line = get_line()
            stmt.append(" "*get_spaces(line) + line + " "*tabs +'ReturnStmt:')
            tabs += 3
            
            if tokens[pos + 1] == ';':
                stmt.append(" "*3 + " "*tabs + 'Empty:')
                next_token()                           
            else:
                stmt.append(ExpressionNode().logicOr())      
            tabs -= 3
            
            if tokens[pos + 1] == ';':
                next_token()                
            else:
                next_token()
                error_handle()
        elif tokens[pos + 1] == 'T_Print':
            #consume print token
            next_token()
            if tokens[pos + 1] == '(':
                stmt.append(" "*3 + " "*tabs + 'PrintStmt:')
                tabs += 3
                stmt.append(self.printStmt()) 
                tabs -= 3                                   
            else:
                next_token()
                error_handle()
        elif tokens[pos + 1] == '{':
            stmt.append(" "*3 + " "*tabs + 'StmtBlock:')
            tabs += 3
            stmt.append(StatementNode().stmtBlock())  
            tabs -= 3
        else:
            stmt = ExpressionNode().expBlock()            
            if tokens[pos + 1] == ';':
                next_token()                
            else:
                pos += 2
                error_handle()

        return stmt
                

    def printStmt(self):
        global tokens, pos, lines, tabs 
        #consume (
        next_token()
        exprs = []

        if tokens[pos + 1] == ')':
            next_token()
            return 

        x = ExpressionNode().expBlock()
        x[0] = "(args) " + x[0]
        exprs.append(x)

        while tokens[pos + 1] == ',':
            next_token()
            x = ExpressionNode().expBlock()
            x[0] = "(args) " + x[0]
            exprs.append(x)

        #Consume )
        if tokens[pos + 1] == ')':
            next_token()
            if tokens[pos + 1] == ';':
                next_token()
            else:
                next_token()
                error_handle()
        else:
            next_token()
            error_handle()
            
        return exprs

    def ifStmt(self):
        global tokens, lines, pos, tabs

        #consume if token
        next_token()

        stmt = []

        if tokens[pos + 1] == '(':
            #consume (
            next_token()

            stmt.append(ExpressionNode().logicOr())
            if tokens[pos + 1] == ')':
                #consume )
                next_token()
            else:
                next_token()
                error_handle()
        else:
            next_token()
            error_handle()
        
        x = self.stmt() 
        x[0] = "(then) " + x[0]
        stmt.append(x)

        while tokens[pos + 1] == 'T_Else':
            next_token()
            x = self.stmt() 
            x[0] = "(then) " + x[0]
            stmt.append(x)

        return stmt

    def whileStmt(self):
        global tokens, lines, pos, tabs
        stmt = []
        #consume while token
        next_token()

        if tokens[pos + 1] == '(':
            #consume (
            next_token()
            stmt.append(ExpressionNode().logicOr())
            if tokens[pos + 1] == ')':
                #consume )
                next_token()
            else:
                next_token()
                error_handle()              
        else:
            next_token()
            error_handle()           

        stmt.append(self.stmt())

        return stmt

    def forStmt(self):
        global tokens, lines, pos, tabs
        stmt = []
        #consume for token
        next_token()

        if tokens[pos + 1] == '(':
            #consume (
            next_token()
          
            #first expression may be empty
            if tokens[pos + 1] == ';':
                stmt.append("(init) Empty:")
                next_token()
            else:
                x = ExpressionNode().logicOr()
                x[0] = "(init) " + x[0]
                stmt.append(x)
                #stmt.append(ExpressionNode().logicOr())
                             
            #second expression is enforced
            x = ExpressionNode().logicOr()
            x[0] = "(test) " + x[0]
            stmt.append(x)
            #stmt.append(ExpressionNode().logicOr())

            #enforce ; after expression
            if tokens[pos + 1] == ';':
                next_token()
            else:
                next_token()
                error_handle()
                

            #third expression is optional
            if tokens[pos + 1] == ';':
                stmt.append("(step) Empty:")
                next_token()
            else:
                x = ExpressionNode().logicOr()
                x[0] = "(step) " + x[0]
                stmt.append(x)
                #stmt.append(ExpressionNode().logicOr())            
            
            if tokens[pos + 1] == ')':
                #consume )
                next_token()
            else:
                next_token()
                error_handle()
        else:
            next_token()
            error_handle()
            

        stmt.append(self.stmt())

        return stmt

class ExpressionNode:
    def __init__(self):
        self.expr = []
    
    def expBlock(self):
        global tokens, pos, lines, tabs
        
        expr = []
        if tokens[pos + 1]:
            if tokens[pos + 1] == 'T_Identifier':
                if tokens[pos + 2] == '=':
                    expr = self.assign()
                elif tokens[pos + 2] == '(':
                    #consume ident
                    next_token()
                    line = get_line()
                    expr.append(" "*get_spaces(line) + line + " "*tabs +'Call:')
                    tabs += 3
                    expr.append(" "*get_spaces(line) + line + " "*tabs +'Identifier: ' + lines[pos].split()[0])
                    tabs -= 3
                    expr.append(self.actuals())
                else:
                    #consume ident
                    next_token()
                    line = get_line()
                    expr.append(" "*get_spaces(line) + line + " "*tabs +'Identifier: ' + lines[pos].split()[0])                    
            elif tokens[pos + 1] == '(':
                expr.append(self.parenthesis())
            elif re.match(r"\-|\!",tokens[pos + 1]):
                expr.append('Unary:')
                expr.append(self.unary())
            elif re.match(r"T_IntConstant|T_DoubleConstant|T_StringConstant|T_BoolConstant", tokens[pos + 1]):
                #consume constant token
                next_token()
                line = get_line()
                name = tokens[pos].split('_')[1]
                if tokens[pos] == 'T_StringConstant':
                    value = name + ': ' + '"' + lines[pos].split('"')[1] + '"'
                    expr.append(" "*get_spaces(line) + line + " "*tabs + value)
                else:
                    value = name + ": " + lines[pos].split()[0]
                    expr.append(" "*get_spaces(line) + line + " "*tabs + value)
            elif tokens[pos + 1] == 'T_ReadInteger':
                #consume readinteger, (, )
                line = get_line()
                pos += 3
                expr.append(" "*get_spaces(line) + line + " "*tabs +'ReadIntegerExpr:')
            else:
                next_token()
                error_handle()
        return expr
        
    def parenthesis(self):
        global tokens, pos, lines, tabs
        #consume (
        next_token() 
        expr = []

        if tokens[pos + 1] == ')':
            #consume )
            next_token()
            return 
        else:
            expr = self.logicOr()

        if tokens[pos + 1] == ')':
            next_token()
        else:
            next_token()
            error_handle()
            
        
        return expr
    
    def actuals(self):
        global tokens, pos, lines, tabs
        actuals = []
        #consume (
        next_token()

        if tokens[pos + 1] == ')':
            next_token()
            return 

        x = self.logicOr()
        x[0] = "(actuals) " + x[0]
        actuals.append(x)

        while tokens[pos + 1] == ',':
            next_token()
            x = self.logicOr()
            line = get_line()
            x[0] = " "*get_spaces(line) + line + " "*tabs + "(actuals) " + x[0]
            actuals.append(x)
        
        #Consume )
        if tokens[pos + 1] == ')':
            next_token()
        else:
            next_token()
            error_handle()
            
        return actuals
    
    def unary(self):
        global tokens, pos, lines, tabs
        expr = []

        if re.match(r"\-|\!",tokens[pos + 1]):
            next_token()
            line = get_line()
            expr.append(" "*get_spaces(line) + line + " "*tabs +'Operator: ' + tokens[pos])
            expr.append(self.expBlock())
        else:
            line = get_line()
            expr.append(" "*get_spaces(line) + line + " "*tabs +"FieldAccess:")
            tabs += 3
            expr.append(self.expBlock())
            tabs -= 3

        return expr

    def multiplication(self):
        global tokens, pos, lines, tabs

        expr = []
        expr = self.unary()

        while re.match(r"\*|\/|\%", tokens[pos + 1]):
            line = get_line()
            expr.append(" "*get_spaces(line) + line + " "*tabs +"ArithmeticExpr:")
            next_token()
            expr.append(" "*get_spaces(line) + line + " "*tabs +'Operator: ' + re.findall(r"\*|\/|\%",tokens[pos])[0])
            expr.append(self.unary())

        return expr
        
    def addition(self):
        global tokens, pos, lines, tabs

        expr = []

        expr=self.multiplication()

        while re.match(r"\+|\-", tokens[pos + 1]):
            #consume +/-
            next_token()
            line = get_line()
            expr.append(" "*get_spaces(line) + line + " "*tabs +"ArithmeticExpr:")
            expr.append(" "*get_spaces(line) + line + " "*tabs +'Operator: ' + re.findall(r"\+|\-",tokens[pos])[0])
            expr.append(self.multiplication())

        return expr
    
    def relational(self):
        global tokens, pos, lines, tabs
        
        expr = []

        expr=self.addition()

        if re.match(r"\<|\>|T_LessEqual|T_GreaterEqual", tokens[pos + 1]):
            next_token()
            line = get_line()
            expr.append(" "*get_spaces(line) + line + " "*tabs +"RelationalExpr:")
            expr.append(" "*get_spaces(line) + line + " "*tabs +'Operator: ' + lines[pos].split()[0])
            expr.append(self.addition()) 

        return expr

    def equality(self):
        global tokens, pos, lines, tabs
        
        expr = []

        expr = self.relational()
        
        if re.match(r"T_Equal|T_NotEqual", tokens[pos + 1]):
            next_token()            
            line = get_line()
            expr.append(" "*get_spaces(line) + line + " "*tabs +"EqualityExpr:")
            expr.append(" "*get_spaces(line) + line + " "*tabs +'Operator: ' + lines[pos].split()[0])
            expr.append(self.relational())

        return expr
    
    def logicAnd(self):
        global tokens, pos, lines, tabs

        expr = []

        expr = self.equality()
        
        while re.match(r"T_And", tokens[pos + 1]):
            #consume &&
            next_token()
            line = get_line()
            expr.append(" "*get_spaces(line) + line + " "*tabs +"LogicalExpr:")
            expr.append(" "*get_spaces(line) + line + " "*tabs +'Operator: ' + lines[pos].split()[0])
            expr.append(self.equality())     
            
        return expr
    
    def logicOr(self):
        global tokens, pos, lines, tabs
        
        expr = []

        #expr.append(self.logicAnd())
        expr = self.logicAnd()
        while re.match(r"T_Or", tokens[pos + 1]):
            #consume ||
            next_token()
            line = get_line()
            expr.append(" "*get_spaces(line) + line + " "*tabs +"LogicalExpr:")
            expr.append(" "*get_spaces(line) + line + " "*tabs +'Operator: ' + lines[pos].split()[0])
            expr.append(self.logicAnd())          

        return expr

    def assign(self):
        global tokens, pos, lines, tabs
        expr = []
        #consume identifier
        next_token()
        line = get_line()
        expr = [" "*get_spaces(line) + line + " "*tabs +"AssignExpr:"]
        tabs += 3
        expr.append(" "*get_spaces(line) + line + " "*tabs +"FieldAccess:")
        tabs += 3
        expr.append(" "*get_spaces(line) + line + " "*tabs +'Identifier: ' + lines[pos].split()[0])
        tabs -= 3
        expr.append(" "*get_spaces(line) + line + " "*tabs +'Operator: ' + re.findall(r"\=",tokens[pos + 1])[0])        

        #consume =
        next_token()
        expr.append(self.logicOr())
        tabs -= 3
        return expr