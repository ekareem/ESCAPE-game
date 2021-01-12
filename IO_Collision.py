from __future__ import annotations
import pygame
from IO_Object import IO_Entity, IO_Object
from IO_Screen import IO_SCREEN_SIZE
from IO_Camera import IO_Camera

class Collider(IO_Object):
    """
    sets collider object
    """
    def __init__(self,x = 0,y = 0, w = 0,h = 0):
        """
        box Rect object collider box
        buffer Rect object collider box helps to shrink box
        """
        super().__init__()
        self.box : pygame.Rect = pygame.Rect(x,y,w,h)
        self.buffer : pygame.Rect = pygame.Rect(x,y,w,h)

    def set(self,x,y,w,h):
        self.box.x = x - self.buffer.x
        self.box.y = y - self.buffer.y
        self.box.w = w - self.buffer.w
        self.box.h = h - self.buffer.h
    
    def setBuffer(self,x,y,w,h):
        self.buffer.x = x
        self.buffer.y = y
        self.buffer.w = w
        self.buffer.h = h

    def render(self,dt:float = 0,color = (255,255,255)):
        cam =  IO_Camera.getInstance().position
        b = pygame.Rect(self.box.x - cam.x,self.box.y - cam.y,self.box.w,self.box.h)

    def __iter__(self):
        yield 'class', self.__class__.__name__
        yield 'box', self.box
        yield 'buffer', self.buffer

class IO_CollisonHandler(IO_Entity):
    __instance = None
    @staticmethod 
    def getInstance():
        """ Static access method. """
        if IO_CollisonHandler.__instance == None:
            IO_CollisonHandler()
        return IO_CollisonHandler.__instance

    
    def setTileMap(self,data : list[list[int]], tileSize : tuple [int,int]):
        self.data = data
        self.tileSize = tileSize
        self.mapSize = (len(data[0]),len(data))

    def CheckCollision(self,a : pygame.Rect,b : pygame.Rect):

        return a.colliderect(b) == 1

    def mapCollision(self,a):
        # tileSize = self.collisonLayer.tileSize
        # rowCount = self.collisonLayer.rowCount
        # colCount = self.collisonLayer.colCount
    
        leftTile = int(a.x/self.tileSize[0])
        rightTile = int((a.x + a.w)/self.tileSize[0]) + 1

        topTile = int(a.y/self.tileSize[1])
        bottomTile = int((a.y + a.h)/self.tileSize[1]) + 1
        if leftTile < 0: leftTile = 0
        if rightTile > self.mapSize[0] : rightTile = self.mapSize[0]

        if topTile < 0 : topTile = 0
        if bottomTile > self.mapSize[1] : bottomTile = self.mapSize[1]
        
        for i in range(topTile,bottomTile):
            for j in range(leftTile, rightTile):
                if(self.data[i][j] > -1):
                    return True
        return False


    def __iter__(self):
        yield 'class', self.__class__.__name__
        yield 'collisonLayer', self.collisonLayer
        yield 'data', self.data

    def __init__(self):
        """ Virtually private constructor. """
        if IO_CollisonHandler.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            IO_CollisonHandler.__instance = self
        super().__init__()
        
        # self.collisonLayer = None
        # self.collisonIndex = collisonIndex
        self.tileSize : tuple[int,int] = ()
        self.mapSize : tuple[int,int] = ()
        self.data = [[]]