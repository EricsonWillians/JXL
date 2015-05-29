#! /usr/bin/env jython

'''
JXL - The Java Extensible Language.
The JXL Interpreter.

Created on 27/05/2015 
@author: Ericson Willians (Rederick Deathwill)
'''

from java.io import File
from java.nio.file import Paths
from javax.xml.parsers import DocumentBuilderFactory
import sys

class JXLLoader():
    
    def __init__(self, file_name):
        path = Paths.get(file_name)
        self.file_name = path.toAbsolutePath().toString()
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
                        if var_name == "print":
                            try:
                                print(self.outer_scopes[node_name][var.getTextContent()])
                            except KeyError:
                                print(var.getTextContent())
                        elif var_name == "python":
                            exec(var.getTextContent()) in globals(), self.outer_scopes[node_name]
                        else:
                            self.outer_scopes[node_name][var_name] = eval(
                                var.getTextContent(), globals(), self.outer_scopes[node_name])
        
if __name__ == '__main__':
    
    if len(sys.argv) == 2:
        jxl = JXLReader(sys.argv[1])
    #    print(jxl.outer_scopes)
    else:
        raise RuntimeError("JXL Error: No path to XML file provided.")