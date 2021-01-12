from __future__ import annotations
from ast import parse

from IO_Texture import IO_Texture, IO_TextureManager
from IO_Collision import Collider, IO_CollisonHandler
import pygame
from pygame import transform
from IO_Input import IO_InputHandler
from IO_Animation import IO_Animation, IO_AnimationHandler, IO_SpriteAnimation
from IO_Object import IO_Object
from IO_Physics import IO_Point, IO_RigidBody, IO_Transform, IO_Vector
from IO_Object import IO_Entity
from IO_Texture import FLIP_BOTH,FLIP_HORIZONTAL,FLIP_VERTICAL,FLIP_NONE


class IO_Property(IO_Entity):
    def __init__(self,
                animation : IO_Animation = None,
                texture : IO_Texture = None,
                x : float = 0,
                y : float = 0,
                w : float = 0,
                h : float = 0,
                m : float = 1,
                flip = (False,False)):
        super().__init__()
        """
        """
        self.animation = animation
        self.texture = texture
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.m = m
        self.flip = flip

    def __iter__(self):
        yield 'animation',self.animation
        yield 'texture',self.texture
        yield 'x', self.x
        yield 'y', self.y
        yield 'w', self.w
        yield 'h', self.h
        yield 'flip', self.flip

class IO_Actor(IO_Object):
    def __init__(self,property : IO_Property,name="Dude"):
        super().__init__()
        self.name = name
        self.w : float = property.w
        self.h : float = property.h
        self.flip : list[int,int] = property.flip
        self.animation : IO_Animation = property.animation
        self.texture : IO_Texture = property.texture
        self.transform : IO_Transform = IO_Transform(property.x,property.y)
        self.rigidBody : IO_RigidBody = IO_RigidBody(mass =property.m)
        self.rigidBody.position.x = property.x
        self.rigidBody.position.y = property.y
        self.collider = Collider()
        self.collider.setBuffer(0,0,0,0)
        self.collider.set(self.transform.x,self.transform.y,self.w,self.h)
        self.origin = IO_Point(x=property.x,y=property.y)
        self.lastSafePosition = pygame.Rect(self.transform.x,self.transform.y,self.w,self.h)

    def render(self,dt):
        if self.animation != None:
            self.animation.render(self.transform.x ,self.transform.y)
        if self.texture != None:
            self.texture.draw((self.transform.x,self.transform.y))
        
        self.collider.set(self.transform.x,self.transform.y,self.w,self.h)
       
        self.collider.render(dt)


class IO_ActorManager(IO_Object):
    __instance = None
    
    def __init__(self):
        super().__init__()
        """ Virtually private constructor. """
        if IO_ActorManager.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            IO_ActorManager.__instance = self

        self.actorMap : dict[str,IO_Actor] = {}

    def parse(self,source):
        pass

    def update(self,dt):
        k = list(self.actorMap.keys())
        
        for actor in self.actorMap.values():
             actor.update(dt)

    def render(self,dt):
        for actor in self.actorMap.values():
            actor.render(dt)

    @staticmethod
    def getInstance():
        """ Static access method. """
        if IO_ActorManager.__instance == None:
            IO_ActorManager()
        return IO_ActorManager.__instance
