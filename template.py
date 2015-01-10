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
            result += node.eval(scope)
        return result

def parse_python_node(tokens):
    output = ''
    index = 0
    for i, token in enumerate(tokens):
        if token != '}':
            output += token
        else:
            index = i
            break
    if tokens[index+1] != '}':
        raise ParseError
    node = PythonNode(output)
    tokens = tokens[index+2:]
    return (node, tokens)

def parse_text_node(tokens):
    output = ''
    index = 0
    for i, token in enumerate(tokens):
        if token != '{':
            output += token
        else:
            index = i
            break
    else:
        index = len(tokens)
    node = TextNode(output)
    tokens = tokens[index:]
    return (node, tokens)

def parse_group_node(tokens):
    children = []
    while tokens != '':
        if tokens[0] != '{':
            node, tokens = parse_text_node(tokens)
            children.append(node)
        else:
            node, tokens = parse_python_node(tokens[2:])
            children.append(node)
    return GroupNode(children)      
