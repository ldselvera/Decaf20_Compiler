import re
import sys

lines   = []
tokens  = []
original = []
pos     = -1
tabs    = 0

def error_handle():        
    global tokens, pos, lines, tabs

    line_no = re.findall(r"line \d+",lines[pos])[0].split()[-1]
    token   = lines[pos].split()[0]
    line    = original[int(line_no) - 1]
    print("\n*** Error line " + line_no + ".")
    print(line)
    result = line.find(token) 
    print( " " * (result) + '^'*len(token)) 

    print("*** syntax error\n\n")
    sys.exit()

class ProgramNode:

    def __init__(self):
        self.programNode = ["\n"+" "*tabs + 'Program:']
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
                tabs = 3
        
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
                                tabs = 0
                                self.variablefunct = self.functionDecl()
                                return self.variablefunct
                            else:
                                #Variable declaration
                                tabs = 0
                                self.variabledecl = self.variableDecl()
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
        
        pos += 1
        tabs += 3

        line = re.findall(r"line \d+",lines[pos])[0].split()[-1]

        fnDecl = ["  " + line + " "*tabs + "FnDecl:"]
        #Get line #, type of function, and identifier
        tabs += 3
        fnDecl.append(" "*3 + " "*tabs + "(return type) Type: " + re.findall(r"int|double|string|bool|void", lines[pos].split()[0])[0])
        
        if tokens[pos + 1] == 'T_Identifier':
            pos += 1
            line = re.findall(r"line \d+",lines[pos])[0].split()[-1]
            fnDecl.append("  " + line + " "*tabs +"Identifier: " + lines[pos].split()[0])
        else:
            pos += 1
            error_handle()               

        #Formals
        if tokens[pos + 1] == '(':
            if tokens[pos + 2] != ')':
                fnDecl.append(self.formals())
            else:
                #consume ( and )
                pos += 2
        else:
            pos += 1
            error_handle()
            
        #Statement block
        if tokens[pos + 1] == '{':
            tabs += 3
            fnDecl.append(" "*3 + " "*tabs +'(body) StmtBlock:')
            fnDecl.append(StatementNode().stmtBlock())
        else:
            pos += 1
            error_handle()
            
        return fnDecl

    def variableDecl(self):
        global tokens, pos, lines, tabs     
        
        var = []
        tabs += 3
        line = re.findall(r"line \d+",lines[pos + 1])[0].split()[-1]
        var.append("  "+ line + " "*tabs + "VarDecl:")
        var.append(self.variable())

        if tokens[pos + 1] == ';':
            pos += 1
            tabs -= 6
            return var
        else:
            pos += 1
            error_handle()
            
    
    def variable(self):
        global tokens, pos, lines, tabs

        pos += 1
        var = []
        tabs += 3
        var.append(" "*3 + " "*tabs +"Type: " + re.findall(r"int|double|string|bool|void", lines[pos].split()[0])[0])

        if tokens[pos + 1] == 'T_Identifier':
            pos += 1
            line = re.findall(r"line \d+",lines[pos])[0].split()[-1]
            var.append("  " + line + " "*tabs +"Identifier: " + lines[pos].split()[0]) 
        else:
            pos += 1 
            error_handle()
                
        return var
    
    #List of variables seperated by comma
    def formals(self):
        global tokens, pos, lines, tabs
        formals = []
        pos += 1
        line = re.findall(r"line \d+",lines[pos])[0].split()[-1]
        formals.append("  " + line + " "*tabs +'(formals) VarDecl:')
        formals.append(self.variable())
        tabs -= 6        

        while tokens[pos + 1] == ',':
            pos += 1
            line = re.findall(r"line \d+",lines[pos])[0].split()[-1]
            formals.append("  " + line + " "*tabs +'(formals) VarDecl:')
            formals.append(self.variable()) 
        
        #Consume )
        if tokens[pos + 1] == ')':
            pos += 1   
        else:
            pos += 1
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
        pos += 1 

        if tokens[pos + 1] == '}':
            pos += 1
            return     

        while re.match(r"T_Int|T_Double|T_String|T_Bool|T_Void", tokens[pos + 1]):      
            self.variabledecl.append(DeclNode().variableDecl())

        while tokens[pos + 1] != '}': 
            self.variablestmt.append(self.stmt())

        #redundant?
        if tokens[pos + 1] == '}':
            pos += 1
        else:
            pos += 1
            error_handle()

        self.stmts.append(self.variabledecl)
        self.stmts.append(self.variablestmt)   
  
        return self.stmts
    
    def stmt(self):
        global tokens, pos, lines, tabs

        stmt = []

        if tokens[pos + 1] == 'T_If':
            stmt.append('ifStmt:')
            stmt.append(self.ifStmt())
            return stmt
        elif tokens[pos + 1] == 'T_While':
            stmt.append('WhileStmt:')
            stmt.append(self.whileStmt())     
            return stmt
        elif tokens[pos + 1] == 'T_For':
            stmt.append('ForStmt:')
            stmt.append(self.forStmt())     
            return stmt
        elif tokens[pos + 1] == 'T_Break':
            pos += 1  
            stmt.append('BreakStmt:')
            if tokens[pos + 1] == ';':
                pos += 1              
                return stmt
            else:
                pos += 1
                error_handle()
        elif tokens[pos + 1] == 'T_Return':
            pos += 1 
            line = re.findall(r"line \d+",lines[pos])[0].split()[-1]
            tabs += 3
            stmt.append("  " + line + " "*tabs +'ReturnStmt:')
            if tokens[pos + 1] == ';':
                stmt.append('Empty:')
                pos += 1              
                return stmt
            else:
                stmt.append(ExpressionNode().logicOr())      
            if tokens[pos + 1] == ';':
                pos += 1
                return stmt
            else:
                pos += 1
                error_handle()
        elif tokens[pos + 1] == 'T_Print':
            #consume print token
            pos += 1
            if tokens[pos + 1] == '(':
                tabs += 3
                stmt.append(" "*3 + " "*tabs + 'PrintStmt:')
                stmt.append(self.printStmt())                
                return stmt
            else:
                pos += 1
                error_handle()
        elif tokens[pos + 1] == '{':
            stmt.append('StmtBlock:')
            stmt.append(StatementNode().stmtBlock())              
            return stmt
        else:
            stmt = ExpressionNode().expBlock()
            
            if tokens[pos + 1] == ';':
                pos += 1
                return stmt
            else:
                pos += 2
                error_handle()
                

    def printStmt(self):
        global tokens, pos, lines, tabs 
        #consume (
        pos += 1
        exprs = []

        if tokens[pos + 1] == ')':
            pos += 1
            return 
        #"(args) " + 
        x = ExpressionNode().expBlock()

        tabs += 3
        line = re.findall(r"line \d+",lines[pos])[0].split()[-1]
        x[0] = "  " + line + " "*tabs +"(args) " + x[0]
        exprs.append(x)

        while tokens[pos + 1] == ',':
            pos += 1
            x = ExpressionNode().expBlock()
            x[0] = "(args) " + x[0]
            exprs.append(x)

        #Consume )
        if tokens[pos + 1] == ')':
            pos += 1
            if tokens[pos + 1] == ';':
                pos += 1
            else:
                pos += 1
                error_handle()
        else:
            pos += 1
            error_handle()
            
        return exprs

    def ifStmt(self):
        global tokens, lines, pos, tabs

        #consume if token
        pos += 1

        stmt = []

        if tokens[pos + 1] == '(':
            #consume (
            pos += 1

            stmt.append(ExpressionNode().logicOr())
            if tokens[pos + 1] == ')':
                #consume )
                pos += 1
            else:
                pos += 1
                error_handle()
        else:
            pos += 1
            error_handle()
            
        x = self.stmt() 
        x[0] = "(then) " + x[0]
        stmt.append(x)

        while tokens[pos + 1] == 'T_Else':
            pos += 1
            x = self.stmt() 
            x[0] = "(then) " + x[0]
            stmt.append(x)

        return stmt

    def whileStmt(self):
        global tokens, lines, pos, tabs
        stmt = []
        #consume while token
        pos += 1

        if tokens[pos + 1] == '(':
            #consume (
            pos += 1
            stmt.append(ExpressionNode().logicOr())
            if tokens[pos + 1] == ')':
                #consume )
                pos += 1
            else:
                pos += 1
                error_handle()              
        else:
            pos += 1
            error_handle()           

        stmt.append(self.stmt())

        return stmt

    def forStmt(self):
        global tokens, lines, pos, tabs
        stmt = []
        #consume for token
        pos += 1

        if tokens[pos + 1] == '(':
            #consume (
            pos += 1
          
            #first expression may be empty
            if tokens[pos + 1] == ';':
                stmt.append("(init) Empty:")
                pos += 1
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
                pos += 1
            else:
                pos += 1
                error_handle()
                

            #third expression is optional
            if tokens[pos + 1] == ';':
                stmt.append("(step) Empty:")
                pos += 1
            else:
                x = ExpressionNode().logicOr()
                x[0] = "(step) " + x[0]
                stmt.append(x)
                #stmt.append(ExpressionNode().logicOr())            
            
            if tokens[pos + 1] == ')':
                #consume )
                pos += 1
            else:
                pos += 1
                error_handle()
        else:
            pos += 1
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
                    pos += 1
                    line = re.findall(r"line \d+",lines[pos])[0].split()[-1]
                    expr.append('Call:')
                    expr.append("  " + line + " "*tabs +'Identifier: ' + lines[pos].split()[0])
                    tabs -= 3
                    expr.append(self.actuals())
                else:
                    #consume ident
                    pos += 1
                    line = re.findall(r"line \d+",lines[pos])[0].split()[-1]
                    expr.append("  " + line + " "*tabs +"FieldAccess:")
                    tabs += 3
                    expr.append("  " + line + " "*tabs +'Identifier: ' + lines[pos].split()[0])                    
                    tabs -= 3
            elif tokens[pos + 1] == '(':
                expr.append(self.parenthesis())
            elif re.match(r"\-|\!",tokens[pos + 1]):
                expr.append('Unary:')
                expr.append(self.unary())
            elif re.match(r"T_IntConstant|T_DoubleConstant|T_StringConstant|T_BoolConstant", tokens[pos + 1]):
                #consume constant token
                pos += 1
                line = re.findall(r"line \d+",lines[pos])[0].split()[-1]
                name = tokens[pos].split('_')[1]
                if tokens[pos] == 'T_StringConstant':
                    value = name + ': ' + '"' + lines[pos].split('"')[1] + '"'
                    expr.append("  " + line + " "*tabs + value)
                    #expr.append(' : "' + lines[pos].split('"')[1] + '"')
                else:
                    value = name + ": " + lines[pos].split()[0]
                    expr.append("  " + line + " "*tabs + value)
                    #expr[name] = lines[pos].split()[0]
            elif tokens[pos + 1] == 'T_ReadInteger':
                #consume readinteger, (, )
                pos += 3
                expr.append('ReadIntegerExpr:')
            else:
                pos += 1
                error_handle()
        return expr
        
    def parenthesis(self):
        global tokens, pos, lines, tabs
        #consume (
        pos += 1 
        expr = []

        if tokens[pos + 1] == ')':
            #consume )
            pos += 1
            return 
        else:
            expr = self.logicOr()

        if tokens[pos + 1] == ')':
            pos += 1
        else:
            pos += 1
            error_handle()
            
        
        return expr
    
    def actuals(self):
        global tokens, pos, lines, tabs
        actuals = []
        #consume (
        pos += 1

        if tokens[pos + 1] == ')':
            pos += 1
            return 

        x = self.logicOr()
        x[0] = "(actuals) " + x[0]
        actuals.append(x)

        while tokens[pos + 1] == ',':
            pos += 1
            x = self.logicOr()
            x[0] = "  " + line + " "*tabs + "(actuals) " + x[0]
            actuals.append(x)
        
        #Consume )
        if tokens[pos + 1] == ')':
            pos += 1
        else:
            pos += 1
            error_handle()
            
        return actuals
    
    def unary(self):
        global tokens, pos, lines, tabs
        expr = []

        if re.match(r"\-|\!",tokens[pos + 1]):
            pos += 1
            line = re.findall(r"line \d+",lines[pos])[0].split()[-1]
            expr.append("  " + line + " "*tabs +'Operator: ' + tokens[pos])
            pos += 1 
            name = tokens[pos].split('_')[1]
            expr.append(name + ": " + lines[pos].split()[0])
        else:
            expr = self.expBlock()

        return expr

    def multiplication(self):
        global tokens, pos, lines, tabs

        expr = []

        expr = self.unary()

        while re.match(r"\*|\/|\%", tokens[pos + 1]):
            line = re.findall(r"line \d+",lines[pos])[0].split()[-1]
            tabs += 3
            expr.append("  " + line + " "*tabs +"ArithmeticExpr:")
            pos += 1
            expr.append("  " + line + " "*tabs +'Operator: ' + re.findall(r"\*|\/|\%",tokens[pos])[0])
            expr.append(self.unary())

        return expr
        
    def addition(self):
        global tokens, pos, lines, tabs

        expr = []

        expr=self.multiplication()

        while re.match(r"\+|\-", tokens[pos + 1]):
            #consume +/-
            pos += 1
            line = re.findall(r"line \d+",lines[pos])[0].split()[-1]
            tabs += 3
            expr.append("  " + line + " "*tabs +"ArithmeticExpr:")
            expr.append("  " + line + " "*tabs +'Operator: ' + re.findall(r"\+|\-",tokens[pos])[0])
            expr.append(self.multiplication())

        return expr
    
    def relational(self):
        global tokens, pos, lines, tabs
        
        expr = []

        expr=self.addition()

        if re.match(r"\<|\>|T_LessEqual|T_GreaterEqual", tokens[pos + 1]):
            pos += 1
            line = re.findall(r"line \d+",lines[pos])[0].split()[-1]
            tabs += 3
            expr.append("  " + line + " "*tabs +"RelationalExpr:")
            expr.append("  " + line + " "*tabs +'Operator: ' + lines[pos].split()[0])
            expr.append(self.addition()) 

        return expr

    def equality(self):
        global tokens, pos, lines, tabs
        
        expr = []

        expr = self.relational()
        
        if re.match(r"T_Equal|T_NotEqual", tokens[pos + 1]):
            pos += 1            
            line = re.findall(r"line \d+",lines[pos])[0].split()[-1]
            tabs += 3
            expr.append("  " + line + " "*tabs +"EqualityExpr:")
            expr.append("  " + line + " "*tabs +'Operator: ' + lines[pos].split()[0])
            expr.append(self.relational())

        return expr
    
    def logicAnd(self):
        global tokens, pos, lines, tabs

        expr = []

        expr = self.equality()
        
        while re.match(r"T_And", tokens[pos + 1]):
            #consume &&
            pos += 1
            line = re.findall(r"line \d+",lines[pos])[0].split()[-1]
            tabs += 3
            expr.append("  " + line + " "*tabs +"LogicalExpr:")
            expr.append("  " + line + " "*tabs +'Operator: ' + lines[pos].split()[0])
            expr.append(self.equality())     
            
        return expr
    
    def logicOr(self):
        global tokens, pos, lines, tabs
        
        expr = []

        #expr.append(self.logicAnd())
        expr = self.logicAnd()
        while re.match(r"T_Or", tokens[pos + 1]):
            #consume ||
            pos += 1
            line = re.findall(r"line \d+",lines[pos])[0].split()[-1]
            tabs += 3
            expr.append("  " + line + " "*tabs +"LogicalExpr:")
            expr.append("  " + line + " "*tabs +'Operator: ' + lines[pos].split()[0])
            expr.append(self.logicAnd())            

        return expr

    def assign(self):
        global tokens, pos, lines, tabs
        expr = []
        #consume identifier
        pos += 1
        line = re.findall(r"line \d+",lines[pos])[0].split()[-1]
        expr = ["  " + line + " "*tabs +"AssignExpr:"]
        expr.append("  " + line + " "*tabs +"FieldAccess:")
        tabs += 3
        expr.append("  " + line + " "*tabs +'Identifier: ' + lines[pos].split()[0])
        tabs -= 3
        expr.append("  " + line + " "*tabs +'Operator: ' + re.findall(r"\=",tokens[pos + 1])[0])        

        #consume =
        pos += 1
        expr.append(self.logicOr())

        return expr