from dataclasses import dataclass
import re
TOKEN_RE = re.compile(r"""
    (?P<WS>\s+)|(?P<COMMENT>//[^\n]*)|
    (?P<STRING>"(?:\\.|[^"])*")|
    (?P<NUMBER>\d+)|
    (?P<ID>[A-Za-z_]\w*)|
    (?P<OP>==|!=|<=|>=|->|::|[{}()<>;:,.=+\-*/])|
    (?P<MISMATCH>.)
""", re.X)
KEYWORDS={'class','extends','func','return','var','if','else','while','new','delete','virtual','package','plugin','template','try','catch','throw'}
@dataclass
class Token: kind:str; value:str; line:int; col:int
class Lexer:
    def tokenize(self,text):
        line=1; col=1; toks=[]
        for m in TOKEN_RE.finditer(text):
            kind=m.lastgroup; value=m.group()
            if kind in ('WS','COMMENT'): pass
            elif kind=='ID' and value in KEYWORDS: toks.append(Token(value.upper(),value,line,col))
            elif kind=='MISMATCH': raise SyntaxError(f'unexpected character {value!r} at {line}:{col}')
            else: toks.append(Token(kind,value,line,col))
            parts=value.split('\n'); line += len(parts)-1; col = len(parts[-1])+1 if len(parts)>1 else col+len(value)
        toks.append(Token('EOF','',line,col)); return toks
