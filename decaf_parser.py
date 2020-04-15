import re

lines =[]
tokens = []
pos = -1
tabs = 1


class ProgramNode:

    def __init__(self):
        self.programNode = None
        self.decls = None
        
    def program(self):
        global tokens, pos
        self.programNode = {}
        self.decls = []
        
        if not tokens:
            print("Empty program is syntactically incorrect.")
            return
        else:
            #Keep adding decl to the program
            while (pos + 1) < len(tokens):
                self.decls.append(DeclNode().decl())
        
        self.programNode['Program'] = self.decls

        self.print_data(self.programNode)

        return self.decls

    def load_data(self, lex_dir = ''):
        global lines, tokens
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
            
    def print_data(self, prog):
        print(prog)
        # for k, v in prog.items():
        #     print(k)
        #     if isinstance(v, list):
        #         for item in v:
        #             self.print_data(item)
        #     if isinstance(v, dict):
        #         self.print_data(v)
        #     else:
        #         if not isinstance(v, list):
        #             print(v)

class DeclNode:
    def __init__(self):
        self.fnDecl = None
        self.varDecl = None
        self.variabledecl = None
        self.variablefunct = None

    def decl(self):
        global tokens, pos

        #Check declaration type
        if re.match(r"T_Int|T_Double|T_String|T_Bool|T_Void", tokens[pos + 1]):
            if tokens[pos + 2] == 'T_Identifier':
                if tokens[pos + 3] == '(':
                    #Function declaration
                    self.variablefunct = {}
                    self.variablefunct['line'] = re.findall(r"line \d+",lines[pos + 1])[0].split()[-1]
                    self.variablefunct['FnDecl'] = self.functionDecl()
                    return self.variablefunct
                elif tokens[pos+3] == ';':
                    #Variable declaration
                    self.variabledecl = {}
                    self.variabledecl = self.variableDecl()
                    return self.variabledecl
            else:
                print('reportSyntaxErr(nextNextToken)')
                return
        else:
            print('reportSyntaxErr(nextToken)')
            return

    def functionDecl(self):
        global tokens, pos, lines
        
        pos += 1
        self.fnDecl = {}
        
        #Get line #, type of function, and identifier
        #self.fnDecl['line'] = re.findall(r"line \d+",lines[pos])[0].split()[-1]
        self.fnDecl['(return type) Type'] = re.findall(r"int|double|string|bool|void", lines[pos].split()[0])[0]

        if tokens[pos+1] == 'T_Identifier':
            pos += 1
            self.fnDecl['line'] = re.findall(r"line \d+",lines[pos])[0].split()[-1]
            self.fnDecl['Identifier'] = lines[pos].split()[0]
        else:
            print('reportSyntaxErr(nextToken)')   
            return    

        #Formals
        if tokens[pos + 1] == '(':
            if tokens[pos + 2] != ')':
                self.fnDecl['(formals) VarDecl'] = self.formals()
            else:
                #consume ( and )
                pos += 2
        else:
            print('reportSyntaxErr(nextToken)')
            return
        
        #Statement block
        if tokens[pos + 1] == '{':
            self.fnDecl['(body) StmtBlock'] = StatementNode().stmtBlock()
        else:
            print('reportSyntaxErr(nextToken)')
            return

        return self.fnDecl

    def variableDecl(self):
        global tokens, pos, lines     
        
        var = {}
        var = self.variable()
        
        if tokens[pos + 1] == ';':
            pos += 1
            return var
        else:
            print('reportSyntaxErr(nextToken)')
            return
    
    def variable(self):
        global tokens, pos, lines 

        pos += 1
        var = {}

        #var['line'] = re.findall(r"line \d+",lines[pos])[0].split()[-1]
        var['Type'] = re.findall(r"int|double|string|bool|void", lines[pos].split()[0])[0]

        if tokens[pos+1] == 'T_Identifier':
            pos += 1
            var['Identifier'] = lines[pos].split()[0]
        else:
            print('reportSyntaxErr(nextToken)')   
            return    

        return var
    
    #List of variables seperated by comma
    def formals(self):
        global tokens, pos, lines
        formals = []
        pos += 1

        formals.append(self.variable())        

        while tokens[pos + 1] == ',':
            pos += 1
            formals.append(self.variable()) 
        
        #Consume )
        if tokens[pos + 1] == ')':
            pos += 1   
        else:
            print('reportSyntaxErr(nextToken)')   
            return               

        return formals

class StatementNode:
    def __init__(self):
        self.variablestmt = None
        self.stmtNode = None

    def stmtBlock(self):
        global tokens, pos, lines 
        self.variablestmt = []
        self.stmtNode = {}
        #Consume {
        pos += 1

        if tokens[pos + 1] == '}':
            pos += 1
            return     

        while re.match(r"T_Int|T_Double|T_String|T_Bool|T_Void", tokens[pos + 1]):      
            variabledecl = {}
            variabledecl['VarDecl'] = DeclNode().variableDecl()        

        while tokens[pos + 1] != '}':
            self.variablestmt.append(self.stmt())

        #redundant?
        if tokens[pos+1] == '}':
            pos += 1
        else:
            print('reportSyntaxErr(nextNextToken)')   


        return self.variablestmt
    
    def stmt(self):
        global tokens, pos, lines 

        stmt = {}

        if tokens[pos + 1] == 'T_If':
            print("if")
        elif tokens[pos + 1] == 'T_While':
            print("T_While")
        elif tokens[pos + 1] == 'T_For':
            print("T_For")
        elif tokens[pos + 1] == 'T_Break':
            print("T_Break")
        elif tokens[pos + 1] == 'T_Return':
            pos += 1 
            self.stmtNode['ReturnStmt'] = ExpressionNode().logicOr()
            if tokens[pos + 1] == ';':
                pos += 1
                return self.stmtNode
            else:
                print('reportSyntaxErr(nextNextToken)')
                return
        elif tokens[pos + 1] == 'T_Print':
            pos += 1
            if tokens[pos + 1] == '(':
                self.stmtNode['PrintStmt'] = self.printStmt()
                return self.stmtNode
            else:
                print('reportSyntaxErr(nextNextToken)')
                return
        elif tokens[pos + 1] == '{':
            pos += 1
            stmt = StatementNode()
            self.stmtNode['StmtBlock'] = stmt.stmtBlock()
            return self.stmtNode
        else:
            self.stmtNode = ExpressionNode().expBlock()
            if tokens[pos + 1] == ';':
                pos += 1
                return self.stmtNode
            else:
                print('reportSyntaxErr(nextNextToken)')            
    
    def printStmt(self):
        global tokens, pos, lines 
        #consume (
        pos += 1
        exprs = []

        if tokens[pos + 1] == ')':
            pos += 1
            return exprs
        
        exprs.append(ExpressionNode().expBlock())

        while tokens[pos + 1] == ',':
            pos += 1
            exprs.append(ExpressionNode().expBlock())

        #Consume )
        if tokens[pos + 1] == ')':
            pos += 1
            if tokens[pos + 1] == ';':
                pos += 1
            else:
                print('reportSyntaxErr(nextNextToken)')
        else:
            print('reportSyntaxErr(nextNextToken)')

        return exprs

class ExpressionNode:
    def __init__(self):
        self.expr = None
    
    def expBlock(self):
        global tokens, pos, lines
        
        expr = {} 

        if tokens[pos + 1]:
            if tokens[pos + 1] == 'T_Identifier':
                if tokens[pos + 2] == '=':
                    #consume identifier
                    
                    lval = {}
                    express = {}
                    pos += 1
                    lval['Identifier'] = lines[pos].split()[0]
                    expr['FieldAcess'] = lval

                    expr['Operator'] = re.findall(r"\=",tokens[pos + 1])[0]
                    
                    expr['ArithmeticExpr'] = self.assign()
                    
                    express['AssignExpr'] = expr
                elif tokens[pos + 2] == '(':
                    #consume ident
                    pos += 1
                    expr['Identifier'] = lines[pos].split()[0]
                    expr['Actuals'] = self.actuals()
                else:
                    #consume ident
                    pos += 1
                    expr['Identifier'] = lines[pos].split()[0]
            elif tokens[pos + 1] == '(':
                expr = self.parenthesis()
            elif re.match(r"\-|\!",tokens[pos + 1]):
                expr['unary'] = self.unary()
            elif re.match(r"T_IntConstant|T_DoubleConstant|T_StringConstant|T_BoolConstant", tokens[pos + 1]):
                #consume constant token
                pos += 1
                expr['line'] = re.findall(r"line \d+",lines[pos])[0].split()[-1]
                name = "(args) " + tokens[pos].split('_')[1]
                if tokens[pos] == 'T_StringConstant':
                    expr[name] = '"' + lines[pos].split('"')[1] + '"'
                else:
                    expr[name] = lines[pos].split()[0]
            elif tokens[pos + 1] == 'T_ReadInteger':
                #consume readinteger, (, )
                pos += 3
                expr = {'ReadIntegerExpr'}
        return expr
        
    def parenthesis(self):
        global tokens, pos, lines
        #consume (
        pos += 1 
        expr = {}

        if tokens[pos + 1] == ')':
            #consume )
            pos += 1
            return expr
        else:
            expr = self.logicOr()

        if tokens[pos + 1] == ')':
            pos += 1
        else:
            print('reportSyntaxErr(nextNextToken)')
        
        return expr
    
    def actuals(self):
        global tokens, pos, lines
        actuals = []
        #consume (            
        pos += 1

        if tokens[pos + 1] == ')':
            pos += 1
            return actuals
        
        actuals.append(self.logicOr())

        while tokens[pos + 1] == ',':
            pos += 1
            actuals.append(self.logicOr()) 
        
        #Consume )
        if tokens[pos + 1] == ')':
            pos += 1
        else:
            print('reportSyntaxErr(nextToken)')
            return

        return actuals
    
    def unary(self):
        global tokens, pos, lines
        unary = {}

        if re.match(r"\-|\!",tokens[pos + 1]):
            pos += 1
            unary['Operator'] = tokens[pos]
            pos += 1 
            name = tokens[pos].split('_')[1]
            unary[name] = lines[pos].split()[0]
        else:
            unary = self.expBlock()

        return unary

    def multiplication(self):
        global tokens, pos, lines

        expr = {}
        r_expr = {}

        expr = self.unary()

        while re.match(r"\*|\/|\%", tokens[pos + 1]):
            pos += 1
            expr['Operator1'] = re.findall(r"\*|\/",tokens[pos])[0]
            r_expr['FieldAccess1'] = self.unary()
            expr.update(r_expr)

        return expr
        
    def addition(self):
        global tokens, pos, lines

        expr = {}
        r_expr = {}

        expr= self.multiplication()

        while re.match(r"\+|\-", tokens[pos+1]):
            #consume +/-
            pos += 1
            expr['Operator2'] = re.findall(r"\+|\-",tokens[pos])[0]
            r_expr['FieldAccess2'] = self.multiplication()
            expr.update(r_expr)

        return expr
    
    def relational(self):
        global tokens, pos, lines
        
        expr = {}
        r_expr = {}

        expr = self.addition()

        if re.match(r"\<|\>|T_LessEqual|T_GreaterEqual", tokens[pos + 1]):
            pos += 1
            expr['Operator3'] = lines[pos].split()[0]
            r_expr['FieldAccess3'] = self.addition()
            expr.update(r_expr)

        return expr

    def equality(self):
        global tokens, pos, lines
        
        expr = {}
        r_expr = {}

        expr = self.relational()
        
        if re.match(r"T_Equal|T_NotEqual", tokens[pos + 1]):
            pos += 1
            expr['Operator4'] = lines[pos].split()[0]
            r_expr['FieldAccess4'] = self.relational()
            expr.update(r_expr)

        return expr
    
    def logicAnd(self):
        global tokens, pos, lines

        expr = {}
        r_expr = {}

        expr = self.equality()
        while re.match(r"T_And", tokens[pos+1]):
            #consume &&
            pos += 1
            expr['Operator5'] = lines[pos].split()[0]
            r_expr['FieldAccess5'] = self.equality()
            expr.update(r_expr)

            
        return expr
    
    def logicOr(self):
        global tokens, pos, lines
        
        expr = {}
        r_expr = {}

        expr['FieldAccess'] = self.logicAnd()

        while re.match(r"T_Or", tokens[pos+1]):
            #consume ||
            pos += 1
            expr['Operator6'] = lines[pos].split()[0]
            r_expr['FieldAccess6'] = self.logicAnd()
            expr.update(r_expr)

        return expr

    def assign(self):
        global tokens, pos, lines
        expr = {}

        #consume =
        pos += 1

        expr = self.logicOr()

        return expr
    
