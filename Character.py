from __future__ import annotations
from IO_Mixer import IO_MusicManager
from IO_Camera import IO_Camera
from Projectile import Arrow, Ice, Projectile, Stone

from IO_Object import IO_Entity

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
from IO_Actor import IO_Actor,IO_Property,IO_ActorManager

JUMP_TIME = 12
JUMP_FORCE = 7
RUN_FORCE = 4.0
ATTACK_TIME = 20.0

class IO_Character(IO_Actor):
    """
    """
    def __init__(self,property : IO_Property,name="Dude" ,jumpTime=JUMP_TIME,jumpForce=JUMP_FORCE,attackTime = ATTACK_TIME ):
        super().__init__(property,name)
        self.rigidBody.gravity.y = 2
        self.isRunning = False
        self.isJumping= False
        self.isGrounded = True
        self.isAttacking = False
        self.facingRight = True
        self.jumpTime = jumpTime
        self.jumpForce = jumpForce
        self.attackTime = attackTime
        self.isFalling = False
        self.isPushing = False
        self.collider.setBuffer(-6,-2,12,4)
        self.groundedcollider = Collider()
        self.groundedcollider.setBuffer(-6,-22,12,24)
        self.groundedcollider.set(self.transform.x,self.transform.y,self.w,self.h)
        self.isDead = False
        self.oldDead = False
        self.isFrozen = False
        self.dance = False
    
    def update(self,dt,game):
        pass

    def render(self,dt=0):
        #super().render(dt)

        if (self.isFrozen):
            cam = IO_Camera.getInstance().position
            pygame.draw.rect(pygame.display.get_surface(),(135,206,250),(self.transform.x-cam.x,self.transform.y-cam.y,self.w,self.h))

        if (self.animation != None):
            self.animation.render(self.transform.x ,self.transform.y -2)
        if self.texture != None:
            self.texture.draw((self.transform.x,self.transform.y - 10))

        self.collider.set(self.transform.x,self.transform.y,self.w,self.h)
        self.collider.render(dt)
        
        self.groundedcollider.render(dt,color=(0,0,225))
        
    def animationState(self):
        if (self.animation != None):
            self.animation.setAttrib(flip=self.flip) 

        if (self.isFrozen):
            self.collider.setBuffer(0,0,0,2)
        

        if (self.isDead):
            self.animation = IO_AnimationHandler.getInstance().animationMap[self.name+"_Monster"]
            if self.oldDead == False:
                self.animation.setAttrib(rotation=90)
                if(self.isFrozen == False):
                    self.collider.setBuffer(-6,-2,12,20)
            self.oldDead = True
            return


        if(self.isRunning == False):
            self.animation = IO_AnimationHandler.getInstance().animationMap[self.name+"_Monster_Idle_4"]

        if(self.isRunning):
            self.animation = IO_AnimationHandler.getInstance().animationMap[self.name+"_Monster_Run_6"]
    

        if self.isJumping:
            self.animation = IO_AnimationHandler.getInstance().animationMap[self.name+"_Monster_Jump_4"]
        
        if self.isFalling:
            self.animation = IO_AnimationHandler.getInstance().animationMap[self.name+"_Monster_Fall_4"]
        
        if self.isPushing:
            self.animation = IO_AnimationHandler.getInstance().animationMap[self.name+"_Monster_Push_6"]

        if self.dance:
            self.animation = IO_AnimationHandler.getInstance().animationMap[self.name+"_Monster_Climb_4"]

        if self.isAttacking:
            self.animation = IO_AnimationHandler.getInstance().animationMap[self.name+"_Monster_Throw_4"]

    def attack(self):
        pass
        
class Dude(IO_Character):
    def __init__(self,property : IO_Property ,jumpTime=JUMP_TIME,jumpForce=JUMP_FORCE,attackTime = ATTACK_TIME):
        super().__init__(property,name="Dude" ,jumpTime=jumpTime,jumpForce=jumpForce,attackTime = attackTime)
        self.projectiles : list[Projectile] = []

    def attack(self):
        IO_MusicManager.getInstance().playEffect("shoot")
        axis = 1
        if self.flip == FLIP_HORIZONTAL:
            axis = -1
        object = Ice(IO_Property(x= self.transform.x,y=self.transform.y + 12,w=16,h=16),name="ice",axis=axis)
        self.projectiles.append(object)

    def update(self,dt,game):
        for projectile in self.projectiles:
            projectile.update(dt,game)
            #print(projectile.rigidBody)
    
    def render(self, dt):
        super().render(dt)
        for projectile in self.projectiles:
            projectile.render(dt)

    
class Pink(IO_Character):
    def __init__(self,property : IO_Property ,jumpTime=JUMP_TIME,jumpForce=JUMP_FORCE,attackTime = ATTACK_TIME):
        super().__init__(property,name="Pink" ,jumpTime=jumpTime,jumpForce=jumpForce,attackTime = attackTime)
        self.projectiles : list[Projectile] = []

    def attack(self):
        IO_MusicManager.getInstance().playEffect("arrow")
        axis = 1
        if self.flip == FLIP_HORIZONTAL:
            axis = -1
        object = Arrow(IO_Property(x= self.transform.x,y=self.transform.y + 12,w=16,h=16),axis=axis)
        self.projectiles.append(object)

    def update(self,dt,game):
        for projectile in self.projectiles:
            projectile.update(dt,game)
            #print(projectile.rigidBody)
    
    def render(self, dt):
        super().render(dt)
        for projectile in self.projectiles:
            projectile.render(dt)

class Owlet(IO_Character):
    def __init__(self,property : IO_Property ,jumpTime=JUMP_TIME,jumpForce=JUMP_FORCE,attackTime = ATTACK_TIME):
        super().__init__(property,name="Owlet" ,jumpTime=jumpTime,jumpForce=jumpForce,attackTime = attackTime)
        self.projectiles : list[Projectile] = []
    def attack(self):
        IO_MusicManager.getInstance().playEffect("laser")
        axis = 1
        if self.flip == FLIP_HORIZONTAL:
            axis = -1
        object = Stone(IO_Property(x= self.transform.x,y=self.transform.y + 12,w=16,h=16),axis=axis)
        self.projectiles.append(object)

    def update(self,dt,game):
        for projectile in self.projectiles:
            projectile.update(dt,game)
            #print(projectile.rigidBody)
    
    def render(self, dt):
        super().render(dt)
        for projectile in self.projectiles:
            projectile.render(dt)