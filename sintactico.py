# -*- coding: utf-8 -*-

import ply.lex as lex
import ply.yacc as yacc
from lexico import tokens, lexer
from semantico import Node, Program, Body, Declaration, Assignment, Println, ForLoop, IfStatement, DoWhileLoop, BinaryOperation, Condition, Literal, Identifier, SemanticAnalyzer

def p_program(p):
    'program : PRINCIPAL ID LLAVE_ABRE cuerpo LLAVE_CIERRA'
    p[0] = Program(p[2], p[5])

def p_cuerpo(p):
    '''cuerpo : declaracion cuerpo
              | asig cuerpo
              | println cuerpo
              | para cuerpo
              | sif cuerpo
              | dhacer cuerpo
              | res cuerpo
              | empty'''
    if len(p) > 2:
        statements = [p[1]] + (p[2].statements if p[2] else [])
    else:
        statements = [p[1]]
    p[0] = Body(statements)

def p_declaracion(p):
    'declaracion : tipod asig SEMICOLON'
    p[0] = Declaration(p[1], p[2])

def p_tipod(p):
    '''tipod : INTEGER
             | DOUBLE
             | STRING'''
    p[0] = p[1]

def p_println(p):
    'println : PRINTLN idnum SEMICOLON'
    p[0] = Println(p[2])

def p_asig(p):
    'asig : ID tipoasig masasig'
    expression = p[2][1] if len(p[3]) > 0 else p[2][1]
    p[0] = Assignment(p[1], expression)

def p_tipoasig(p):
    '''tipoasig : IGUAL idnum
                | IGUAL COMILLA ID COMILLA'''
    p[0] = ('=', p[2] if len(p) == 3 else Identifier(p[3]))

def p_idnum(p):
    '''idnum : num
             | ID'''
    p[0] = Literal(p[1]) if isinstance(p[1], (int, float)) else Identifier(p[1])

def p_num(p):
    '''num : NUM_INTEGER
           | NUM_DOUBLE'''
    p[0] = int(p[1]) if '.' not in p[1] else float(p[1])

def p_masasig(p):
    '''masasig : COMA asig masasig
               | empty'''
    p[0] = [p[2]] + p[3] if len(p) > 2 else []

def p_para(p):
    'para : CIC_FOR PAREN_ABRE condicionpara PAREN_CIERRA LLAVE_ABRE cuerpo LLAVE_CIERRA'
    p[0] = ForLoop(p[3], p[6])

def p_condicionpara(p):
    'condicionpara : inicio IGUAL fin IGUAL indec'
    p[0] = Condition(p[1], '==', p[3])

def p_inicio(p):
    'inicio : ID IGUAL idnum'
    p[0] = BinaryOperation('=', Identifier(p[1]), p[3])

def p_fin(p):
    'fin : ID oprel idnum'
    p[0] = Condition(Identifier(p[1]), p[2], p[3])

def p_indec(p):
    '''indec : idnum MAS MAS
             | idnum MENOS MENOS'''
    p[0] = (p[1], p[2])

def p_sif(p):
    'sif : COND_IF PAREN_ABRE condicion PAREN_CIERRA COND_THEN LLAVE_ABRE cuerpo LLAVE_CIERRA massif'
    p[0] = IfStatement(p[3], p[7], p[9] if p[9] else None)

def p_massif(p):
    'massif : COND_THEN LLAVE_ABRE cuerpo LLAVE_CIERRA'
    p[0] = p[3]

def p_dhacer(p):
    'dhacer : CIC_DO LLAVE_ABRE cuerpo LLAVE_CIERRA CIC_WHILE PAREN_ABRE condicion PAREN_CIERRA'
    p[0] = DoWhileLoop(p[3], p[7])

def p_condicion(p):
    'condicion : ID oprel mascondicion'
    p[0] = Condition(Identifier(p[1]), p[2], p[3])

def p_mascondicion(p):
    '''mascondicion : idnum oprel mascondicion
                    | idnum'''
    p[0] = p[1:]

def p_res(p):
    'res : idnum oparit idnum'
    p[0] = BinaryOperation(p[2], p[1], p[3])

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
    
def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

class ASTPrinter:
    def print_ast(self, node, level=0):
        indent = " " * (level * 2)
        result = indent + node.__class__.__name__ + ": "

        if isinstance(node, Program) or isinstance(node, Body) or isinstance(node, IfStatement) or isinstance(node, DoWhileLoop) or isinstance(node, ForLoop):
            result += "\n"
            if hasattr(node, 'statements'):
                for stmt in node.statements:
                    result += self.print_ast(stmt, level + 1)
            elif hasattr(node, 'body'):
                result += self.print_ast(node.body, level + 1)
            if hasattr(node, 'condition'):
                result += indent + "  Condition:\n" + self.print_ast(node.condition, level + 2)
            if hasattr(node, 'then_body'):
                result += indent + "  Then:\n" + self.print_ast(node.then_body, level + 2)
            if hasattr(node, 'else_body') and node.else_body is not None:
                result += indent + "  Else:\n" + self.print_ast(node.else_body, level + 2)
        elif isinstance(node, Condition) or isinstance(node, BinaryOperation):
            result += "(" + self.print_ast(node.left, 0) + " " + node.operator + " " + self.print_ast(node.right, 0) + ")\n"
        elif isinstance(node, Declaration) or isinstance(node, Assignment) or isinstance(node, Println):
            result += node.id + " = " + self.print_ast(node.expression, 0)
        elif isinstance(node, Literal) or isinstance(node, Identifier):
            result += node.value + "\n"
        else:
            result += "Unknown node type\n"

        return result

def analizar_y_traducir(source_code):
    ast = parser.parse(source_code, lexer=lexer)
    printer = ASTPrinter()
    print("AST del código proporcionado:")
    print(printer.print_ast(ast))

    semantic_analyzer = SemanticAnalyzer()
    semantic_analyzer.visit(ast)
