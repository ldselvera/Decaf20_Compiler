import pandas as pd
import numpy as np
import sys
import os
import re

reserved = {'void': 'T_Void', 'int': 'T_Int', 'double': 'T_Double','true': 'T_BoolConstant (value = true)', 'false': 'T_BoolConstant (value = false)',
            'string': 'T_String', 'null': 'T_Null', 'for': 'T_For', 'while': 'T_While', 
            'if': 'T_If', 'else': 'T_Else', 'return': 'T_Return','break': 'T_Break', 
            'Print': 'T_Print', 'ReadInteger': 'T_ReadInteger', 'ReadLine': 'T_ReadLine'}

operators = ['a', '0', 'E', '"', '/', '<', '>', '!', '=', '&', '|', '.', '+', '-', '*', '%', ';', ',', '(', ')', '{', '}', '_', '\n', ' ', 'Token']

q_n = [[1, 2, 1, 7, 9, 14, 16, 18, 20, 22, 24, 36, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, -1, 0, 0, ''],
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 'T_Identifier'],
        [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'T_IntConstant (value = %d)'],
        [0, 6, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'T_DoubleConstant (value = %g)'],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ''],
        [0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'T_DoubleConstant (value = %g)'],
        [0, 6, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'T_DoubleConstant (value = %g)'],
        [7, 7, 7, 8, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, -1, 7, ''],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'T_StringConstant (value = %s)'],
        [0, 0, 0, 0, 13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '/'],
        [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 11, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,''],
        [0, 0, 0, 0, 12, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11,''],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'comment'],
        [13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 0, 13, 'comment'],
        [0, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '<'],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,'T_LessEqual'],
        [0, 0, 0, 0, 0, 0, 0, 0, 17, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '>'],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'T_GreaterEqual'],
        [0, 0, 0, 0, 0, 0, 0, 0, 19, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '!'],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '!='],
        [0, 0, 0, 0, 0, 0, 0, 0, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '='],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'T_Equal'],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 23, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ''],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'T_And'],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 25, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ''],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'T_Or'],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '+'],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '-'],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '*'],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '%'],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ';'],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ','],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '('],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ')'],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '{'],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '}'],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '.']]


def get_token(current_string, current_state):
    if current_string:
        token = df["Token"][current_state]
        
    if token == 'T_Identifier':
        #Check if identifier is a reserved word
        if current_string in reserved :
            token = reserved[current_string]
    elif token in operators:
        #Enclose operator in '' as shown in examples
        token = "'" + token + "'"
    elif token == 'T_IntConstant (value = %d)':    
        token = token % (int(current_string)) 
    elif token == "T_DoubleConstant (value = %g)":
        #Use holdplacer %g to show double withouth trailing 0
        token = token % (float(current_string))
    elif token == 'T_StringConstant (value = %s)':
        token = token % (current_string)

    return token

def get_char(ch, current_state):
        #Handle doubles with e or E
        if (ch == 'e' or ch == 'E') and (current_state == 3 or current_state == 6):
            ch ='E'
        elif ch.isalpha(): 
            ch= 'a'
        elif ch.isdigit():
            ch = '0'

        return ch

def lookahead(f, fsm_ch, current_state, encoding):
    f.seek(0,1)
    next_ch = str(f.read(1), encoding)
    
    if fsm_ch == '&' and next_ch != '&':
        return -3
    elif current_state == 5 and (not next_ch.isdigit()) and next_ch != '\n':
        return -4
    elif next_ch:
        next_ch = get_char(next_ch, current_state)
        fsm_next  = next_state(current_state, next_ch)        
        f.seek(-1, os.SEEK_CUR)
        return fsm_next
    
    return 0

def write_token(current_string, line_count, col_start, col_end, current_state, out):
    token = get_token(current_string, current_state)
    if token != 'comment':
        if token == 'T_Identifier' and len(current_string) > 31:
            out.write(f"\n*** Error line " + str(line_count) + ".\n")
            out.write(f"*** Identifier too long: " + '"' + current_string + '"\n\n')
            truncated_string = current_string[:31]
            line =  ' line %s cols %s-%s is %s (truncated to %s)\n' % ( str(line_count), str(col_start), str(col_end), token, truncated_string)
            out.write(f"{current_string:<12}{line:>10}")
        else:
            line =  ' line %s cols %s-%s is %s\n' % ( str(line_count), str(col_start), str(col_end), token)
            out.write(f"{current_string:<12}{line:>10}")
        
def next_state(current_state, ch):

    #Anything allowed withing string quotations
    if current_state == 7 and ch != '"' and ch != '\n':
        current_state = 7
    elif current_state == 13 and ch != '\n':
        current_state =13
    elif current_state == 10 and ch != '*':
        current_state = 10
    elif current_state == 11 and ch != '/':
        current_state = 11
    elif ch in reserved or ch in operators:
        current_state  = df[ch][current_state]
    else:
        current_state = -2

    return current_state
    
def scanner(filename):
    current_state  = 0
    line_count = 1
    col_start = 1
    col_end = 1
    
    ch = ''        #Hold current character
    current_string = ""     #Hold current string being parsed
    token = ""     #The final identified token of the string

    encoding = 'utf-8'
    #in_file = 'samples/' + filename +'.frag'
    in_file = 'samples/' + filename 
    filename = filename.split('.')[0]
    out = open( filename + ".out", "w")
    
    with open(in_file, 'rb') as f:
        while True:

            ch = str(f.read(1), encoding)
            fsm_ch = get_char(ch, current_state)
            
            if not ch: return 0
            elif ch == '\n' and current_state != 7:
                col_start = 1
                col_end = 1
                line_count += 1
                continue
            elif ch == ' ' and current_state != 7:
                col_start += 1
                col_end += 1
                continue
            
            current_state = next_state(current_state, fsm_ch)
            
            if current_state == -1:                   
                out.write(f"\n*** Error line " + str(line_count) + ".\n")
                out.write(f"*** Unterminated string constant: " + current_string + '\n\n')
                current_string = ''
                current_state = 0
                col_start = 1
                col_end = 1
                line_count += 1
                continue
            if current_state == -2:
                out.write(f"\n*** Error line " + str(line_count) + ".\n")
                out.write(f"*** Unrecognized char: '" + ch + "'\n\n")
                current_string = ''
                current_state = 0
                col_start = 1
                col_end = 1
                continue
                
            next_fsm = lookahead(f, fsm_ch, current_state, encoding)

            if next_fsm == 0:
                current_string += ch
                if current_string:
                    write_token(current_string, line_count, col_start, col_end, current_state, out)

                    #Reset current string and column count
                    current_string = ''
                    current_state = 0
                    col_end += 1
                    col_start = col_end
            elif next_fsm == -3:
                out.write(f"\n*** Error line " + str(line_count) + ".\n")
                out.write(f"*** Unrecognized char: '" + ch + "'\n\n")
                current_string = ''
                current_state = 0
                col_start = 1
                col_end = 1
                line_count += 1
            elif next_fsm == -4:
                current_string = str(float(current_string + '0'))
                write_token(current_string, line_count, col_start, col_end-2, current_state, out)
                write_token('E', line_count, col_end - 1 , col_end -1, 1, out)
                write_token(ch, line_count, col_end, col_end, 26, out)
                f.seek(-1, os.SEEK_CUR)
                current_string = ''
                current_state = 0
                col_end += 1
                col_start = col_end
            else:
                #Keep adding to current string
                col_end += 1
                current_string += ch
    out.close()
        
df = pd.DataFrame(data = q_n, columns = operators)
filename = sys.argv[1]
scanner(filename)