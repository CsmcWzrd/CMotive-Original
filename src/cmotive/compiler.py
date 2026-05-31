from pathlib import Path
from .lexer import Lexer
from .parser import Parser
from .semantic import SemanticAnalyzer
from .codegen import NativeCodegen
class CompilerPipeline:
    def __init__(self,include_dirs=None,target_arch='native'): self.include_dirs=include_dirs or []; self.target_arch=target_arch
    def compile_to_c(self,src_path):
        ast=Parser(Lexer().tokenize(Path(src_path).read_text(encoding='utf-8'))).parse()
        sema=SemanticAnalyzer().analyze(ast)
        return NativeCodegen(self.target_arch).emit(ast,sema)
