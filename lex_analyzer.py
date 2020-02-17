import pandas as pd
import numpy as np
import os
import re

reserved = {'void': 'T_Void', 'int': 'T_Int', 'double': 'T_Double','true': 'T_BoolConstant (value = true)', 'false': 'T_BoolConstant (value = false)',
            'string': 'T_String', 'null': 'T_Null', 'for': 'T_For', 'while': 'T_While', 
            'if': 'T_If', 'else': 'T_Else', 'return': 'T_Return','break': 'T_Break', 
            'Print': 'T_Print', 'ReadInteger': 'T_ReadInteger', 'ReadLine': 'T_ReadLine'}

operators = ['a', '0', 'E', '"', '/', '<', '>', '!', '=', '&', '|', '.', '+', '-', '*', '%', ';', ',', '(', ')', '{', '}', '_', '\n', ' ', 'Token']

q_n = [[1, 2, 1, 7, 9, 14, 16, 18, 20, 22, 24, 13, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, -1, 0, 0, ''],
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 'T_Identifier'],
        [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'T_IntConstant (value = %d)'],
        [0, 6, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'T_DoubleConstant (value = %g)'],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ''],
        [0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'T_DoubleConstant (value = %g)'],
        [0, 6, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'T_DoubleConstant (value = %g)'],
        [7, 7, 7, 8, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, ''],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'T_StringConstant (value = %s)'],
        [0, 0, 0, 0, 13, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "'"],
        [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 11, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 0, 0,''],
        [0, 0, 0, 0, 12, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,''],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'comment'],
        [13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 0, 0, 'comment'],
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
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '}']]


def get_token(current_string, previous_state):
    if current_string:
        #Get the token of finished FSM
        token = df["Token"][previous_state]

    if token is 'T_Identifier':
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

def get_char(ch, previous_state):
        #Handle doubles with e or E
        if (ch == 'e' or ch == 'E') and (previous_state == 6 or previous_state == 3):
            ch ='E'
        elif ch.isalpha(): 
            ch= 'a'
        elif ch.isdigit():
            ch = '0'

        return ch
    
def scanner(filename):
    current_state  = 0
    ch = ''        #Hold current character
    current_string = ""     #Hold current string being parsed
    token = ""     #The final identified token of the string

    encoding = 'utf-8'    
    myfile = open("out.txt", "w")
    
    line_count = 0
    col_count = 0
    
    with open(filename, 'rb') as f:
        while True:
            ch = f.read(1)
            previous_state = current_state                
            ch = str(ch, encoding)
            fsm_ch = get_char(ch, previous_state)
            
            if ch == '\n': line_count += 1
            if not ch: return 0

            #Anything allowed withing string quotations
            if current_state == 7 and ch != '"':
                current_state = 7
            else:
                current_state  = df[fsm_ch][current_state ]

            #If have reached the end of current FSM
            if current_state == 0:
                if current_string:
                    token = get_token(current_string, previous_state)
                    line =  ' line %s cols %s-%s is %s\n' % ( str(line_count), str(1), str(col_count), token)
                    myfile.write(f"{current_string:<12}{line:>10}")

                    #Reset current string and column count
                    current_string = ''
                    col_count = 0
            else:
                #Keep adding to current string
                current_string += ch
                col_count += 1
        myfile.close()
        
df = pd.DataFrame(data = q_n, columns = operators)
filename = 'samples/string.frag'
scanner(filename)