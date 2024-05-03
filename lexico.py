# -*- coding: utf-8 -*-
import ply.lex as lex

# Palabras reservadas basadas en Valorant
reserved = {
    'brimstone': 'PRINCIPAL',
    'cypher': 'COND_IF',
    'jett': 'COND_THEN',
    'sage': 'CIC_FOR',
    'breach': 'CIC_DO',
    'viper': 'CIC_WHILE',
    'recon': 'STRING',
    'emp': 'INTEGER',
    'smoke': 'DOUBLE',
    'heal': 'PRINTLN'
}

# Inicializar tabla de símbolos y tabla de errores
symbol_table = {}
error_table = []

# Lista de nombres de tokens incluyendo las palabras reservadas
tokens = [
    'PAREN_ABRE', 'PAREN_CIERRA', 'LLAVE_ABRE', 'LLAVE_CIERRA', 'COMA',
    'COMILLA', 'TOKEN_ASIG', 'IGUAL',
    'MAS', 'MENOS', 'MULTI', 'DIVI', 'MNQ', 'MYQ', 'MNIQ', 'MYIQ', 'EQ', 'DIST',
    'NUM_INTEGER', 'NUM_DOUBLE', 'ID'
] + list(reserved.values())

# Reglas de expresiones regulares para tokens simples
t_PAREN_ABRE = r'\('
t_PAREN_CIERRA = r'\)'
t_LLAVE_ABRE = r'\{'
t_LLAVE_CIERRA = r'\}'
t_COMA = r','
t_COMILLA = r'"'
t_TOKEN_ASIG = r';'
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

# Regla para identificadores
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')  # Verifica si el token es una palabra reservada
    # Agrega el identificador a la tabla de símbolos con información adicional
    symbol_table[t.value] = {
        "type": t.type,
        "line": t.lineno,
        "position": t.lexpos
    }
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

# Manejo de errores léxicos
def t_error(t):
    error_msg = "Illegal character '%s' at line %d position %d" % (t.value[0], t.lineno, t.lexpos)
    error_table.append({
        "message": error_msg,
        "line": t.lineno,
        "position": t.lexpos
    })
    print(error_msg)  # Opcional: imprimir el error al momento de ocurrencia
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()