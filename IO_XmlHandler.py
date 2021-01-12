import xml.etree.ElementTree
from xml.etree.ElementTree import Element

class IO_XmlHandler:
    """
    xml handler
    """
    @staticmethod
    def getRoot(path : str)-> Element:
        """
        loads a new xml object\n
        @param path str : 
        """
        tree = xml.etree.ElementTree.ElementTree(file=path)
        return tree.getroot()
    
    @staticmethod
    def getChild(parent : Element ,child : str)->Element:
        """
        get child of parent\n
        @param parent xml : child\n
        @parem child string : child tag to get\n
        @return child list[xml] : list of all children with given child name
        """
        return parent.findall(child)

    @staticmethod 
    def getChildren(parent : Element)->Element:
        """
        get child of parent\n
        @param parent xml : child\n
        @return child list[xml] : list of all children
        """
        return list(parent)

    @staticmethod 
    def getAttributes(tag : str)->Element:
        """
        gets tags attributes\n
        @param tag xml : \n
        @return dict{name-str,value-str} all attribute name and value pair 
        """
        return tag.attrib

    @staticmethod
    def getAttribute(tag,attributes : str)->Element:
        """
        gets a specific tag attributes\n
        @param tag xml :\n
        @param attribute str :
        """
        return tag.attrib[attributes]

    @staticmethod      
    def getText(tag)->str:  
        """
        gets test from tag
        @param tag xml :
        @return tag text  str :
        """
        return tag.text