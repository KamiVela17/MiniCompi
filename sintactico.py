# -*- coding: utf-8 -*-
from __future__ import print_function
import ply.yacc as yacc
from lexico import tokens, lexer
from semantico import *

symbol_table = {}  # Tabla de símbolos para guardar contextos de las variables y funciones
error_table = []   # Tabla de errores para registrar los errores encontrados durante el análisis

# Precedencia de operadores (si es necesaria)
precedence = (
    ('left', 'EQ', 'DIST'),
    ('left', 'MNQ', 'MYQ', 'MNIQ', 'MYIQ'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'MULTI', 'DIVI'),
)

# Regla para el programa principal
def p_program(p):
    'program : PRINCIPAL ID LLAVE_ABRE cuerpo LLAVE_CIERRA'
    p[0] = Program(p[1], p[2], p[4])
    symbol_table[p[2]] = {'type': 'program', 'line': p.lineno(2)}

def p_cuerpo(p):
    '''cuerpo : declaracion cuerpo2
              | asig cuerpo2
              | println cuerpo2
              | para cuerpo2
              | sif cuerpo2
              | dhacer cuerpo2
              | res cuerpo2
              | empty'''
    if len(p) == 3:
        if p[2]:
            p[0] = Body([p[1]] + p[2].children)
        else:
            p[0] = Body([p[1]])
    else:
        p[0] = Body([])


def p_cuerpo2(p):
    '''cuerpo2 : cuerpo
               | empty'''
    p[0] = p[1]

def p_declaracion(p):
    'declaracion : tipod asig'
    p[0] = Declaration(p[1], p[2])
    symbol_table[p[2].children[0].leaf] = {'type': p[1], 'line': p.lineno(1)}


def p_tipod(p):
    '''tipod : INTEGER
             | DOUBLE
             | STRING'''
    p[0] = p[1]

def p_println(p):
    'println : PRINTLN idnum TOKEN_ASIG'
    p[0] = Println(p[2])

def p_asig(p):
    'asig : ID tipoasig masasig TOKEN_ASIG'
    p[0] = Assignment(Identifier(p[1]), p[2], p[3])
    if p[1] in symbol_table:
        symbol_table[p[1]]['last_assigned'] = p.lineno(1)
    else:
        symbol_table[p[1]] = {'type': 'unknown', 'line': p.lineno(1), 'declared': False}
        error_table.append({'line': p.lineno(1), 'error': 'Variable "{}" not declared.'.format(p[1])})


def p_tipoasig(p):
    '''tipoasig : IGUAL idnum
                | IGUAL COMILLA ID COMILLA'''
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = Literal(p[3])

def p_idnum(p):
    '''idnum : num
             | ID'''
    if isinstance(p[1], str):  
        p[0] = Identifier(p[1])  
    else:
        p[0] = p[1]  

def p_num(p):
    '''num : NUM_INTEGER
           | NUM_DOUBLE'''
    p[0] = Literal(p[1])

def p_masasig(p):
    '''masasig : COMA asig masasig
               | oparit idnum masasig
               | empty'''
    if len(p) == 4:
        items = [p[2]] + (p[3] if p[3] else [])
        p[0] = ListNode(items) if items else ListNode([])
    else:
        p[0] = ListNode([])

def p_para(p):
    'para : CIC_FOR PAREN_ABRE condicionpara PAREN_CIERRA LLAVE_ABRE cuerpo LLAVE_CIERRA'
    p[0] = ForLoop(p[3], p[6])
    # Registrar la línea de inicio del bucle for en la tabla de símbolos para análisis de flujo de control
    symbol_table['for_loop_at_line_{}'.format(p.lineno(1))] = {'line': p.lineno(1)}

def p_sif(p):
    'sif : COND_IF PAREN_ABRE condicion PAREN_CIERRA COND_THEN LLAVE_ABRE cuerpo LLAVE_CIERRA'
    p[0] = IfStatement(p[3], p[7])
    # Registrar la línea de inicio de la sentencia if
    symbol_table['if_statement_at_line_{}'.format(p.lineno(1))] = {'line': p.lineno(1)}


def p_condicionpara(p):
    'condicionpara : inicio TOKEN_ASIG fin TOKEN_ASIG indec'
    p[0] = Condition(p[1], p[3], p[5])

def p_inicio(p):
    'inicio : ID IGUAL idnum'
    p[0] = Assignment(Identifier(p[1]), p[3])

def p_fin(p):
    'fin : ID oprel idnum'
    p[0] = BinaryOperation(p[2], Identifier(p[1]), p[3])

def p_indec(p):
    '''indec : idnum MAS MAS
             | idnum MENOS MENOS'''
    operation = 'increment' if p[2] == '+' else 'decrement'
    p[0] = UnaryOp(operation, p[1])

def p_sif(p):
    'sif : COND_IF PAREN_ABRE condicion PAREN_CIERRA COND_THEN LLAVE_ABRE cuerpo LLAVE_CIERRA'
    p[0] = IfStatement(p[3], p[7])
    # Registrar la línea de inicio de la sentencia if
    symbol_table['if_statement_at_line_{}'.format(p.lineno(1))] = {'line': p.lineno(1)}

def p_dhacer(p):
    'dhacer : CIC_DO LLAVE_ABRE cuerpo LLAVE_CIERRA CIC_WHILE PAREN_ABRE condicion PAREN_CIERRA'
    p[0] = DoWhileLoop(p[3], p[7])

def p_res(p):
    'res : idnum oparit idnum'
    p[0] = BinaryOperation(p[2], p[1], p[3])

def p_condicion(p):
    'condicion : ID oprel mascondicion'
    p[0] = BinaryOperation(p[2], Identifier(p[1]), p[3])

def p_mascondicion(p):
    '''mascondicion : idnum oprel mascondicion
                    | idnum'''
    if len(p) == 4:
        p[0] = BinaryOperation(p[2], p[1], p[3])
    else:
        p[0] = p[1]

def p_oparit(p):
    '''oparit : MAS
              | MENOS
              | MULTI
              | DIVI'''
    p[0] = p[1]

def p_oprel(p):
    '''oprel : MNQ
             | MYQ
             | MNIQ
             | MYIQ
             | EQ
             | DIST'''
    p[0] = p[1]

def p_empty(p):
    'empty :'
    pass

# Manejo de errores
def p_error(p):
    if p:
        error = "Syntax error at token '%s' on line %d" % (p.value, p.lineno)
        print(error)
        error_table.append({'line': p.lineno, 'error': error})
    else:
        print("Syntax error at EOF")


# Construir el parser
parser = yacc.yacc()

def print_ast(node, indent=0):
    if not isinstance(node, Node):
        raise TypeError("Expected a Node, received {}: {}".format(type(node).__name__, node))

    result = " " * indent + "'{}'".format(node.type)
    if node.leaf is not None:
        result += " '{}'".format(node.leaf)
    result += "\n"
    for child in node.children:
        result += print_ast(child, indent + 4)
    return result

def analizar_y_traducir(source_code):
    result = parser.parse(source_code, lexer=lexer)
    print("--------------Arbol de Analisis Sintactico--------------")
    print(print_ast(result))
    print("\n--------------Tabla de Símbolos--------------")
    for symbol, info in symbol_table.items():
        print("{}: {}".format(symbol, info))
    print("\n--------------Tabla de Errores--------------")
    for error in error_table:
        print (error)

