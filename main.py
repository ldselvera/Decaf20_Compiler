import scanner as sc
from io import StringIO
import sys
import decaf_parser as dp
import importlib
from contextlib import redirect_stdout

importlib.reload(dp)
importlib.reload(sc)

def scan(filename, out):
    try:
        with open(out, 'w') as f:
            with redirect_stdout(f):
                sc.scanner(filename)
    except FileNotFoundError as e:
        print(e)
            
def pars(input_dir, lex_dir):
    try:
        prog = dp.ProgramNode()
        prog.load_data(input_dir, lex_dir)
        prog.program()
    except FileNotFoundError as e:
        print(e)
        
def main():
    input_dir = sys.argv[1]
    lex_dir = 'temp.out'

    scan(input_dir, lex_dir)
    pars(input_dir, lex_dir)

if __name__ == "__main__":
    main()