# -*- coding: utf-8 -*-
class Node(object):
    """Base class for all AST nodes."""
    def __init__(self, type, children=None, leaf=None):
        self.type = type
        self.children = children if children is not None else []
        self.leaf = leaf

class Program(Node):
    """Represents the whole program."""
    def __init__(self, principal, name, body):
        super(Program, self).__init__('Program', [body])
        self.principal = principal
        self.name = name

class Body(Node):
    """Represents a body of statements."""
    def __init__(self, components=None):
        super(Body, self).__init__('Body', components if components else [])

class Declaration(Node):
    """Represents a declaration of a variable."""
    def __init__(self, type, assignment):
        super(Declaration, self).__init__('Declaration', [assignment], type)

class Assignment(Node):
    """Represents an assignment statement with an additional segment."""
    def __init__(self, identifier, expression, additional):
        super(Assignment, self).__init__('Assignment', [identifier, expression, additional])

class Println(Node):
    """Represents a print statement."""
    def __init__(self, expression):
        super(Println, self).__init__('Println', [expression])

class ForLoop(Node):
    """Represents a for loop."""
    def __init__(self, condition, body):
        super(ForLoop, self).__init__('ForLoop', [condition, body])

class IfStatement(Node):
    """Represents an if statement."""
    def __init__(self, condition, true_branch, false_branch=None):
        children = [condition, true_branch]
        if false_branch:
            children.append(false_branch)
        super(IfStatement, self).__init__('IfStatement', children)

class DoWhileLoop(Node):
    """Represents a do-while loop."""
    def __init__(self, body, condition):
        super(DoWhileLoop, self).__init__('DoWhileLoop', [body, condition])

class BinaryOperation(Node):
    """Represents a binary operation."""
    def __init__(self, operator, left, right):
        super(BinaryOperation, self).__init__('BinaryOperation', [left, right], operator)

class UnaryOperation(Node):
    """Represents a unary operation."""
    def __init__(self, operator, operand):
        super(UnaryOperation, self).__init__('UnaryOperation', [operand], operator)

class Literal(Node):
    """Represents a literal value."""
    def __init__(self, value):
        super(Literal, self).__init__('Literal', leaf=value)

class Identifier(Node):
    """Represents an identifier."""
    def __init__(self, name):
        super(Identifier, self).__init__('Identifier', leaf=name)

class Condition(Node):
    """Represents a condition in loops and if statements."""
    def __init__(self, expression):
        super(Condition, self).__init__('Condition', [expression])

class ListNode(Node):
    """Node to handle lists of items in the AST."""
    def __init__(self, items):
        super(ListNode, self).__init__('ListNode', items)
