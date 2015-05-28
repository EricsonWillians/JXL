'''
JXL - The Java Extensible Language.
The JXL Interpreter.

Created on 27/05/2015
@author: Ericson Willians (Rederick Deathwill)
'''

from java.io import File
from javax.xml.parsers import DocumentBuilderFactory
from org.w3c.dom import Node;
import sys

class JXLLoader():
    
    def __init__(self, file_name):  
        self.file_name = file_name
        self.file = File(self.file_name)
        self.db_factory = DocumentBuilderFactory.newInstance()
        self.db_builder = self.db_factory.newDocumentBuilder()
        self.doc = self.db_builder.parse(self.file)
        self.doc.getDocumentElement().normalize()

class JXLReader(JXLLoader):
    
    def __init__(self, file_name):
        JXLLoader.__init__(self, file_name)
        self.main_node_list = self.doc.getElementsByTagName("main")
        if self.main_node_list.getLength() == 0:
            raise RuntimeError("There's no <main> tag within the JXL file.")
        self._global = {}
        self.store_globals()
        
    def store_globals(self):
        for i in range(self.main_node_list.getLength()):
            node = self.main_node_list.item(i)
            var = node.getChildNodes()
            if var is not None:
                for j in range(var.getLength()):
                    var_node = var.item(j)
                    if (var_node.getNodeType() == Node.ELEMENT_NODE):
                        self._global[var_node.getNodeName()] = var_node.getTextContent()
        self.determine_types()
                    
    def determine_types(self):
        def extract_number(s):
            try:
                if s.startswith('f'):
                    return float(s[1:])
                else:
                    return int(float(s))
            except ValueError:
                return str(s)
        self._global = {str(name): (lambda x: extract_number(x))(value) for name, value in self._global.items()}
        
if __name__ == '__main__':
    
    jxl = JXLReader("main.xml")
    print("JXL Global Variables: ")
    [sys.stdout.write(name + " <- " + str(value) + "\n") for name, value in jxl._global.items()]  # @UndefinedVariable