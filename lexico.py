# -*- coding: utf-8 -*-

import ply.lex as lex

# Lista de palabras reservadas
reserved = {
    'reyna': 'PRINCIPAL',
    'jett': 'COND_IF',
    'brimstone': 'COND_THEN',
    'omen': 'CIC_FOR',
    'breach': 'CIC_DO',
    'killjoy': 'CIC_WHILE',
    'vandal': 'INTEGER',
    'phantom': 'DOUBLE',
    'operator': 'STRING',
    'heal': 'PRINTLN',
}

# Lista de tokens
tokens = [
    'SEMICOLON',
    'ID', 'NUM_INTEGER', 'NUM_DOUBLE',
    'IGUAL', 'MAS', 'MENOS', 'MULTI', 'DIVI',
    'MNQ', 'MYQ', 'MNIQ', 'MYIQ', 'EQ', 'DIST',
    'LLAVE_ABRE', 'LLAVE_CIERRA', 'PAREN_ABRE', 'PAREN_CIERRA', 
    'COMA', 'COMILLA', 'DOT', 'COLON',
] + list(reserved.values())

t_SEMICOLON = r';'
t_IGUAL = r'='
t_MAS = r'\+'
t_MENOS = r'-'
t_MULTI = r'\*'
t_DIVI = r'/'
t_MNQ = r'<'
t_MYQ = r'>'
t_MNIQ = r'<='
t_MYIQ = r'>='
t_EQ = r'=='
t_DIST = r'!='
t_LLAVE_ABRE = r'\{'
t_LLAVE_CIERRA = r'\}'
t_PAREN_ABRE = r'\('
t_PAREN_CIERRA = r'\)'
t_COMA = r','
t_COMILLA = r'"'
t_DOT = r'\.'
t_COLON = r':'

# Regla para identificadores
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

# Regla para números enteros
def t_NUM_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Regla para números con punto flotante
def t_NUM_DOUBLE(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

# Regla para ignorar espacios en blanco
def t_WS(t):
    r'[ \t\r\n]+'
    pass 

# Regla para manejar errores
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()
