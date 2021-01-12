from __future__ import annotations
import pygame

from pygame.event import clear
from pygame.image import load
from IO_Texture import IO_TextureManager
from xml.etree.ElementTree import Element, parse
from IO_Object import IO_Entity, IO_Object
from IO_XmlHandler import IO_XmlHandler
import numpy


class IO_Image(IO_Entity):
    """
    image object
    """
    def __init__(self,name,xmlImage = None) -> None:
        """
        @member source str image filename\n
        @member width int image width\n
        @member height int image heightt
        """
        super().__init__()
        self.source : str = ""
        self.width : float = 0
        self.height : float = 0
        self.name : str = name
        self.surface : pygame.Surface = None

        if(xmlImage != None) : self.parse(self.name, xmlImage)

    def parse(self, name : str, xmlImage : Element) -> None:
        """
        parses xmlImage and sets image attirbutes\n
        @param name str textures id\n
        @param xmlImage Element xmlImage element
        """
        self.source = IO_XmlHandler.getAttribute(xmlImage,'source')
        self.width = int(IO_XmlHandler.getAttribute(xmlImage,'width'))
        self.height = int(IO_XmlHandler.getAttribute(xmlImage,'height'))
        IO_TextureManager.getInstance().textureMap[name]

    def __iter__(self) -> None:
        yield 'class', self.__class__.__name__
        yield 'source', self.source
        yield 'width', self.width
        yield 'height', self.height

class IO_Layer(IO_Entity):
    """
    """
    def __init__(self,xmlLayer = None) -> None:
        """
        @member id int\n
        @member name str\n
        @member width str\n
        @member height str\n
        @member data list[list[int]]
        """
        super().__init__()
        self.id : int
        self.name : str
        self.width : int
        self.height : int 
        self.data : list[list[int]]
    
        if(xmlLayer != None) : self.parse(xmlLayer)

    def parse(self,xmlLayer : Element) -> None:
        """
        parses xmlLayer and sets Layer attirbutes\n
        @param xmlLayer Eelemet 
        """
        self.id = int(IO_XmlHandler.getAttribute(xmlLayer,'id'))
        self.name = IO_XmlHandler.getAttribute(xmlLayer,'name')
        self.width = int(IO_XmlHandler.getAttribute(xmlLayer,'width'))
        self.height = int(IO_XmlHandler.getAttribute(xmlLayer,'height'))

        #gets data element
        xmlData = IO_XmlHandler.getChild(xmlLayer,'data')
        #text to list
        data = IO_XmlHandler.getText(xmlData[0]).split(',')
        
        for i in range(len(data)):
            data[i] = int(data[i]) - 1

        #1d array to 2d array
        self.data = numpy.reshape(numpy.array(data),(self.height,self.width)).tolist()


    def __iter__(self):
        yield 'class', self.__class__.__name__
        yield 'id', self.id
        yield 'name' , self.name
        yield 'width',self.width
        yield 'height',self.height
        yield 'data', self.data


class IO_TileSet(IO_Entity):
    """
    """
    def __init__(self,xmlTileset : Element = None) -> None:
        """
        change tileset
        @param xmlTileset Element
        """
        super().__init__()
        self.firstid : int
        self.name : str
        self.tileWidth : int
        self.tileHeight : int
        self.tileCount : int
        self.columns : int
        self.image : IO_Image

        if(xmlTileset != None) : self.parse(xmlTileset)

    def parse(self,xmlTileset : Element) -> None:
        """
        parses xmlTileset and sets tileset attirbutes\n
        @param xmlTileset Eelemet 
        """
        self.firstid = int(IO_XmlHandler.getAttribute(xmlTileset,'firstgid')) - 1
        self.name = IO_XmlHandler.getAttribute(xmlTileset,'name')
        self.tileWidth = int(IO_XmlHandler.getAttribute(xmlTileset,'tilewidth'))
        self.tileHeight = int(IO_XmlHandler.getAttribute(xmlTileset,'tileheight'))
        self.tileCount = int(IO_XmlHandler.getAttribute(xmlTileset,'tilecount'))
        self.columns = int(IO_XmlHandler.getAttribute(xmlTileset,'columns'))

        xmlImage = IO_XmlHandler.getChild(xmlTileset,'image')[0]
        self.image = IO_Image(self.name,xmlImage)

    def __iter__(self) -> None:
        yield 'class', self.__class__.__name__
        yield 'firstid', self.firstid
        yield 'name', self.name
        yield 'tileWidth' , self.tileWidth
        yield 'tileHeight', self.tileHeight
        yield 'tileCount', self.tileCount
        yield 'columns' , self.columns
        yield 'image' , self.image

class IO_Map(IO_Entity):
    """
    """
    def __init__(self,source : str) -> None:
        """
        map oobject\n
        @member orientation map orientation\n
        @member renderorder str maprender order\n
        @member width  int\n
        @member height int\n
        @member tilewidth int\n
        @member tileHeight int\n
        @member tilesets dict[str,IO_TileSet]\n
        @member layer dict[str,IO_Layer]
        """
        self.orientation : str = "orthogonal"
        self.renderorder : str = "right-down"
        self.width : int = 0
        self.height : int = 0
        self.tileWidth : int = 0
        self.tileHeight : int = 0
        self.tilesets : dict[str,IO_TileSet] = {}
        self.layers : dict[str,IO_Layer] = {}

        self.parse(source)

    def parse(self,source: str): 
        """
        creates map and sets attributes
        """
        xmlMap = IO_XmlHandler.getRoot(source)

        self.orientation = IO_XmlHandler.getAttribute(xmlMap,'renderorder')
        self.renderorder = IO_XmlHandler.getAttribute(xmlMap,'renderorder')
        self.tileWidth = int(IO_XmlHandler.getAttribute(xmlMap,'tilewidth'))
        self.tileHeight = int(IO_XmlHandler.getAttribute(xmlMap,'tileheight'))
        self.width = int(IO_XmlHandler.getAttribute(xmlMap,'width'))
        self.height = int(IO_XmlHandler.getAttribute(xmlMap,'height'))
        

        xmlTilesets = IO_XmlHandler.getChild(xmlMap,'tileset')
        for xmlTileset in xmlTilesets:
            tileset = IO_TileSet(xmlTileset)
            self.tilesets[tileset.name] = tileset

        xmlLayers = IO_XmlHandler.getChild(xmlMap,'layer')

        for xmlLayer in xmlLayers:
            layer =  IO_Layer(xmlLayer)
            self.layers[layer.name] = layer


    def render(self, dt: float = 0) -> None:
        """
        renders map
        """
        #itrates through each layer
        for layerid in self.layers.keys():
            layer = self.layers[layerid]
            #iterates through tilemap
            for i in range(layer.width):
                for j in range(layer.height):
                    
                    #gets tileMap value
                    tileID = layer.data[j][i]
            
                    #if tileID has a blue
                    if tileID != -1:
                       
                        #itrates through tilesets
                        for tilesetID in self.tilesets.keys():
                            #finds the image that tileID belongs to
                            if tileID >= self.tilesets[tilesetID].firstid and tileID < self.tilesets[tilesetID].firstid + self.tilesets[tilesetID].tileCount - 1: 
                                tileID = tileID + self.tilesets[tilesetID].tileCount - (self.tilesets[tilesetID].firstid + self.tilesets[tilesetID].tileCount - 1) - 1

                                
                                #get tilesets
                                tileset = self.tilesets[tilesetID]

                                source = (self.tileWidth, self.tileHeight)
                                
                                dimen = (tileset.image.width,tileset.image.height)
                                destination = (i * self.tileWidth,j * self.tileHeight)
                                
                                frame = int(tileID % tileset.columns)
                                row = int(tileID / tileset.columns)
                                # if (tilesetID == 'element'):
                                #     print(tileset.columns)
                                #     print('frame ',frame)
                                #     print('row ',row)
                                area = pygame.Rect(frame * 16 ,row * 16,self.tileWidth,self.tileHeight)
                                IO_TextureManager.getInstance().textureMap[tileset.name].drawTile(source,destination,frame,row)
                                #IO_TextureManager.getInstance().drawTile(id = tileset.name , source=source , destination=destination , frame = frame , row = row)

    def __iter__(self):
        yield 'class', self.__class__.__name__
        
        yield 'orientation',self.orientation
        yield 'renderorder',self.renderorder
        yield 'width',self.width
        yield 'height',self.height
        yield 'tileWidth',self.tileWidth
        yield 'tileHeight',self.tileHeight

        yield 'tilesets', self.tilesets
        yield 'layer', self.layers


class IO_MapManager(IO_Object):
    __instance = None

    def __init__(self):
        super().__init__()
        """ Virtually private constructor. """
        if IO_MapManager.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            IO_MapManager.__instance = self

        self.maps : dict[str,IO_Map] = {}
    
    def parse(self,source : str):
       xmlRoot = IO_XmlHandler.getRoot(source)
       xmlmaps = IO_XmlHandler.getChild(xmlRoot,"map")
       for xmlmap in xmlmaps:
           id = IO_XmlHandler.getAttribute(xmlmap,"id")
           path = IO_XmlHandler.getAttribute(xmlmap,"source")
           self.load(id,path)

    def load(self,id : str,source : str) -> None:
        self.maps[id] = IO_Map(source)

    def render(self,id : str, dt : int = 0 ) -> None:
        self.maps[id].render(dt)

    def clean(self):
        self.maps.clear()
    
    def drop(self,id):
        self.maps.pop(key=id)

    @staticmethod 
    def getInstance():
        """ Static access method. """
        if IO_MapManager.__instance == None:
            IO_MapManager()
        return IO_MapManager.__instance

