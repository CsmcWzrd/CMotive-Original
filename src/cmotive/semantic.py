from .ast import Function, ClassDecl, VarDecl

class SemanticError(Exception): pass

class SemanticAnalyzer:
    def analyze(self, program):
        funcs = set(); classes = {}; globals_ = set()
        for d in program.declarations:
            if isinstance(d, Function):
                key = (d.method_of or '', d.name)
                if key in funcs and not d.constructor:
                    raise SemanticError('duplicate function: ' + ('%s::%s' % key))
                funcs.add(key)
            elif isinstance(d, ClassDecl):
                if d.name in classes:
                    raise SemanticError('duplicate class: ' + d.name)
                classes[d.name] = d
            elif isinstance(d, VarDecl) and d.global_decl:
                if d.name in globals_:
                    raise SemanticError('duplicate global variable: ' + d.name)
                globals_.add(d.name)
        for c in classes.values():
            # CMotive 1.0 lowers single inheritance now.  Multiple inheritance in
            # source is accepted as metadata; only the first base participates in
            # the C bootstrap layout.
            if c.base and c.base not in classes:
                # Header/package imports may provide the base outside this unit, so
                # keep this a scaffold warning rather than an error.
                pass
        return {'functions': funcs, 'classes': classes, 'globals': globals_}
