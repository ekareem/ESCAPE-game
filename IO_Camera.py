import pygame
from IO_Object import IO_Entity, IO_Object
from IO_Physics import IO_Point
from IO_Physics import IO_Vector
from IO_Screen import IO_SCREEN_SIZE

class IO_Camera(IO_Object):
    __instance = None
    @staticmethod 
    def getInstance():
        """ Static access method. """
        if IO_Camera.__instance == None:
            IO_Camera()
        return IO_Camera.__instance
    
    def init(self,screenSize = IO_SCREEN_SIZE):
        self.target = IO_Point()
        self.position = IO_Vector()
        self.viewBox = pygame.Rect(0,0,screenSize[0],screenSize[1])
        self.screenSize = screenSize

    def update(self,dt):
        if self.target != None:
            
            self.viewBox.x =  int(self.target.origin.x - self.screenSize[0] / 2)
            self.viewBox.y =  int(self.target.origin.y - self.screenSize[1] / 2)
            
            self.position.x, self.position.y = self.viewBox.x,self.viewBox.y

    def __iter__(self):
        yield 'class', self.__class__.__name__
        yield 'target', self.target
        yield 'position', self.position
        yield 'viewBox', self.viewBox
        yield 'screenSize', self.screenSize


    def __init__(self):
        """ Virtually private constructor. """
        if IO_Camera.__instance != None:
            raise Exception("This class is a IO_Camera!")
        else:
            IO_Camera.__instance = self
        super().__init__()
        self.target = None
        self.position = IO_Vector()
        self.viewBox = pygame.Rect(0,0,0,0)
        self.screenSize = IO_SCREEN_SIZE