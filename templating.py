'''
PROPERTY OF THE HOLY SOCIETY OF TEMPLATEIA. UNAUTHORISED EDITING WILL BE PROSECUTED

This code parses the templates into python and html.
The python code can then be evaluated and added to the html to be displayed by a web browser
'''
class ParseError(Exception):
    pass

class Node(object):
    def __init__(self, content):
        self.content = content
    def eval(self):
        raise NotImplementedError()

class PythonNode(Node):
    def eval(self, scope):
        return eval(self.content, scope)

class TextNode(Node):
    def eval(self, scope):
        return self.content

class GroupNode(Node):
    def __init__(self, children):
        self.children = children
    def eval(self, scope):
        result = ''
        for node in self.children:
            result += str(node.eval(scope))
        return result
        
class IfNode(Node):
    def __init__(self, predicate, true_node):
        self.predicate = predicate
        self.true_node = true_node

    def eval(self, scope):
        if eval(self.predicate, scope):
            return self.true_node.eval(scope)
        else:
            return ''

class Parser(object):
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0
        self.length = len(tokens)

    def _parse_python_node(self):
        #need to account for python node in python node
        content = ''
        content += self.tokens[self.index]
        while self.read_next() != '}':
            self.next()
            content += self.tokens[self.index]
        if self.read_next() != '}':
            raise ParseError("'}' expected")
        if not self.is_end():
            self.next()
        self.next()
        self.next()
        return PythonNode(content)

    def _parse_text_node(self):
        content = ''
        content += self.tokens[self.index]
        while self.read_next() != '{':
            self.next()
            content += self.tokens[self.index]
        self.next()
        return TextNode(content)

    def _parse_group_node(self):
        children = []
        while not self.is_end():
            if self.tokens[self.index] == '{':
                self.next()
                if self.tokens[self.index] == '{':
                    self.next()
                    children.append(self._parse_python_node())
                else:
                    raise ParseError("Unexpected token after '{'")
            else:
                children.append(self._parse_text_node())
        return GroupNode(children)
        
    def parse(self):
        node = self._parse_group_node()
        if not self.is_end():
            raise ParseError("Extra input")
        return node
    
    def eval(self, scope):
        return self.parse().eval(scope)

    def read_next(self):
        return self.tokens[self.index + 1]

    def is_end(self):
        return self.index >= self.length - 1

    def next(self):
        self.index += 1
            
