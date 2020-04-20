import re
import sys

lines   = []
tokens  = []
original = []
pos     = -1
tabs    = 1

def error_handle():
    global tokens, pos, lines, tabs

    line_no = get_line()
    token   = lines[pos].split()[0]
    line    = original[int(line_no) - 1]
    print("\n*** Error line " + line_no + ".")
    print(line)
    result = line.find(token) 
    print( " " * (result) + '^'*len(token)) 

    print("*** syntax error\n")
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
    line = re.findall(r"line \d+ ",lines[pos])[0].split()[-1]
    return line

def next_token():
    global tokens, pos
    if pos + 1 <= len(tokens):
        pos += 1
    else:
        error_handle()

def check_next():
    global tokens, pos
    if pos + 1 > len(tokens):
        error_handle()

class ProgramNode:

    def __init__(self):
        self.programNode = ["\n" + " "*3 + 'Program: ']
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
                print(" "*tabs + node)
                tabs += 1

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
                                
                                self.variablefunct = self.functionDecl()
                                
                                return self.variablefunct
                            else:
                                #Variable declaration
                                
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
        
        next_token()

        line = get_line()


        fnDecl = [" "*get_spaces(line) + line + " " + "FnDecl: "]
        #Get line #, type of function, and identifier
        
        
        fnDecl.append(" "*3 + " " + "(return type) Type: " + re.findall(r"int|double|string|bool|void", lines[pos].split()[0])[0])
        
        if tokens[pos + 1] == 'T_Identifier':
            next_token()
            line = get_line()
            fnDecl.append(" "*get_spaces(line) + line + " " + "Identifier: " + lines[pos].split()[0])
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
            fnDecl.append(" "*3 + " " + '(body) StmtBlock: ')
            fnDecl.append(StatementNode().stmtBlock())
        else:
            next_token()
            error_handle()
            
        return fnDecl

    def variableDecl(self):
        global tokens, pos, lines, tabs
        
        var = []
        line = re.findall(r"line \d+ ",lines[pos + 1])[0].split()[-1]
        var.append(" "*get_spaces(line) + line + " " + "VarDecl: ")

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
        
        var.append(" "*3 + " " + "Type: " + re.findall(r"int|double|string|bool|void", lines[pos].split()[0])[0])

        if tokens[pos + 1] == 'T_Identifier':
            next_token()
            line = get_line()
            var.append(" "*get_spaces(line) + line + " " + "Identifier: " + lines[pos].split()[0]) 
        else:
            next_token() 
            error_handle()
        
           
        return var
    
    #List of variables seperated by comma
    def formals(self):
        global tokens, pos, lines, tabs
        formals = []
        next_token()
        line = get_line()
        formals.append(" "*get_spaces(line) + line + " " + '(formals) VarDecl: ')

        formals.append(self.variable())

        while tokens[pos + 1] == ',':
            next_token()
            line = get_line()
            formals.append(" "*get_spaces(line) + line + " " + '(formals) VarDecl: ')
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
         
        return self.stmts
    
    def stmt(self):
        global tokens, pos, lines, tabs

        stmt = []

        if tokens[pos + 1] == 'T_If':
            stmt.append(" "*3 + " " + 'IfStmt: ')
            stmt.append(self.ifStmt())
        elif tokens[pos + 1] == 'T_While':
            stmt.append(" "*3 + " " + 'WhileStmt: ')
            stmt.append(self.whileStmt())
        elif tokens[pos + 1] == 'T_For':
            stmt.append(" "*3 + " " + 'ForStmt: ')
            stmt.append(self.forStmt())
        elif tokens[pos + 1] == 'T_Break':
            next_token()
            stmt.append(" "*3 + " " + 'BreakStmt: ')
            if tokens[pos + 1] == ';':
                next_token()
            else:
                next_token()
                error_handle()
        elif tokens[pos + 1] == 'T_Return':
            next_token() 
            line = get_line()
            stmt.append(" "*get_spaces(line) + line + " " + 'ReturnStmt: ')
            if tokens[pos + 1] == ';':
                stmt.append(" "*3 + " " + 'Empty: ')
            else:
                stmt.append(ExpressionNode().logicOr())
            if tokens[pos + 1] == ';':
                next_token()
            else:
                next_token()
                error_handle()
        elif tokens[pos + 1] == 'T_Print':
            #consume print token
            next_token()
            if tokens[pos + 1] == '(':
                stmt.append(" "*3 + " " + 'PrintStmt: ')
                stmt.append(self.printStmt())
            else:
                next_token()
                error_handle()
        elif tokens[pos + 1] == '{':
            stmt.append(" "*3 + " " + '(body) StmtBlock: ')
            
            stmt.append(StatementNode().stmtBlock())
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
        line = get_line()

        if "Identifier" in x[0]:
            exprs.append(" "*get_spaces(line) + line + " " + "(args) FieldAccess: ")
            exprs.append(x)
        elif "StringConstant" in x[0]:
            x[0] = " "*get_spaces(line) + line + " (args) " + x[0]
            exprs.extend(x)           
        else:
            x[0] = " "*get_spaces(line) + line + " (args) " + x[0].split()[-1]
            exprs.extend(x)

        # Expressions inside Print(), continue if ,
        while tokens[pos + 1] == ',':
            next_token()
            x = ExpressionNode().expBlock()
            line = get_line()

            if "Identifier" in x[0]:
                exprs.append(" "*get_spaces(line) + line + " " + "(args) FieldAccess: ")
                exprs.append(x)
            elif "StringConstant" in x[0]:
                x[0] = " "*get_spaces(line) + line + " (args) " + x[0]
                exprs.extend(x)                        
            else:
                x[0] = " "*get_spaces(line) + line + " (args) " + x[0]
                exprs.extend(x)

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
            x = ExpressionNode().logicOr()
            line = get_line()
            x[0] = " "*get_spaces(line) + line + " " + "(test) " + x[0].split()[-1]
            stmt.append(x)

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
        line = get_line()
        if "Identifier" in x[0]:
            stmt.append(" "*get_spaces(line) + line + " " + "(then) FieldAccess: ")
            stmt.append(x)
        else:
            x[0] = " "*get_spaces(line) + line + " (then) " + x[0].split()[-1]
            stmt.extend(x)

        while tokens[pos + 1] == 'T_Else':
            next_token()
            x = self.stmt()
            line = get_line()
            if "Identifier" in x[0]:
                stmt.append(" "*get_spaces(line) + line + " " + "(else) FieldAccess: ")
                stmt.append(x)
            else:
                x[0] = " "*get_spaces(line) + line + " (else) " + x[0].split()[-1]
                stmt.extend(x)

        return stmt

    def whileStmt(self):
        global tokens, lines, pos, tabs
        stmt = []
        #consume while token
        next_token()

        if tokens[pos + 1] == '(':
            #consume (
            next_token()
            line = get_line()
            x = ExpressionNode().logicOr()
            x[0] = " "*get_spaces(line) + line + " " + "(test) " + x[0].split()[-1]
            stmt.append(x)
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
        stmt.extend(x)

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
                line = get_line()
                stmt.append(" "*3 + " " + "(init) Empty: ")
                next_token()
            else:
                x = ExpressionNode().logicOr()
                line = get_line()
                x[0] = " "*get_spaces(line) + line + " " + "(init) " + x[0].split()[-1]
                stmt.append(x)
                             
            #second expression is enforced
            x = ExpressionNode().logicOr()
            line = get_line()
            x[0] = " "*get_spaces(line) + line + " " + "(test) " + x[0].split()[-1]
            stmt.append(x)

            #enforce ; after expression
            if tokens[pos + 1] == ';':
                next_token()
            else:
                next_token()
                error_handle()

            #third expression is optional
            if tokens[pos + 1] == ';':
                line = get_line()
                stmt.append(" "*get_spaces(line) + line + " " + "(step) Empty: ")
                next_token()
            else:
                x = ExpressionNode().logicOr()
                line = get_line()
                x[0] = " "*get_spaces(line) + line + " " + "(step) " + x[0].split()[-1]
                stmt.append(x)
            
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
        stmt.extend(x)

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
                    expr.append(" "*get_spaces(line) + line + " " + 'Call: ')
                    expr.append(" "*get_spaces(line) + line + " " + 'Identifier: ' + lines[pos].split()[0])
                    expr.append(self.actuals())
                else:
                    #consume ident
                    next_token()
                    line = get_line()
                    expr.append(" "*get_spaces(line) + line + " " + 'Identifier: ' + lines[pos].split()[0])
            elif tokens[pos + 1] == '(':
                expr.append(self.parenthesis())
            elif re.match(r"\-|\!",tokens[pos + 1]):
                expr.append('Unary: ')
                expr.append(self.unary())
            elif re.match(r"T_IntConstant|T_DoubleConstant|T_StringConstant|T_BoolConstant", tokens[pos + 1]):
                #consume constant token
                next_token()
                line = get_line()
                name = tokens[pos].split('_')[1]

                if tokens[pos] == 'T_StringConstant':
                    value = name + ': ' + '"' + lines[pos].split('"')[1] + '"'
                    expr.append(value)
                elif tokens[pos] == 'T_DoubleConstant':
                    value = name + ": " + lines[pos].split()[0]
                    if (float(value.split()[-1])).is_integer():
                        new_int = int(float(value.split()[-1]))
                        value = value.split()[0] + " " + str(new_int)
                    expr.append(value)
                else:
                    value = name + ": " + lines[pos].split()[0]
                    expr.append(value)
            elif tokens[pos + 1] == 'T_ReadInteger':
                #consume readinteger, (, )
                line = get_line()
                pos += 3
                expr.append(" "*get_spaces(line) + line + " " + 'ReadIntegerExpr: ')
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
        line = get_line()
        x[0] = " "*get_spaces(line) + line + " " + "(actuals) " + x[0].split()[-1]
        
        actuals.append(x)

        while tokens[pos + 1] == ',':
            next_token()
            x = self.logicOr()
            line = get_line()
            x[0] = " "*get_spaces(line) + line + " " + "(actuals) " + x[0].split()[-1]
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
            x = [" "*get_spaces(line) + line + " " + "LogicalExpr: "]
            expr.append(" "*get_spaces(line) + line + " " + 'Operator: ' + tokens[pos])
            y = self.expBlock()
            if "Identifier" in y[0]: 
                expr.append(" "*get_spaces(line) + line + " " + "FieldAccess: ")
                expr.extend(y)
            elif "Constant" in y[0]:
                y[0] = " "*get_spaces(line) + line + " " + y[0]
                expr.extend(y)
            else:
                expr.extend(y)
            expr = x + expr
        else:
            line = get_line()
            x = self.expBlock()
            if "Identifier" in x[0]: 
                expr.append(" "*get_spaces(line) + line + " " + "FieldAccess: ")
                expr.extend(x)
            elif "Constant" in x[0]:
                x[0] = " "*get_spaces(line) + line + " " + x[0]
                expr.extend(x)
            else:
                expr.extend(x)

        return expr

    def multiplication(self):
        global tokens, pos, lines, tabs

        expr = []
        expr = self.unary()

        while re.match(r"\*|\/|\%", tokens[pos + 1]):
            line = get_line()
            x = [" "*get_spaces(line) + line + " " + "ArithmeticExpr: "]
            next_token()
            expr.append(" "*get_spaces(line) + line + " " + 'Operator: ' + re.findall(r"\*|\/|\%",tokens[pos])[0])
            expr.extend(self.unary())
            expr = x + expr

        return expr
        
    def addition(self):
        global tokens, pos, lines, tabs

        expr = []
        expr = self.multiplication()

        while re.match(r"\+|\-", tokens[pos + 1]):
            #consume +/-
            next_token()
            line = get_line()
            x = [" "*get_spaces(line) + line + " " + "ArithmeticExpr: "]
            expr.append(" "*get_spaces(line) + line + " " + 'Operator: ' + re.findall(r"\+|\-",tokens[pos])[0])
            expr.extend(self.multiplication())

            expr = x + expr

        return expr
    
    def relational(self):
        global tokens, pos, lines, tabs
        
        #expr = []
        expr = self.addition()

        if re.match(r"\<|\>|T_LessEqual|T_GreaterEqual", tokens[pos + 1]):
            next_token()
            line = get_line()
            x = [" "*get_spaces(line) + line + " " + "RelationalExpr: "]
            expr.append(" "*get_spaces(line) + line + " " + 'Operator: ' + lines[pos].split()[0])
            expr.extend(self.addition()) 
            expr = x + expr

        return expr

    def equality(self):
        global tokens, pos, lines, tabs
        
        #expr = []
        expr = self.relational()
        
        if re.match(r"T_Equal|T_NotEqual", tokens[pos + 1]):
            next_token()
            line = get_line()
            x = [" "*get_spaces(line) + line + " " + "EqualityExpr: "]
            expr.append(" "*get_spaces(line) + line + " " + 'Operator: ' + lines[pos].split()[0])
            expr.extend(self.relational())
            expr = x + expr

        return expr
    
    def logicAnd(self):
        global tokens, pos, lines, tabs

        #expr = []
        expr = self.equality()
        
        while re.match(r"T_And", tokens[pos + 1]):
            #consume &&
            next_token()
            line = get_line()
            x = [" "*get_spaces(line) + line + " " + "LogicalExpr: "]
            expr.append(" "*get_spaces(line) + line + " " + 'Operator: ' + lines[pos].split()[0])
            expr.extend(self.equality())
            expr = x + expr
            
        return expr
    
    def logicOr(self):
        global tokens, pos, lines, tabs
        
        #expr = []
        expr = self.logicAnd()

        while re.match(r"T_Or", tokens[pos + 1]):
            #consume ||
            next_token()
            line = get_line()
            x = [" "*get_spaces(line) + line + " " + "LogicalExpr: "]
            expr.append(" "*get_spaces(line) + line + " " + 'Operator: ' + lines[pos].split()[0])
            expr.extend(self.logicAnd())
            expr = x + expr

        return expr

    def assign(self):
        global tokens, pos, lines, tabs
        expr = []

        #consume identifier
        next_token()
        line = get_line()
        expr = [" "*get_spaces(line) + line + " " + "AssignExpr: "]
        
        expr.append(" "*get_spaces(line) + line + " " + "FieldAccess: ")
        expr.append(" "*get_spaces(line) + line + " " + 'Identifier: ' + lines[pos].split()[0])
        expr.append(" "*get_spaces(line) + line + " " + 'Operator: ' + re.findall(r"\=",tokens[pos + 1])[0])

        #consume =
        next_token()
        expr.extend(self.logicOr())
        
        return expr