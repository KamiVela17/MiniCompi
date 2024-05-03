# -*- coding: utf-8 -*-
class Node(object):
    """ Base class for AST nodes """
    def accept(self, visitor):
        return visitor.visit(self)

class Program(Node):
    def __init__(self, id, body):
        self.id = id
        self.body = body

class Body(Node):
    def __init__(self, statements):
        self.statements = statements

class Declaration(Node):
    def __init__(self, type, assignment):
        self.type = type
        self.assignment = assignment

class Assignment(Node):
    def __init__(self, id, expression):
        self.id = id
        self.expression = expression

class Println(Node):
    def __init__(self, expression):
        self.expression = expression

class ForLoop(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class IfStatement(Node):
    def __init__(self, condition, then_body, else_body=None):
        self.condition = condition
        self.then_body = then_body
        self.else_body = else_body

class DoWhileLoop(Node):
    def __init__(self, body, condition):
        self.body = body
        self.condition = condition

class BinaryOperation(Node):
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

class Condition(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class Literal(Node):
    def __init__(self, value):
        self.value = value

class Identifier(Node):
    def __init__(self, name):
        self.name = name

class SemanticAnalyzer(object):
    def __init__(self):
        self.errors = []

    def visit(self, node):
        """ Dispatch method to visit a node. """
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """ Called if no explicit visitor function exists for a node. """
        if hasattr(node, 'statements'):
            for stmt in node.statements:
                self.visit(stmt)
        elif hasattr(node, 'expression'):
            self.visit(node.expression)
        elif hasattr(node, 'condition'):
            self.visit(node.condition)
        elif hasattr(node, 'body'):
            self.visit(node.body)

    def visit_Program(self, node):
        if node.body:
            self.visit(node.body)

    def visit_Body(self, node):
        for stmt in node.statements:
            self.visit(stmt)

    def visit_Declaration(self, node):
        self.visit(node.assignment)

    def visit_Assignment(self, node):
        self.visit(node.expression)

    def visit_Println(self, node):
        self.visit(node.expression)

    def visit_ForLoop(self, node):
        self.visit(node.condition)
        self.visit(node.body)

    def visit_IfStatement(self, node):
        self.visit(node.condition)
        self.visit(node.then_body)
        if node.else_body:
            self.visit(node.else_body)

    def visit_DoWhileLoop(self, node):
        self.visit(node.body)
        self.visit(node.condition)

    def visit_BinaryOperation(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_Condition(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_Literal(self, node):
        pass

    def visit_Identifier(self, node):
        pass

    def report_errors(self):
        for error in self.errors:
            print("Semantic error:", error)
