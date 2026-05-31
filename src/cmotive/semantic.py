from .ast import Function, ClassDecl
class SemanticError(Exception): pass
class SemanticAnalyzer:
    def analyze(self,program):
        funcs=set(); classes={}
        for d in program.declarations:
            if isinstance(d,Function):
                if d.name in funcs: raise SemanticError('duplicate function: '+d.name)
                funcs.add(d.name)
            elif isinstance(d,ClassDecl):
                if d.name in classes: raise SemanticError('duplicate class: '+d.name)
                classes[d.name]=d
        for c in classes.values():
            if c.base and c.base not in classes: raise SemanticError(f'unknown base class {c.base} for {c.name}')
        return {'functions':funcs,'classes':classes}
