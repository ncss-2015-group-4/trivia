'''
PROPERTY OF THE HOLY SOCIETY OF TEMPLATEIA. UNAUTHORISED EDITING WILL BE PROSECUTED

This code parses the templates into python and html.
The python code can then be evaluated and added to the html to be displayed by a web browser
'''

IF_TAG = ' if '
INCLUDE_TAG = ' include '
FOR_TAG = ' for '

class ParseError(Exception):
    '''
    Defines an exception for errors encounterd while parsing
    '''
    pass

class Node(object):
    '''
    Defines a basic node object
    '''
    def __init__(self, content):
        self.content = content
    def eval(self, scope):
        raise NotImplementedError()

class PythonNode(Node):
    '''
    Defines a node for the execution of python code
    Syntax: {{<python_expression}}
    '''
    def eval(self, scope):
        #return the execution of the python code
        return eval(self.content, scope)

class TextNode(Node):
    '''
    Defines a node for html code/other stuff that is not part of the templating language
    '''
    def eval(self, scope):
        return self.content

class GroupNode(Node):
    '''
    Defines a node to group nodes in the same area, e.g within a for/if statement
    '''
    def __init__(self, children):
        self.children = children
    def eval(self, scope):
        result = ''
        #evaluate all the child nodes and add them to output
        for node in self.children:
            result += str(node.eval(scope))
        return result
        
class IfNode(Node):
    '''
    Defines a node for execution if statements
    Syntax: {% if <condition> %}<stuff>{% end if %}
    '''
    def __init__(self, predicate, true_node):
        self.predicate = predicate
        self.true_node = true_node

    def eval(self, scope):
        if eval(self.predicate, scope):
            return self.true_node.eval(scope)
        else:
            return ''

class IncludeNode(Node):
    '''
    Defines a node for including other html files
    Syntax: {% include <file> %}
    '''
    def __init__(self, path):
        self.path = path.strip()
        
    def eval(self, scope):
        with open(self.path) as p:
            lines=[line.strip() for line in p]
            template=''.join(lines)
        return Parser(template).eval(scope)
            
class ForNode():
    '''
    Defines a node for executing for loops
    Syntax: {% for <var_name> in <itterable_name> %}<stuff>{% end for %}
    '''
    def __init__(self, var_name, itterable_name, true_node):
        self.var_name = var_name
        self.itterable_name = itterable_name
        self.true_node = true_node
    
    def eval(self, scope):
        output = ''
        modified_scope = scope
        itterable = eval(self.itterable_name ,scope)
        for var in itterable:
            modified_scope[self.var_name] = var
            output += str(self.true_node.eval(modified_scope)).strip()
        return output

class Parser(object):
    '''
    Class used to parse a template file into html
    
    >>> Parser("abcd{{1+1}}efgh{% if 1==1 %}2{% end if %}{% if 1==3 %}3{% end if %}1234").eval({})
    'abcd2efgh21234'
    >>> Parser("{% if 1==1 %}2{% end if %}{{5*2}}{% if 1==3 %}3{% end if %}1234").eval({})
    '2101234'
    >>> Parser("{{a+b}}{% if a==d %}{{str(b)*5}}{% end if %}").eval({'a':1, 'b':2, 'c':3, 'd':1})
    '322222'
    >>> Parser("{{a+b}}{% if a==d %}{{str(b)*5}}{% end if %}{% include templating/template_include_test.test %}{{a+b}}{% if a==d %}{{str(b)*5}}{% end if %}").eval({'a':1, 'b':2, 'c':3, 'd':1})
    '322222abcd2efgh212342101234333333333322222'
    >>> Parser("{% for i in items %}{{i}}{% end for %}").eval({'items':[1,2,3]})
    '123'
    >>> Parser("abc{% for i in items %}{{'something'+str(i)}}{% end for %}def").eval({'items':[1,2,3]})
    'abcsomething1something2something3def'
    >>> Parser("abc{% for i in items %}something{{i}}{% end for %}def").eval({'items':[1,2,3]})
    'abcsomething1something2something3def'
    '''
    
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0
        self.length = len(tokens)

    def _parse_python_node(self):
        '''
        Function to parse a python node
        '''
        content = ''
        content += self.tokens[self.index]
        #all everything before the end of the node into content
        while self.read_next() != '}':
            self.next()
            content += self.tokens[self.index]
            if self.is_end():
                raise ParseError("Unexpected end of input.")
        self.next()
        if self.read_next() != '}':
            raise ParseError("'}' expected at end of python node")
        self.next()
        self.next()
        return PythonNode(content)

    def _parse_text_node(self):
        '''
        Function to parse a text node
        '''
        content = ''
        content += self.tokens[self.index]
        while not self.is_end() and self.read_next() != '{':
            self.next()
            content += self.tokens[self.index]
        self.next()
        return TextNode(content)
        
    def _parse_if_node(self):
        '''
        Function to parse an if node
        '''
        predicate = ''
        predicate += self.tokens[self.index]
        #find the predicate for the if statement
        while self.read_next() != '%':
            self.next()
            predicate += self.tokens[self.index]
            if self.is_end():
                raise ParseError("Unexpected end of input.")
        self.next()
        #check for the end of the if decleration
        if self.read_next() != '}':
            raise ParseError("'}' expected")
        self.next() 
        self.next()
        #create a GroupNode for all the stuff in the for loop
        true_node = self._parse_group_node('{% end if %}')
        return IfNode(predicate, true_node)
        
    def _parse_for_node(self):
        '''
        Function to parse a for node
        '''
        var_name = ''
        itterable_name = ''
        var_name += self.tokens[self.index]
        #find the name of the variable to store the value in the itterable
        while self.read_next() != ' ':
            self.next()
            var_name += self.tokens[self.index]
            if self.is_end():
                raise ParseError("Unexpected end of input.")
        #check if the variable name exists
        if var_name=='':
            raise ParseError('Missing variable name.')
        self.next()
        #check for " in "
        if self.tokens[self.index:self.index+4]!= ' in ':
            raise ParseError("'in' expected.")
        self.index+=3
        #find the name of the itterable that is being looped through
        while self.read_next() != ' ':
            self.next()
            itterable_name += self.tokens[self.index]
            if self.is_end():
                raise ParseError("Unexpected end of input.")
        #check if the itterable name exists
        if itterable_name == '':
            raise ParseError("Missing name for itterable.")
        #check for the end of the for decleration
        self.next()
        if self.read_next() != '%':
            raise ParseError("'%' expected")
        self.next()
        if self.read_next() != '}':
            raise ParseError("'}' expected")
        self.next() 
        self.next()
        #create a GroupNode for all the stuff in the foor loop
        true_node = self._parse_group_node('{% end for %}')
        return ForNode(var_name, itterable_name, true_node)
        
    def _parse_include_node(self):
        '''
        Function to parse an include node
        '''
        path = ''
        path += self.tokens[self.index]
        while self.read_next() != '%':
            self.next()
            path += self.tokens[self.index]
            if self.is_end():
                raise ParseError("Unexpected end of input.")
        self.next()
        if self.read_next() != '}':
            raise ParseError("'}' expected")
        self.next() 
        self.next()
        return IncludeNode(path)
    
    def _parse_group_node(self, end):
        '''
        Function to group nodes in similar areas together into group nodes
        '''
        children = []
        while self.tokens[self.index:self.index+len(end)] != end or (end == '' and not self.is_end()):
            if self.is_end():
                return ParseError("Unexpected end of input.")
            if self.tokens[self.index] == '{':
                self.next()
                if self.tokens[self.index] == '{':
                    self.next()
                    children.append(self._parse_python_node())
                
                elif self.tokens[self.index] == '%':
                    self.next()
                    if self.tokens[self.index:self.index+len(IF_TAG)] == IF_TAG:
                        self.index += len(IF_TAG)
                        children.append(self._parse_if_node())
                
                    elif self.tokens[self.index:self.index+len(INCLUDE_TAG)] == INCLUDE_TAG:
                        self.index += len(INCLUDE_TAG)
                        children.append(self._parse_include_node())
                    
                    elif self.tokens[self.index:self.index+len(FOR_TAG)] == FOR_TAG:
                        self.index += len(FOR_TAG)
                        children.append(self._parse_for_node())
                else:
                    raise ParseError("Unexpected token after '{'")
            else:
                children.append(self._parse_text_node())
        self.index += len(end)
        return GroupNode(children)
        
    def parse(self):
        '''
        Function to start parsing
        '''
        node = self._parse_group_node('')
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

def render_template(path, scope):
    with open(path) as p:
        lines=[line.strip() for line in p]
        template=''.join(lines)
    return Parser(template).eval(scope)
  
if __name__ == "__main__":
    import doctest
    doctest.testmod()
