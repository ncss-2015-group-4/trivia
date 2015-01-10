'''
PROPERTY OF THE HOLY SOCIETY OF TEMPLATEIA. UNAUTHORISED EDITING WILL BE PROSECUTED

This code parses the templates into python and html.
The python code can then be evaluated and added to the html to be displayed by a web browser
'''

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

def _parse_template(template, upto, parent):
    #TODO
    pass

def parse_template(template):
    return _parse_template(template, 0, None)

