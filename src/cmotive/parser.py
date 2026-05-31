from .ast import Program, Function, ClassDecl, VarDecl, Return, ExprStmt, If, While
class Parser:
    def __init__(self,tokens): self.tokens=tokens; self.i=0
    def peek(self): return self.tokens[self.i]
    def take(self,kind=None,value=None):
        t=self.peek()
        if kind and t.kind!=kind: raise SyntaxError(f'expected {kind}, got {t.kind} at {t.line}:{t.col}')
        if value and t.value!=value: raise SyntaxError(f'expected {value}, got {t.value} at {t.line}:{t.col}')
        self.i+=1; return t
    def accept(self,value):
        if self.peek().value==value: return self.take()
        return None
    def parse(self):
        decls=[]
        while self.peek().kind!='EOF':
            if self.peek().kind=='CLASS': decls.append(self.class_decl())
            elif self.peek().kind=='FUNC': decls.append(self.function())
            elif self.peek().kind in ('PACKAGE','PLUGIN','TEMPLATE'): self.skip_scaffold()
            else: raise SyntaxError(f'unexpected token {self.peek().value}')
        return Program(decls)
    def skip_scaffold(self):
        depth=0
        while self.peek().kind!='EOF':
            v=self.take().value
            if v=='{': depth+=1
            elif v=='}': depth-=1
            elif v==';' and depth==0: break
            if depth<0: break
    def class_decl(self):
        self.take('CLASS'); name=self.take('ID').value; base=None
        if self.peek().kind=='EXTENDS': self.take('EXTENDS'); base=self.take('ID').value
        self.take(value='{'); methods=[]; fields=[]; has_virtuals=False
        while self.peek().value!='}':
            if self.peek().kind=='VIRTUAL': self.take('VIRTUAL'); has_virtuals=True
            if self.peek().kind=='FUNC':
                f=self.function(); f.method_of=name; methods.append(f)
            elif self.peek().kind=='VAR': self.take('VAR'); fields.append(self.take('ID').value); self.take(value=';')
            else: raise SyntaxError(f'unexpected class token {self.peek().value}')
        self.take(value='}'); return ClassDecl(name,base,methods,fields,has_virtuals)
    def function(self):
        self.take('FUNC'); name=self.take('ID').value; self.take(value='('); params=[]
        while self.peek().value!=')': params.append(self.take('ID').value); self.accept(',')
        self.take(value=')'); ret='Int'
        if self.accept(':'): ret=self.take('ID').value
        return Function(name,params,self.block(),ret)
    def block(self):
        self.take(value='{'); body=[]
        while self.peek().value!='}': body.append(self.statement())
        self.take(value='}'); return body
    def statement(self):
        if self.peek().kind=='RETURN': self.take('RETURN'); e=self.expr_until(';'); self.take(value=';'); return Return(e)
        if self.peek().kind=='VAR': self.take('VAR'); n=self.take('ID').value; self.take(value='='); e=self.expr_until(';'); self.take(value=';'); return VarDecl(n,e)
        if self.peek().kind=='IF':
            self.take('IF'); self.take(value='('); c=self.expr_until(')'); self.take(value=')'); th=self.block(); el=[]
            if self.peek().kind=='ELSE': self.take('ELSE'); el=self.block()
            return If(c,th,el)
        if self.peek().kind=='WHILE': self.take('WHILE'); self.take(value='('); c=self.expr_until(')'); self.take(value=')'); return While(c,self.block())
        e=self.expr_until(';'); self.take(value=';'); return ExprStmt(e)
    def expr_until(self,term):
        parts=[]; depth=0
        while not (self.peek().value==term and depth==0):
            if self.peek().value=='(': depth+=1
            elif self.peek().value==')': depth-=1
            parts.append(self.take().value)
        return ' '.join(parts)
