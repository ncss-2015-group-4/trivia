'''
PROPERTY OF THE HOLY SOCIETY OF TEMPLATEIA. UNAUTHORISED EDITING WILL BE PROSECUTED

This code parses the templates into python and html.
The python code can then be evaluated and added to the html to be displayed by a web browser
'''
import html
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
        #stuff inside the node
        self.content = content
    def eval(self, scope):
        raise NotImplementedError()

class PythonNode(Node):
    '''
    Defines a node for the execution of python code
    Syntax: {{ python_expression }}
    '''
    def eval(self, scope):
        #return the execution of the python code
        return html.escape(str(eval(self.content, scope)))

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
        #List of nodes that the group node contains
        self.children = children
    def eval(self, scope):
        result = ''
        #Evaluate all the child nodes and add them to output
        for node in self.children:
            result += str(node.eval(scope))
        return result
 
class IfNode(Node):
    '''
    Defines a node for execution if statements
    Syntax: {% if <condition> %}stuff{% end if %}
    '''
    def __init__(self, predicate, true_node):
        #Part to be evaluated to true or false
        self.predicate = predicate
        #Group node to be executed if the predicate is true
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
        #Path to the file to be included
        self.path = path.strip()

    def eval(self, scope):
        #Open the file
        with open(self.path) as p:
            #Read the file
            lines = [line.strip() for line in p]
            template = ''.join(lines)
        #return the evaluation of the file
        return Parser(template).eval(scope)

class ForNode(Node):
    '''
    Defines a node for executing for loops
    Syntax: {% for <var_name> in <itterable_name> %}<stuff>{% end for %}
    '''
    def __init__(self, var_name, itterable_name, true_node):
        #Name of the variable to store content from the itterable
        self.var_name = var_name
        #Varible to be itterated over
        self.itterable_name = itterable_name
        #Group node to be executed in every itteration
        self.true_node = true_node

    def eval(self, scope):
        output = ''
        modified_scope = scope
        #Get the itterable
        itterable = eval(self.itterable_name, scope)
        #Itterate over the itterable
        for var in itterable:
            #Set var_name to be the contents of the current position in itterable
            modified_scope[self.var_name] = var
            #Evaluate the group node and concatenate it to the output
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
        #String to be parsed
        self.tokens = tokens
        #Current position in tokens
        self.index = 0
        #Length of tokens
        self.length = len(tokens)

    def _parse_python_node(self):
        '''
        Function to parse a python node
        '''
        content = ''
        #Add the current position to the content
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
        #Add the current token to content
        content += self.tokens[self.index]
        #Keep adding to content until a '{' is reached
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
        if var_name == '':
            raise ParseError('Missing variable name.')
        self.next()
        #check for " in "
        if self.tokens[self.index:self.index+4] != ' in ':
            raise ParseError("'in' expected.")
        self.index += 3
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
        #Add current token to that path of file to be included
        path += self.tokens[self.index]
        while self.read_next() != '%':
            #Add to the path until an '%' is reached
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
        #While not at the end of the node, or the end of the file
        while self.tokens[self.index:self.index+len(end)] != end or (end == '' and not self.is_end()):
            if self.is_end():
                return ParseError("Unexpected end of input.")
            #check for a '{'
            if self.tokens[self.index] == '{':
                self.next()
                #if there is another '{' it must be a python statement
                if self.tokens[self.index] == '{':
                    self.next()
                    children.append(self._parse_python_node())
                #If there is a '%' it could be include, if, or for
                elif self.tokens[self.index] == '%':
                    self.next()
                    #Check if it is an if
                    if self.tokens[self.index:self.index+len(IF_TAG)] == IF_TAG:
                        self.index += len(IF_TAG)
                        children.append(self._parse_if_node())
                    #check if it is an include
                    elif self.tokens[self.index:self.index+len(INCLUDE_TAG)] == INCLUDE_TAG:
                        self.index += len(INCLUDE_TAG)
                        children.append(self._parse_include_node())
                    #check if it is a for
                    elif self.tokens[self.index:self.index+len(FOR_TAG)] == FOR_TAG:
                        self.index += len(FOR_TAG)
                        children.append(self._parse_for_node())
                else:
                    #Otherwise it is an error
                    raise ParseError("Unexpected token after '{'")
            else:
                #If there was not a '{' then it is a text node
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
        '''
        Return the next character in tokens
        '''
        return self.tokens[self.index + 1]

    def is_end(self):
        '''
        Check if we are at the ned of tokens
        '''
        return self.index >= self.length - 1

    def next(self):
        '''
        Incriment the current index
        '''
        self.index += 1

def render_template(path, scope):
    '''
    Function which uses the Parser class to parse a html file
    '''
    with open(path) as p:
        lines = [line.strip() for line in p]
        template = ''.join(lines)
    return Parser(template).eval(scope)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
