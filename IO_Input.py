from __future__ import annotations
from IO_Screen import IO_Screen
import pygame
from IO_Object import IO_Entity

class IO_InputHandler(IO_Entity):
    """
    """
    __instance : IO_InputHandler = None
    def __init__(self) -> IO_InputHandler:
        """
        initalize IO_input
        """
        if IO_InputHandler.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            IO_InputHandler.__instance = self

        self.event = pygame.event.get()
    
    def listen(self) -> pygame.event.Event:
        """
        @purpose listens to events\n
        @param engine IO_Engine\n
        """
        self.event = pygame.event.get()
        for event in self.event:
            if event.type == pygame.QUIT:
                IO_Screen.getInstance().running =False
            elif event.type == pygame.KEYDOWN:
                pass
            elif event.type == pygame.KEYUP:
                pass
            return event
        return None
        
    
    def isPressed(self,key : int) -> bool:
        """
        @purpose checks if key is pressed\n
        @param key int positon of key presssed\n
        """
        return pygame.key.get_pressed()[key] == 1

    def mousePressed(self,key) -> bool:
        return pygame.mouse.get_pressed()[key] == 1
        
    @staticmethod 
    def getInstance() -> IO_InputHandler:
        if IO_InputHandler.__instance == None:
            IO_InputHandler()
        return IO_InputHandler.__instance

