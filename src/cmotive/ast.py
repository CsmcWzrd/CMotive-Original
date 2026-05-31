from dataclasses import dataclass, field
from typing import List, Optional
@dataclass
class Node: pass
@dataclass
class Program(Node): declarations: List[Node]=field(default_factory=list)
@dataclass
class Function(Node): name:str; params:List[str]; body:List[Node]; return_type:str='Int'; method_of:Optional[str]=None
@dataclass
class ClassDecl(Node): name:str; base:Optional[str]; methods:List[Function]=field(default_factory=list); fields:List[str]=field(default_factory=list); has_virtuals:bool=False
@dataclass
class VarDecl(Node): name:str; value:str
@dataclass
class Return(Node): value:str
@dataclass
class ExprStmt(Node): value:str
@dataclass
class If(Node): condition:str; then_body:List[Node]; else_body:List[Node]
@dataclass
class While(Node): condition:str; body:List[Node]
