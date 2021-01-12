from __future__ import annotations
import pygame
from IO_Object import IO_Entity

IO_TARGET_FPS = 60
IO_TARGET_DT = 1.5

class IO_Timer(IO_Entity):
    __instance = None


    def __init__(self):
        super().__init__()
        if IO_Timer.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            IO_Timer.__instance = self

        self.deltaTIme : float = 0
        self.lastTime : float = 0
        self.targetFps : float = IO_TARGET_FPS
        self.tergetDT : float = IO_TARGET_DT
        self.clock :pygame.time.Clock = None

    def init (self,targetFps : float = IO_TARGET_FPS , targetDt : float = IO_TARGET_DT) -> None:
        """
        """
        self.targetFps = targetFps
        self.targetDt = targetDt
        #self.clock = pygame.time.Clock()

    def tick(self):
        """
        """
        self.deltaTIme = (pygame.time.get_ticks() - self.lastTime) * (self.targetFps /1000.0)
        if(self.deltaTIme > self.targetDt): self.deltaTIme = self.targetDt
        self.lastTime = pygame.time.get_ticks()
        
    def __iter__(self):
        yield 'class',self.__class__.__name__
        yield 'deltaTIme',self.deltaTIme 
        yield 'lastTime',self.lastTime 
        yield 'targetFps',self.targetFps 
        yield 'tergetDT',self.tergetDT 

    @staticmethod 
    def getInstance():
        if IO_Timer.__instance == None:
            IO_Timer()
        return IO_Timer.__instance

