from __future__ import annotations
from IO_Object import IO_Object
import pygame

IO_SCREEN_SIZE : tuple = (960,640)
IO_SCREEN_TITLE : str = 'IO_title'
IO_SCREEN_COLOR : tuple = (0,28,61,255)

class IO_Screen(IO_Object):
    __instance = None

    def __init__(self) -> IO_Screen| None:
        """
        intitilize IO_Screen
        @member surface pygame.surface
        @member size tuple[int,int] 
        @member title str
        @member color tuple[int,int,int,int]
        @member running bool 
        """
        super().__init__()
        if IO_Screen.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            IO_Screen.__instance = self
        
        self.surface : pygame.Surface = None
        self.size : tuple[int,int] = IO_SCREEN_SIZE
        self.title: str = IO_SCREEN_TITLE
        self.color: tuple[int,int,int,int] = IO_SCREEN_COLOR
        self.running : bool = False

    def init(self,
        screenSize : tuple[int,int] = IO_SCREEN_SIZE,
        screenColor : tuple[int,int,int,int] = IO_SCREEN_COLOR,
        screenTitle : str = IO_SCREEN_TITLE) -> None :
        """
        @purpose initlize IO_Screen member variable\n
        @param[0] self IO_Screen\n
        @param[1] self screenSize\n
        @param[2] self screenColor\n
        @param[3] self screenTitle\n
        """
        self.size = screenSize
        self.color = screenColor
        self.title = screenTitle
        self.running = True

        self.surface = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.title)

    def event(self, dt: float = 0.0) -> None:
        """
        @purpose : handles event\n
        @param[0] : self IO_Object\n
        @param[1] : dt delta time\n
        """
        pass

    def render(self, dt: float = 0.0) -> None:
        """
        @purpose : renders entity\n
        @param[0] : self IO_Object\n
        @param[1] : dt delta timen\n
        """
        self.surface.fill(self.color)

    def __iter__(self):
        yield 'class', self.__class__.__name__
        yield 'entities', self.entites
        yield 'color', self.color
        yield 'running',self.running
        yield 'size',self.size
        yield 'surface',self.surface
        yield 'title',self.title

    @staticmethod 
    def getInstance():
        if IO_Screen.__instance == None:
            IO_Screen()
        return IO_Screen.__instance