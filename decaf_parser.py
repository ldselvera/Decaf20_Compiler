import re

lines =[]
tokens = []
pos = -1
tabs = 1


class ProgramNode:

    def __init__(self):
        self.decls = None
        
    def check(self):
        global tokens
        print(tokens)
        
    def program(self):
        global tokens, pos
        self.decls = []
        
        if not tokens:
            print("Empty program is syntactically incorrect.")
            return
        else:
            #Keep adding decl to the program
            while (pos + 1) < len(tokens):
                declNode = DeclNode()
                self.decls.append(declNode.decl())                                                

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
    
    
class DeclNode:
    def __init__(self):
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
        funct = {}
        
        pos += 1
        
        #Get line #, type of function, and identifier
        funct['line'] = re.findall(r"line \d+",lines[pos])[0].split()[-1]
        funct['Type'] = re.findall(r"int|double|string|bool|void", lines[pos].split()[0])[0]
        pos += 1
        funct['Identifier'] = lines[pos].split()[0]
        
        #Formals
        if tokens[pos + 1] == '(':
            funct['Formals VarDecl'] = self.formals()
        else:
            print('reportSyntaxErr(nextToken)')
            return
         
        #Statement block
        if tokens[pos + 1] == '{':
            funct['StmtBlock'] = StatementNode().stmtBlock()
        else:
            print('reportSyntaxErr(nextToken)')
            return

        return funct

    def variableDecl(self):
        global tokens, pos, lines     
        
        var = {}
        var['VarDecl'] = self.variable()
        
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

        var['line'] = re.findall(r"line \d+",lines[pos])[0].split()[-1]
        var['Type'] = re.findall(r"int|double|string|bool|void", lines[pos].split()[0])[0]
        pos += 1
        var['Identifier'] = lines[pos].split()[0]

        return var
    
    #List of variables seperated by comma
    def formals(self):
        global tokens, pos, lines
        formals = []
        pos += 1

        if tokens[pos + 1] == ')':
            return formals
        
        formals.append(self.variable())        
        
        while tokens[pos + 1] == ',':
            formals.append(self.variable()) 
        
        #Consume )
        pos += 1         

        return formals

class StatementNode:
    def __init__(self):
        self.variablestmt = None

    def stmtBlock(self):
        global tokens, pos, lines 
        self.variablestmt = []

        #Consume {
        pos += 1
       
        while re.match(r"T_Int|T_Double|T_String|T_Bool|T_Void", tokens[pos + 1]):      
            
            variabledecl = {}
            variabledecl['VarDecl'] = DeclNode().variableDecl()

            if tokens[pos + 1] == ';':
                pos += 1                
                self.variablestmt.append(variabledecl)
                pos += 1
            else:
                print('reportSyntaxErr(nextNextToken)')
                return

        while tokens[pos + 1] != '}':  
            self.variablestmt.append(self.stmt())
            pos += 1         

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
            exprNode = ExpressionNode()
            stmt['ReturnStmt'] = exprNode.expBlock()       
            if tokens[pos + 1] == ';':
                pos += 1
                return stmt
            else:
                print('reportSyntaxErr(nextNextToken)')
                return
        elif tokens[pos + 1] == 'T_Print':
            pos += 1
            if tokens[pos] == '(':
                pos += 1
                stmt['PrintStmt'] = self.printStmt()
                pos += 1
        
                if tokens[pos] == ';':
                    return stmt
                else:
                    print('reportSyntaxErr(nextNextToken)')
                    return
            else:
                print('reportSyntaxErr(nextNextToken)')
                return
        elif tokens[pos + 1] == '{':
            pos += 1
            stmtNode = StatementNode()
            stmt['StmtBlock'] = stmtNode.stmtBlock()
            return stmt
        else:
            exprNode = ExpressionNode()
            stmt = exprNode.expBlock()
            return stmt
    
    def printStmt(self):
        global tokens, pos, lines 
        
        exprs = []
        while tokens[pos] != ')':
            exprNode = ExpressionNode()
            exprs.append(exprNode.expBlock())
            pos += 1
        
        return exprs
    
class ExpressionNode:
    def __init__(self):
        self.expr = None
    
    def expBlock(self):
        global tokens, pos, lines             
        
        expr = {} 

        
        if tokens[pos + 1]:
            if tokens[pos + 1] == '(':  
                expr = self.parenthesis()
            elif re.match(r"\*|\/|\%",tokens[pos + 2]):
                expr['ArithmeticExpr'] = self.multiplication()
            elif re.match(r"\+|\-",tokens[pos + 2]):                
                print("going to add",lines[pos])
                print(lines[pos+1])
                expr['ArithmeticExpr'] = self.addition()
            elif re.match(r"\<|\>|T_LessEqual|T_GreaterEqual", tokens[pos + 2]):
                expr['Relational'] = self.relational()
            elif re.match(r"T_Equal|T_NotEqual", tokens[pos + 2]):
                expr['EqualityExpr'] = self.equality()
            elif tokens[pos + 2] == 'T_And':
                expr['LogicalExpr'] = self.logicAnd()
            elif tokens[pos + 2] == 'T_Or':
                expr['Comparison'] = self.logicOr()
            elif tokens[pos + 2] == '=':
                expr['AssignExpr'] = self.assign()        
            elif tokens[pos + 1] == 'T_Identifier':
                if tokens[pos + 2] == '(':
                    call = {}
                    calls = []
                    call['Identifier'] = lines[pos+1].split()[0]
                    pos += 1
                    calls.append(call)
                    calls.append( self.call())
                    expr['Call'] = calls
                else:
                    expr['LValue'] = lines[pos + 1].split()[0]
            elif re.match(r"\-|\!",tokens[pos + 1]):
                expr['Urinary'] = self.urinary()
            elif re.match(r"T_IntConstant|T_DoubleConstant|T_StringConstant|T_StringConstant|T_BoolConstant", tokens[pos + 1]):
                name = tokens[pos].split('_')[1]
                if tokens[pos + 1] == 'T_StringConstant':
                    expr[name] = '"' + lines[pos].split('"')[1] + '"'
                else:
                    expr[name] = lines[pos].split()[0]
        return expr
        
    def parenthesis(self):
        global tokens, pos, lines
        #consume (
        pos += 1 
        
        expr = {}
        
        if tokens[pos + 1] == ')':
            return expr
        else:
            expr = self.expBlock()

        if tokens[pos + 1] == ')':
            pos += 1
        else:
            print('reportSyntaxErr(nextNextToken)')
        
        return expr
        
    def call(self):
        global tokens, pos, lines 
        exprs = []
        
        while tokens[pos] != ')':
            exprNode = ExpressionNode()
            exprs.append(exprNode.expBlock())
            if tokens[pos] == ',':
                pos += 1
            elif tokens[pos] == ')':
                continue
            
        return exprs
    
    def urinary(self):
        global tokens, pos, lines        
        urinary = {}
        
        if re.match(r"\-|\!",tokens[pos + 1]):
            urinary['Operator'] = tokens[pos]
            pos += 1 
            urinary['Identifier'] = lines[pos].split()[0]
            pos += 1
        else:
            pos += 1
            urinary['Identifier'] = lines[pos].split()[0]

        return urinary

    def multiplication(self):
        global tokens, pos, lines

        mult = {}
        fields = []
        idents = []
        
        
        mult = self.urinary()
        pos += 1
        
        while re.match(r"\*|\/|\%", tokens[pos + 2]):
            mult['Operator'] = re.findall(r"\*|\/|\%",tokens[pos])
            pos += 1
            mult['Identifier'] = lines[pos].split()[0]
            fields.append(mult['Identifier'])
            mult['FieldAccess'] = fields
            pos += 1
            
        return mult        
        
    def addition(self):
        global tokens, pos, lines        
        add = {}
        fields = []
        idents = []   

        print("inside to add",lines[pos])
        print(lines[pos+1])
        expr = self.multiplication()
        pos += 1
        
        while re.match(r"\+|\-", tokens[pos+1]):
            add['Operator'] = re.findall(r"\+|\-",tokens[pos])
            pos += 1
            expr = ExpressionNode()
            r_expr = expr.expBlock()       
            pos += 1
            fields.append(l_expr)
            fields.append(r_expr)
            add['FieldAccess'] = fields
            pos += 1
            
        return add
    
    def relational(self):
        global tokens, pos, lines
        
        relational = {}
        fields = []
        idents = []
        pos -= 1
        
        relational['Identifier'] = lines[pos].split()[0]
        fields.append(relational['Identifier'])         
        pos += 1
        relational['Operator'] = lines[pos].split()[0]
        pos += 1
        relational['Identifier'] = lines[pos].split()[0]
        fields.append(relational['Identifier'])
        relational['FieldAccess'] = fields
        pos += 1

        return relational        

    def equality(self):
        global tokens, pos, lines
        
        logic = {}
        fields = []
        idents = []
        pos -= 1
        
        logic['Identifier'] = lines[pos].split()[0]
        fields.append(logic['Identifier'])         
        pos += 1
        logic['Operator'] = lines[pos].split()[0]
        pos += 1
        logic['Identifier'] = lines[pos].split()[0]
        fields.append(logic['Identifier'])
        logic['FieldAccess'] = fields
        pos += 1

        return logic
    
    def logicAnd(self):
        global tokens, pos, lines
        
        logand = {}
        fields = []
        idents = []
        pos -= 1
        
        logand['Identifier'] = lines[pos].split()[0]
        fields.append(logand['Identifier'])         
        pos += 1
        logand['Operator'] = lines[pos].split()[0]
        pos += 1
        logand['Identifier'] = lines[pos].split()[0]
        fields.append(logand['Identifier'])
        logand['FieldAccess'] = fields
        pos += 1
            
        return logand
    
    def logicOr(self):
        global tokens, pos, lines
        
        logand = {}
        fields = []
        idents = []
        pos -= 1
        
        logand['Identifier'] = lines[pos].split()[0]
        fields.append(logand['Identifier'])         
        pos += 1
        logand['Operator'] = lines[pos].split()[0]
        pos += 1
        logand['Identifier'] = lines[pos].split()[0]
        fields.append(logand['Identifier'])
        logand['FieldAccess'] = fields
        pos += 1

        return logand

    def assign(self):
        global tokens, pos, lines
        pos -= 1

        assign = {}
        fields = []
        right = {}
        left = {}

        left['Identifier'] = lines[pos].split()[0]
        fields.append(left)
        pos += 1
        assign['Operator'] = re.findall(r"\=",tokens[pos])
        pos += 1
        exprNode = ExpressionNode()
        right['Identifier'] = exprNode.expBlock()
        fields.append(right)
        assign['FieldAccess'] = fields
        pos += 1

        return assign
    
