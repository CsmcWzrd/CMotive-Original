#!/usr/bin/env python3
import argparse, re, sys
from pathlib import Path
DEFINE_RE = re.compile(r'^\s*#\s*define\s+(\w+)\s*(.*)$')
UNDEF_RE = re.compile(r'^\s*#\s*undef\s+(\w+)\s*$')
INCLUDE_RE = re.compile(r'^\s*#\s*include\s+["<]([^">]+)[">]\s*$')
TOKEN_RE = re.compile(r'\b[A-Za-z_]\w*\b')
class Preprocessor:
    def __init__(self, include_dirs):
        self.include_dirs=[Path(p) for p in include_dirs]; self.macros={}; self.seen=[]
    def resolve(self, name, current):
        for c in [current.parent/name]+[d/name for d in self.include_dirs]:
            if c.exists(): return c.resolve()
        raise FileNotFoundError('include not found: '+name)
    def expand(self,line): return TOKEN_RE.sub(lambda m:self.macros.get(m.group(0),m.group(0)), line)
    def process(self,path):
        path=Path(path).resolve()
        if path in self.seen: return ''
        self.seen.append(path); out=[f'// cmotivepp: begin {path}\n']
        for raw in path.read_text(encoding='utf-8').splitlines(True):
            m=INCLUDE_RE.match(raw)
            if m: out.append(self.process(self.resolve(m.group(1),path))); continue
            m=DEFINE_RE.match(raw)
            if m: self.macros[m.group(1)]=m.group(2).strip(); continue
            m=UNDEF_RE.match(raw)
            if m: self.macros.pop(m.group(1),None); continue
            out.append(self.expand(raw))
        out.append(f'// cmotivepp: end {path}\n'); return ''.join(out)
def main(argv=None):
    ap=argparse.ArgumentParser(prog='cmotivepp'); ap.add_argument('-I',dest='includes',action='append',default=[]); ap.add_argument('-D',dest='defines',action='append',default=[]); ap.add_argument('-o'); ap.add_argument('input')
    ns=ap.parse_args(argv); pp=Preprocessor(ns.includes)
    for d in ns.defines:
        k,v=(d.split('=',1)+['1'])[:2] if '=' in d else (d,'1'); pp.macros[k]=v
    text=pp.process(ns.input)
    if ns.o: Path(ns.o).parent.mkdir(parents=True,exist_ok=True); Path(ns.o).write_text(text,encoding='utf-8')
    else: sys.stdout.write(text)
if __name__=='__main__': main()
