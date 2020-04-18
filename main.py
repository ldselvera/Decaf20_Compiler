import scanner as sc
from io import StringIO
import sys
import decaf_parser as dp
import importlib
from contextlib import redirect_stdout

importlib.reload(dp)
importlib.reload(sc)

def scan(filename, out):
    with open(out, 'w') as f:
        with redirect_stdout(f):
            sc.scanner(filename)
            
def pars(lex_dir):
    prog = dp.ProgramNode()
    prog.load_data(lex_dir)
    prog.program()
        
def main():
#     input_dir = sys.argv[1]
#     lex_dir = sys.argv[2]
    input_dir = 'samples2/bad1.decaf'
    lex_dir = 'simple.out'

    scan(input_dir, lex_dir)
    pars(lex_dir)

if __name__ == "__main__":
    main()