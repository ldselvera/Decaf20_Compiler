import numpy as np
import os

reserved = {'void': 'T_Void', 'int': 'T_Int', 'double': 'T_Double','true': 'T_BoolConstant (value = true)', 'false': 'T_BoolConstant (value = false)',
            'string': 'T_String', 'null': 'T_Null', 'for': 'T_For', 'while': 'T_While', 'bool': 'T_Bool',
            'if': 'T_If', 'else': 'T_Else', 'return': 'T_Return','break': 'T_Break', 
            'Print': 'T_Print', 'ReadInteger': 'T_ReadInteger', 'ReadLine': 'T_ReadLine'}

operators = ['a', '1', 'E', '"', '/', '<', '>', '!', '=', '&', '|', '.', '+', '-', '*', '%', ';', ',', '(', ')', '{', '}', '_', '\n', ' ', '0', 'X', 'F', 'na', 'Token']

df = np.array([['a', '1', 'E', '"', '/', '<', '>', '!', '=', '&', '|', '.', '+', '-', '*', '%', ';', ',', '(', ')', '{', '}', '_', '\n', ' ', '0', 'X', 'F', 'na', 'Token'],
        [1, 2, 1, 7, 9, 14, 16, 18, 20, 22, 24, 36, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, -1, 0, 0, 37, 1, 1, -2, ''],
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, -2, 'T_Identifier'],
        [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, -2, 'T_IntConstant (value = %d)'],
        [0, 6, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, -2, 'T_DoubleConstant (value = %g)'],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -2, ''],
        [37, 5, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 0, 0, 5, 0, 0, -2, 'T_DoubleConstant (value = %g)'],
        [0, 6, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, -2, 'T_DoubleConstant (value = %g)'],
        [7, 7, 7, 8, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, -1, 7, 0, 0, 0, 7, ''],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -2, 'T_StringConstant (value = %s)'],
        [0, 0, 0, 0, 13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -2, '/'],
        [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 11, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 0, 0, 0, 10, ''],
        [0, 0, 0, 0, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -2, ''],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -2, 'comment'],
        [13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 0, 13, 13, 13, 13, 13, 'comment'],
        [0, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -2, '<'],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -2, 'T_LessEqual'],
        [0, 0, 0, 0, 0, 0, 0, 0, 17, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -2, '>'],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -2, 'T_GreaterEqual'],
        [0, 0, 0, 0, 0, 0, 0, 0, 19, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -2, '!'],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -2, 'T_NotEqual'],
        [0, 0, 0, 0, 0, 0, 0, 0, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -2, '='],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -2, 'T_Equal'],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 23, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -2, ''],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -2, 'T_And'],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 25, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -2, ''],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -2, 'T_Or'],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -2, '+'],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -2, '-'],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -2, '*'],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -2, '%'],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -2, ';'],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -2, ','],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -2, '('],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -2, ')'],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -2, '{'],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -2, '}'],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -2, '.'],
        [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 38, 0, -2, 'T_IntConstant (value = %d)'],
        [40, 39, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 39, 40, 39, -2, ''],
        [0, 39, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 39, 0, 39, -2, 'T_HexConstant (value = %d)'],
        [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, -2, '']])

df = df.transpose()
current_state  = 0
next_fsm = 0
line_count = 1
col_start = 1
col_end = 1

ch = ''                 #Hold current character
current_string = ""     #Hold current string being parsed
token = ""              #The final identified token of the string
    
encoding = 'utf-8'

def reset():
    global current_string, current_state
    current_string = ''
    current_state = 0

def scanner(input_dir):
    global current_state, line_count, col_start, col_end
    global ch, current_string, token

    with open(input_dir, 'rb') as f:
        while True:
            ch = f.read(1)
            ch = str(ch, encoding)
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
            if current_state == -2:
                print("\n*** Error line " + str(line_count) + ".")
                print("*** Unrecognized char: '" + ch + "'\n")
                reset()
                col_start = 1
                col_end = 1
                continue

            next_fsm = lookahead(f, fsm_ch, encoding)
            if next_fsm == 40:
                f.seek(-2, os.SEEK_CUR)
                current_state = 40
                current_string = ""
                col_end -= 1
                continue
            
            if next_fsm == 0 or next_fsm == -2:
                current_string += ch
                if current_string:
                    write_token(current_string, line_count, col_start, col_end, current_state)

                    #Reset current string and column count
                    reset()
                    col_end += 1
                    col_start = col_end
            elif next_fsm == -1:
                current_string += ch
                print("\n*** Error line " + str(line_count) + ".")
                print("*** Unterminated string constant: " + current_string + '\n')
                reset()
                col_start = 1
                col_end = 1
                continue
            elif next_fsm == -3:
                print("\n*** Error line " + str(line_count) + ".")
                print("*** Unrecognized char: '" + ch + "'\n")
                reset()
                col_start = 1
                col_end = 1
                line_count += 1
            elif next_fsm == -4:
                current_string = str(float(current_string + '0'))
                write_token(current_string, line_count, col_start, col_end-2, current_state)
                write_token('E', line_count, col_end - 1 , col_end -1, 1)
                write_token(ch, line_count, col_end, col_end, 26)
                f.seek(-1, os.SEEK_CUR)
                reset()
                col_end += 1
                col_start = col_end
            else:
                if ch:
                    col_end += 1
                    current_string += ch
    f.close()

def get_token( current_string, current_state):
    if current_string:
        itemindex = np.where(df[:,0]=='Token')
        token = df[itemindex[0][0]][current_state + 1]
        #token = df["Token"][current_state]

    if token == 'T_Identifier':
        #Check if identifier is a reserved word
        if current_string in reserved :
            token = reserved[current_string]
    elif token in operators:
        #Enclose operator in '' as shown in examples
        token = "'" + token + "'"
    elif token == 'T_IntConstant (value = %d)':   
        token = token % (int(current_string))
    elif token == 'T_HexConstant (value = %d)':   
        token = token % (int(current_string,0))
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
        elif (ch == 'x' or ch == 'X') and (current_state == 37):
            ch = 'X'
        elif (ch.lower() in "abcdefABCDEF" or ch.upper() in "abcdefABCDEF") and (current_state == 38 or current_state == 39):
            ch = 'F'
        elif ch.isalpha(): 
            ch= 'a'
        elif ch == '0':
            ch = '0'
        elif ch.isdigit() and ch != 0:
            ch = '1'
            
        if ch not in operators:
            ch = 'na'

        return ch

def lookahead(f, fsm_ch, encoding):
    global current_state, current_string, next_fsm
    
    f.seek(0,1)
    next_ch = str(f.read(1), encoding)

    if current_state == 22 and next_ch != '&':
        next_fsm = -3
    elif current_state == 5 and (not next_ch.isdigit()) and next_ch != '\n':
        next_fsm = -4
    elif current_state == 7 and (not next_ch):
        next_fsm = -1
    elif next_ch:
        next_ch = get_char(next_ch, current_state)
        next_fsm  = next_state(current_state, next_ch)   
        f.seek(-1, os.SEEK_CUR)
    elif not next_ch:
        next_fsm = 0
    else:
        next_fsm = 0
    
    return next_fsm

def write_token(current_string, line_count, col_start, col_end, current_state):
    fmt = '{:<12} {:<10}'
    token = get_token(current_string, current_state)
    if token != 'comment':
        if token == 'T_Identifier' and len(current_string) > 31:
            print("\n*** Error line " + str(line_count) + ".")
            print("*** Identifier too long: " + '"' + current_string + '"\n')
            truncated_string = current_string[:31]
            #line =  ' line %s cols %s-%s is %s (truncated to %s)' % ( str(line_count), str(col_start), str(col_end), token, truncated_string)
            line =  " line " + str(line_count) +  " cols " + str(col_start) + "-" + str(col_end) + " is " + token + " (truncated to " + truncated_string + ")"            
            print(fmt.format(current_string, line))
            #print(f"{current_string:<12}{line:>10}")
        else:
            #line =  ' line %s cols %s-%s is %s' % ( str(line_count), str(col_start), str(col_end), token)
            line =  " line " + str(line_count) +  " cols " + str(col_start) + "-" + str(col_end) + " is " + token
            print(fmt.format(current_string, line))
            #print(f"{current_string:<12}{line:>10}")

def next_state(current_state, ch):
    #Anything allowed withing string quotations
    if current_state == 10 and ch != '*':
        current_state = 10
    elif current_state == 11 and ch != '/':
        current_state = 11
    elif ch in reserved or ch in operators:
        itemindex = np.where(df[:,0]== ch)
        current_state = int(df[itemindex[0][0]][current_state + 1])
        #current_state  = df[ch][current_state]
    else:
        current_state = -2
    return current_state