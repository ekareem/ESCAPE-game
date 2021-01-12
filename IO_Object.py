from __future__ import annotations

import pygame

"""
interface class defines actions of game entities
"""
class IO_Entity:
    """
    @purpoe : base entity object
    """
    def __init__(self):
        self.origin : pygame.Rect = pygame.Rect(0,0,0,0)

    def getEntity(self,
        name : str ,
        entity : IO_Entity) -> IO_Entity | None:

        raise NotImplementedError()

    def __str__(self): 
        return str(dict(self))

    def __repr__(self):
        return str(self)

    def __iter__(self):
        yield 'class', self.__class__.__name__

class IO_Object(IO_Entity):
    """
    @purpose : defines abstaction for entity objects
    """
    def __init__(self) -> None:
        super().__init__()
        self.entites : dict[str : IO_Entity] = {}

    def getEntity(self,
        name : str ,
        entity : IO_Entity) -> IO_Entity | None:
        """
        """
        self.entites[name] = entity
        return entity
    
    def update(self, dt : float = 0.0) -> None:
        """
        @purpose : updates entitiy attributes\n
        @param[0] : self IO_Object\n
        @param[1] : dt delta time\n
        """
        raise NotImplementedError()

    def event(self, dt : float = 0.0) -> None:
        """
        @purpose : handles event\n
        @param[0] : self IO_Object\n
        @param[1] : dt delta time\n
        """
        raise NotImplementedError()

    def render(self, dt : float = 0.0) -> None:
        """
        @purpose : renders entity\n
        @param[0] : self IO_Object\n
        @param[1] : dt delta timen\n
        """
        raise NotImplementedError()

    def clean(self) -> None:
        """
        @purpose : clean entity\n
        @param[0] : self IO_Object\n
        @param[1] : dt delta time\n
        """
        raise NotImplementedError()

    def __iter__(self):
        yield 'IO_Entity' , self.__class__.__name__
       