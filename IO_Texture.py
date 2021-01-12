from __future__ import annotations
from IO_XmlHandler import IO_XmlHandler

from pygame.transform import flip, rotate, scale
from IO_Object import IO_Object,IO_Entity
from IO_Camera import IO_Camera
from IO_Screen import IO_Screen
import pygame

FLIP_HORIZONTAL = (True,False)
FLIP_VERTICAL = (False,True)
FLIP_NONE = (False,False)
FLIP_BOTH = (True,True)

class IO_Texture(IO_Entity):
    def __init__(self, id : str, w : int , h : int,  texture : pygame.Surface, scale :tuple[int,int] = (1,1), angle :float =0,flip :tuple[int,int]=(False,False)):
        self.id : str = id
        self.w = w
        self.h = h
        self.scale = scale
        self.angle = angle
        self.flip = flip
        self.texture : pygame.Surface = texture
    
    def transform(self,
            scale : tuple[sx: int , sy: int] = None,
            angle : float = None,
            flip : tuple [bool,bool] = None):

        # if flip != None: 
        #     self.texture = pygame.transform.flip(self.texture,flip[0],flip[1])
        if flip != None: self.flip = flip
        if angle != None: 
            self.texture = pygame.transform.rotate(self.texture,angle)
            self.angle = angle
        if scale != None: 
            self.texture = pygame.transform.scale(self.texture, (int(self.w * scale[0]),int(self.h * scale[1])))
            self.scale = scale

    def draw(self,
        destination : tuple[int,int],
        area : pygame.Rect = None,
        scrollRatio : float = 1,
        screenPos = False):
        """
        draw sprite\n
        @param id str : sprite id\n
        @param area pygame.Rect : area of sprite to draw from picture\n
        @param destination tuple(int,int) where to draw spriten\n
        """

        texture = pygame.transform.flip(self.texture,self.flip[0],self.flip[1])
        if screenPos == False:
            cam  = IO_Camera.getInstance().position * scrollRatio
            destination = (destination[0] - cam.x,destination[1] - cam.y)
        
        screen = screen = IO_Screen.getInstance().surface

        if area == None: area = pygame.Rect(0, 0 , self.w * self.scale[0], self.h * self.scale[1])
        
        screen.blit(texture,destination,area)
        pygame.sprite.Group().draw(screen)
    
    def drawFrame(self,
        source : tuple['w' :int,'h' :int],
        destination: tuple['x' :int,'y' :int],
        frame : int,
        row : int,
        scrollRatio : float = 1,
        screenPos = False):
        """
        draw sprite\n
        @param source tuple(int,int) frame width and height\n 
        @param destination tuple(int,int) where to draw spriten\n
        @param frame int frame\n
        @param row int row\n
        """
        texture = pygame.transform.flip(self.texture,self.flip[0],self.flip[1])
        if screenPos == False:
            cam  = IO_Camera.getInstance().position * scrollRatio
            destination = (destination[0] - cam.x, destination[1] - cam.y)
        screen = IO_Screen.getInstance().surface
        
        area = pygame.Rect(frame * source[0] , row * source[1] , source[0] , source[1])
    
        screen.blit(texture,destination,area)
        pygame.sprite.Group().draw(screen)

    def drawTile(self,
        source : tuple['w' :int,'h' :int],
        destination: tuple['x' :int,'y' :int],
        frame : int,
        row : int,
        scrollRatio : float = 1,
        screenPos = False):
        """
        draw sprite\n
        @param source tuple(int,int) frame width and height\n 
        @param destination tuple(int,int) where to draw spriten\n
        @param frame int frame\n
        @param row int row\n
        """
        texture = pygame.transform.flip(self.texture,self.flip[0],self.flip[1])
        if screenPos == False:
            cam  = IO_Camera.getInstance().position * scrollRatio
            destination = (destination[0] - cam.x, destination[1] - cam.y)
        screen = IO_Screen.getInstance().surface
        
        area = pygame.Rect(frame * source[0] , row * source[1] , source[0] , source[1])

        screen.blit(texture,destination,area)
        pygame.sprite.Group().draw(screen)
    
        
class IO_TextureManager(IO_Object):
    __instance = None

    def __init__(self):
        super().__init__()
        """ Virtually private constructor. """
        if IO_TextureManager.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            IO_TextureManager.__instance = self

        self.textureMap : dict[str,IO_Texture]= {}

    def init(self, textureMap : dict[str,pygame.Surface] = {}):
        self.textureMap = textureMap
    
    def load(self,id : str,filename : str,w : int, h : int, scale = (1,1), angle = 0, flip = (False,False)):
        texture = pygame.image.load(filename)
        texture = pygame.transform.flip(texture,flip[0],flip[1])
        texture = pygame.transform.rotate(texture,angle)
        texture = pygame.transform.scale(texture, (int(w * scale[0]),int(h * scale[1])))
        self.textureMap[id] = IO_Texture(id,w,h,texture,scale,angle,flip)
        

    def parse(self,source):
        xmlroot = IO_XmlHandler.getRoot(source)
        xmlTextures = IO_XmlHandler.getChild(xmlroot,'texture')
        for xmlTexture in xmlTextures:
            id = IO_XmlHandler.getAttribute(xmlTexture,'id')
            w = float(IO_XmlHandler.getAttribute(xmlTexture,'w'))
            h = float(IO_XmlHandler.getAttribute(xmlTexture,'h'))
            source = IO_XmlHandler.getAttribute(xmlTexture,'source')
            scaleX = float(IO_XmlHandler.getAttribute(xmlTexture,'scaleX'))
            scaleY = float(IO_XmlHandler.getAttribute(xmlTexture,'scaleY'))
            angle = float(IO_XmlHandler.getAttribute(xmlTexture,'angle'))

            flipX =  IO_XmlHandler.getAttribute(xmlTexture,'flipX') == 'True'
            flipY = IO_XmlHandler.getAttribute(xmlTexture,'flipY') == 'True'
            
            self.load(id,source,w,h,scale=(scaleX,scaleY),angle=angle,flip=(flipX,flipY))


    def transform(self,id:str,
            scale : tuple[w: int , h: int , sx: int , sy: int] = None,
            angle : float = None,
            flip : tuple [bool,bool] = None):

        texture = self.textureMap[id].texture
        if flip == None: texture = pygame.transform.flip(texture,flip[0],flip[1])
        if angle == None: texture = pygame.transform.rotate(texture,angle)
        if scale == None: texture = pygame.transform.scale(texture, (int(scale[0] * scale[2]),int(scale[1] * scale[3])))
        

    def draw(self,
        id : str,
        area : pygame.Rect,
        destination : tuple[int,int] = (0,0),
        scrollRatio : float =1):
        """
        draw sprite\n
        @param id str : sprite id\n
        @param area pygame.Rect : area of sprite to draw from picture\n
        @param destination tuple(int,int) where to draw spriten\n
        """

        self.textureMap[id].draw(destination=destination,area=area,scrollRatio=scrollRatio)

    def drawFrame(self,
        id : str ,
        source : tuple['w' :int,'h' :int],
        destination: tuple['x' :int,'y' :int] = (0,0),
        frame : int = 0,
        row : int = 0,
        scrollRatio : float =1):
        """
        draw sprite\n
        @param id str : sprite id\n
        @param source tuple(int,int) frame width and height\n 
        @param destination tuple(int,int) where to draw spriten\n
        @param frame int frame\n
        @param row int row\n
        """

        self.textureMap[id].drawFrame(source=source,destination=destination,frame=frame,row=row,scrollRatio=scrollRatio)

    def drawTile(self,
        id : str ,
        source : tuple['w' :int,'h' :int],
        destination: tuple['x' :int,'y' :int] = (0,0),
        frame : int = 0,
        row : int = 0,
        scrollRatio : float =1):
        """
        draw sprite\n
        @param id str : sprite id\n
        @param source tuple(int,int) frame width and height\n 
        @param destination tuple(int,int) where to draw spriten\n
        @param frame int frame\n
        @param row int row\n
        """
        self.textureMap[id].drawTile(source=source,destination=destination,frame=frame,row=row,scrollRatio=scrollRatio)

    def drop(self,id : str) -> None:
        """
        drops surface from map\n
        @param id texture id to drop
        """
        self.textureMap.pop(id)

    def clean(self) -> None:
        """
        removes all textures
        """
        self.textureMap.clear()

    def __iter__(self) -> None:
        yield 'class', self.__class__.__name__
        yield 'entities', self.entites
        yield 'textureMap', self.textureMap

    @staticmethod 
    def getInstance():
        """ Static access method. """
        if IO_TextureManager.__instance == None:
            IO_TextureManager()
        return IO_TextureManager.__instance

