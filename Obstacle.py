from __future__ import annotations
from IO_Collision import IO_CollisonHandler


from pygame.display import update
from IO_Animation import IO_Animation, IO_AnimationHandler

from pygame import transform
import pygame
from IO_Texture import IO_TextureManager
from IO_Physics import IO_Point, IO_Vector
from IO_Actor import IO_Actor, IO_ActorManager, IO_Property

class Obstacle(IO_Actor):
    def __init__(self,property : IO_Property,name):
        super().__init__(property)
        self.name = name

    def render(self,dt):
        if self.animation != None:
            self.animation.render(self.transform.x ,self.transform.y)
        if self.texture != None:
            self.texture.draw((self.transform.x,self.transform.y))
        
        self.collider.render(dt)


class Button(IO_Actor):
    def __init__(self,x : int, y : int,name):
        super().__init__(IO_Property(animation=IO_AnimationHandler.getInstance().animationMap["trigger_2"],x = x, y = y ,w = 32, h = 32),name)
        self.isPressed = False
        self.animation.pause = True
        

    def update(self,dt,game):
        self.animation.update()
        if(self.isPressed == True):
            self.animation.pause = False
            self.animation.repeat = False
        
        for actor in game.level.characters.values():
            if IO_CollisonHandler.getInstance().CheckCollision(actor.collider.box,self.collider.box):
                self.isPressed = True
            
    def animationState(self):
        pass

class Barrier(IO_Actor):
    def __init__(self,x : int, y : int,w : int,h : int, num:int, force:IO_Vector = IO_Vector(y=-3)):
        super().__init__( IO_Property(texture=IO_TextureManager.getInstance().textureMap["obstacle"],x = x, y = y ,w = w, h = h), name="Barrier"+str(num))
        self.buttons : list[Button] = []
        self.force : IO_Vector = force
        self.startingpos = IO_Point(self.transform.x,self.transform.y)
        self.opentime = 40

    def update(self,dt,game):
        if (self.allPressed() and self.opentime > 0):
            pass
            self.rigidBody.applyForce(self.force)
    
            self.rigidBody.update(dt)
            self.transform.translateY(self.rigidBody.position.y)
            self.transform.translateX(self.rigidBody.position.x)
            self.collider.set(self.transform.x,self.transform.y,self.w,self.h)

            self.opentime -= dt
        for button in self.buttons:
            button.update(dt,game)
            button.animation.update(dt)

    def allPressed(self):
        for button in self.buttons:
            if button.isPressed == False:
                return False
        return True

    def render(self, dt):
        
        if self.opentime > 0 :
            if self.animation != None:
                self.animation.render(self.transform.x ,self.transform.y)
            if self.texture != None:
                area = pygame.Rect(0,0,self.w,self.h)
                self.texture.draw((self.transform.x,self.transform.y),area)
            
            
            self.collider.render(dt)
            
        for button in self.buttons:
            button.render(dt)

    def animationState(self):
        pass

class Spike(IO_Actor):
    def __init__(self,x:int,y:int,w:float,h:float,num):
        super().__init__(IO_Property(x=x ,y=y, w = w, h= h),name="Spike"+str(num))

    def update(self,dt,game):
       for actor in game.level.characters.values():
            if(actor.isDead == False):
                if IO_CollisonHandler.getInstance().CheckCollision(actor.collider.box,self.collider.box):
                    actor.isDead = True
    