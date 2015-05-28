'''
JXL - The Java Extensible Language.
The JXL Interpreter.

Created on 27/05/2015
@author: Ericson Willians (Rederick Deathwill)
'''

from java.io import File
from javax.xml.parsers import DocumentBuilderFactory
import sys

class JXLLoader():
    
    def __init__(self, file_name):  
        self.file_name = file_name
        self.file = File(self.file_name)
        self.db_factory = DocumentBuilderFactory.newInstance()
        self.db_builder = self.db_factory.newDocumentBuilder()
        self.doc = self.db_builder.parse(self.file)
        self.doc.getDocumentElement().normalize()
        
class JXLScope(dict):
    
    def __init__(self, *args):
        dict.__init__(self, args)
        
    def __getitem__(self, key):
        return dict.__getitem__(self, key)
    
    def __setitem__(self, key, value):
        dict.__setitem__(self, key, value)
        
class JXLReader(JXLLoader):
    
    def __init__(self, file_name):
        JXLLoader.__init__(self, file_name)
        self.outer_scopes = JXLScope()
        self.root = self.doc.getElementsByTagName("JXL")
        if self.root.getLength() == 0:
            raise RuntimeError("The JXL file has no <JXL> root tag.")
        self.children = self.root.item(0).getChildNodes()
        for i in range(self.children.getLength()):
            node = self.children.item(i)
            node_name = str(node.getNodeName())
            if node_name not in ["#text", "#comment"]:
                self.outer_scopes[node_name] = JXLScope()
                _vars = node.getChildNodes()
                for j in range(_vars.getLength()):
                    var = node.item(j)
                    var_name = str(var.getNodeName())
                    if var_name not in ["#text", "#comment"]:
                        self.outer_scopes[node_name][var_name] = var.getTextContent()
        self.preprocess_types()
        self.evaluate()
        
    def preprocess_types(self):
        def extract_number(s):
            try:
                if s.startswith('f'):
                    return float(s[1:])
                else:
                    return int(float(s))
            except ValueError:
                return str(s)
        for node_name in self.outer_scopes.keys():
            self.outer_scopes[node_name] = {
                str(name): (lambda x: extract_number(x))(value) for name, value in self.outer_scopes[node_name].items()}
         
    def evaluate(self):
        for node_name in self.outer_scopes.keys():
            try:
                self.outer_scopes[node_name] = {str(name): (lambda x: eval(str(x), globals(), self.outer_scopes[node_name]))(value) for name, value in self.outer_scopes[node_name].items()}
            except SyntaxError:
                raise RuntimeError("JXL Error: An invalid expression was used.")
        
if __name__ == '__main__':
    
    jxl = JXLReader("main.xml")
    print(jxl.outer_scopes)