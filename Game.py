
from __future__ import annotations
from IO_Mixer import IO_MusicManager
import copy
from IO_Camera import IO_Camera
from IO_Collision import IO_CollisonHandler
from typing import Any, List
import pygame
from IO_Input import IO_InputHandler
from Character import ATTACK_TIME, IO_Character, JUMP_TIME
from Level import Level, LevelManager
from IO_Object import IO_Entity, IO_Object
from IO_Texture import FLIP_BOTH,FLIP_HORIZONTAL,FLIP_VERTICAL,FLIP_NONE
from IO_Object import IO_Object
from Level import Level

class Game(IO_Object):
    __instance = None

    def __init__(self):
        super().__init__()
        if Game.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Game.__instance = self
        
        self.level : Level
        self.player : IO_Character
        self.current : int = 0
        self.currentLevel = 0
        
    def init(self):
        IO_MusicManager.getInstance().playMusic("skool",-1)
        self.level = LevelManager.getInstance().levelMap["level"+str(self.currentLevel + 1)]
        IO_CollisonHandler.getInstance().setTileMap(self.level.wall.data,(self.level.map.tileWidth,self.level.map.tileWidth))
        self.player = self.level.characters["Dude"]

    def nextLevel(self):
        self.currentLevel = (self.currentLevel + 1) % len(LevelManager.getInstance().levelMap)

    def update(self, dt: float = 0) -> None:
        if self.won():
            self.nextLevel()
            if self.currentLevel == 0:
                LevelManager.getInstance().parse("asset/level.xml")
            self.level = LevelManager.getInstance().levelMap["level"+str(self.currentLevel+ 1)]
            IO_CollisonHandler.getInstance().setTileMap(self.level.wall.data,(self.level.map.tileWidth,self.level.map.tileWidth))
            self.player = self.level.characters["Dude"]
        
        if self.lost() or IO_InputHandler.getInstance().isPressed(pygame.K_r):
            LevelManager.getInstance().parse("asset/level.xml")
            self.level = LevelManager.getInstance().levelMap["level"+str(self.currentLevel+ 1)]
            IO_CollisonHandler.getInstance().setTileMap(self.level.wall.data,(self.level.map.tileWidth,self.level.map.tileWidth))
            self.player = self.level.characters["Dude"]
        
        if self.player.isDead:
            ChangeCommand().execute()
        self.level.update(dt,self)
        for actor  in self.level.characters.values():
            actor.update(dt,self)
            actor.isPushing = False
            actor.rigidBody.update(dt)
            actor.lastSafePosition.x = actor.transform.x
            actor.transform.translateX(actor.rigidBody.position.x)
            actor.collider.set(actor.transform.x,actor.transform.y,actor.w,actor.h)
            actor.groundedcollider.set(actor.transform.x,actor.transform.y,actor.w,actor.h)
            
            if(IO_CollisonHandler.getInstance().mapCollision(actor.collider.box) or self.actorCollide(actor) or self.barrierCollide(actor)) and actor.isFrozen == False:
                actor.transform.x = actor.lastSafePosition.x 
            elif (actor.isDead== False or actor.isFrozen )and (IO_CollisonHandler.getInstance().mapCollision(actor.groundedcollider.box) or self.actorCollide(actor) or self.barrierCollide(actor) and actor.isFrozen == True):
                actor.transform.x = actor.lastSafePosition.x 
            
            actor.rigidBody.update(dt)
            actor.lastSafePosition.y = actor.transform.y
            actor.transform.translateY(actor.rigidBody.position.y)
            actor.collider.set(actor.transform.x,actor.transform.y,actor.w,actor.h)
            actor.groundedcollider.set(actor.transform.x,actor.transform.y,actor.w,actor.h)
            
            if (IO_CollisonHandler.getInstance().mapCollision(actor.collider.box) or self.actorCollide(actor) or  self.barrierCollide(actor)) and actor.isFrozen == False:
                actor.transform.y = actor.lastSafePosition.y
            elif (actor.isDead == False or actor.isFrozen) and (IO_CollisonHandler.getInstance().mapCollision(actor.groundedcollider.box) or self.actorCollide(actor) or self.barrierCollide(actor) and actor.isFrozen == True):
                actor.transform.y = actor.lastSafePosition.y
            if(IO_CollisonHandler.getInstance().mapCollision(actor.groundedcollider.box) or self.barrierCollide(actor) or self.actorCollide(actor)):
                actor.isGrounded = True
                actor.isJumping = False
            else:
                actor.isGrounded = False
            
            if actor.isJumping and actor.jumpTime > 0:
                actor.jumpTime -= dt

            if actor.attackTime > 0 and actor.isAttacking:    
                actor.attackTime -= dt
            else:
                actor.attackTime = ATTACK_TIME
                actor.isAttacking = False
            
            actor.animationState()
            if (actor.animation != None):
                actor.animation.update(dt)
            actor.rigidBody.unSetForce()

    def actorCollide(self,actor : IO_Character):
        for char in self.level.characters.values():
            if char !=  actor:
                
                if IO_CollisonHandler.getInstance().CheckCollision(actor.collider.box,char.collider.box) :
                    if(self.player == actor):
                        if(self.player.flip == FLIP_NONE ) and  (actor.transform.y + actor.h -10 >= char.transform.y and actor.transform.y + actor.h <= char.transform.y + char.w ):
                            self.player.isPushing = True
                            char.rigidBody.applyForceX(1) 

                        if(self.player.flip == FLIP_HORIZONTAL) and (actor.transform.y + actor.h -10 >= char.transform.y and actor.transform.y + actor.h <= char.transform.y + char.w ):
                            self.player.isPushing = True
                            char.rigidBody.applyForceX(-1)
                    return True
        return False
    
    def gameOver(self):
        return (self.lost() or self.won())



    def lost(self):
        for actor in self.level.characters.values():
           if actor.isDead == False: return False
        
        return True

    def won(self):
        return self.level.goal.atGoal


    def barrierCollide(self,actor : IO_Character):
        for barrier in self.level.barriers:
            if IO_CollisonHandler.getInstance().CheckCollision(barrier.collider.box,actor.collider.box):
                return True
        return False
    
    def render(self, dt: float = 0) -> None:
        self.level.render(dt)
        cam =  IO_Camera.getInstance().position
        b =self.player.collider.box
        r = pygame.Rect(b.x - cam.x,b.y - cam.y,b.w,b.h)
        pygame.draw.polygon(pygame.display.get_surface(),(0,255,255),((r.x + 4,r.y - 10),(r.x + r.w - 4,r.y - 10),(r.x + (r.w/2),r.y -3)))

    def event(self, dt: float) -> None:
        if(self.gameOver() == False):
            for invoke in  self.invoker(dt):
                invoke.execute()

    def invoker(self,dt : float) ->Command:
        commands  = []
        
        if IO_InputHandler.getInstance().listen() != None:
            if IO_InputHandler.getInstance().listen() != pygame.KEYUP:
                if IO_InputHandler.getInstance().isPressed(pygame.K_j):
                        commands.append(ChangeCommand())
                if(self.player.isDead == False):
                    if IO_InputHandler.getInstance().isPressed(pygame.K_k):
                        commands.append( AttackCommand())

        if(self.player.isDead == False):
            if IO_InputHandler.getInstance().isPressed(pygame.K_w):
                commands.append( JumpCommand(queue=[dt]))
            if IO_InputHandler.getInstance().isPressed(pygame.K_a):
                commands.append(MoveCommand(queue=["left"]))
            if IO_InputHandler.getInstance().isPressed(pygame.K_d):
                commands.append( MoveCommand(queue=["right"]))
            
            if len(commands) == 0:
                commands.append( idleCommand())
        return commands

    @staticmethod 
    def getInstance():
        if Game.__instance == None:
            Game()
        return Game.__instance
    
class Command(IO_Entity):
    def __init__(self,queue : list[Any] = []):
        super().__init__()
        self.game = Game.getInstance()
        self.queue = queue

    def execute(self):
        raise NotImplementedError

class idleCommand(Command):
    def __init__(self,queue=[]):
        super().__init__(queue)

    def execute(self):
        self.game.player.isRunning = False
        if self.game.player.isGrounded:
            self.game.player.jumpTime = JUMP_TIME
            
        self.game.player.rigidBody.unSetForce()

class JumpCommand(Command):
    def __init__(self,queue=[]):
        super().__init__(queue)

    def execute(self):
        if self.game.player.isGrounded:
            self.game.player.isJumping = True
            self.game.player.isGrounded = False
            self.game.player.rigidBody.applyForceY(-1*self.game.player.jumpForce)
            IO_MusicManager.getInstance().playEffect("jump")
        elif self.game.player.isJumping and self.game.player.jumpTime > 0:
            #print(self.game.player.jumpTime)
            self.game.player.rigidBody.applyForceY(-1*self.game.player.jumpForce)
        else:
            self.game.player.isJumping = False
            self.game.player.jumpTime = JUMP_TIME

class MoveCommand(Command):
    def __init__(self,queue=[]):
        super().__init__(queue)

    def execute(self):
        direction = self.queue.pop(0)
        if(direction == "left"):
            self.game.player.isRunning = self.game.player.isGrounded
            self.game.player.flip = FLIP_HORIZONTAL
            self.game.player.rigidBody.applyForceX(-1 * 3)
            IO_MusicManager.getInstance().playEffect("walk")
            
        if(direction == "right"):
            self.game.player.isRunning = self.game.player.isGrounded
            self.game.player.flip = FLIP_NONE
            self.game.player.rigidBody.applyForceX(1 * 3)
            IO_MusicManager.getInstance().playEffect("walk")


class ChangeCommand(Command):
    def __init__(self,queue=[]):
        super().__init__(queue)

    def execute(self):
        keys = list(self.game.level.characters.keys())

        self.game.current = (self.game.current + 1) % len(self.game.level.characters)
        while(self.game.level.characters[keys[self.game.current]].isDead == True):
            self.game.current = (self.game.current + 1) % len(self.game.level.characters)
    
        self.game.player.rigidBody.unSetForce()
        self.game.player.isRunning = False
        self.game.player = self.game.level.characters[keys[self.game.current]]


class AttackCommand(Command):
    def __init__(self,queue=[]):
        super().__init__(queue)

    def execute(self):
        self.game.player.isAttacking =True
        self.game.player.attack()