from __future__ import annotations
from IO_Collision import IO_CollisonHandler


from IO_Physics import IO_Vector
from IO_Texture import IO_TextureManager
from IO_Actor import IO_Actor,IO_Property

class Projectile(IO_Actor):
    def __init__(self,property : IO_Property,name="Projectile",axis = -1):
        super().__init__(property,name)
        self.texture = IO_TextureManager.getInstance().textureMap["Rock2"]
        self.force= IO_Vector(x=1,y=0)
        self.rigidBody.gravity = IO_Vector()
        self.force *= axis
        
    def update(self,dt,game):
        raise NotImplementedError

    def render(self,dt):
        super().render(dt)


class Ice(IO_Actor):
    def __init__(self,property : IO_Property,name="Projectile",axis = -1):
        super().__init__(property,name)
        self.texture = IO_TextureManager.getInstance().textureMap["Rock2"]
        self.force= IO_Vector(x=3,y=0)
        self.rigidBody.gravity = IO_Vector()
        self.force *= axis
        self.axis = axis
        
    def update(self,dt,game):
        self.rigidBody.applyForceX(self.force.x)

        self.rigidBody.update(dt)
        self.transform.translateX(self.rigidBody.position.x)
        
        self.rigidBody.unSetForce()

        for actor in game.level.characters.values():
            if IO_CollisonHandler.getInstance().CheckCollision(actor.collider.box,self.collider.box):
                if (actor != game.level.dude):
                    
                
                    self.force.x = 0
                    actor.rigidBody.gravity =  IO_Vector(y=2)
                    if actor.isDead and actor.isFrozen == False:
                        actor.transform.y  = actor.transform.y -20
                    if abs(actor.transform.x - game.level.dude.transform.x) <28 and actor.isDead == False:
                        actor.rigidBody.applyForceX(10* self.axis)
                    actor.isFrozen =actor.isDead =  True
                
                    game.level.dude.projectiles.remove(self)
                elif (actor != game.level.dude and actor.isFrozen):
                    game.level.dude.projectiles.remove(self)
            
        if self.transform.x < 0 or self.transform.x > 608:
            if self in game.level.dude.projectiles:
                game.level.dude.projectiles.remove(self)  

    def render(self,dt):
        super().render(dt)


class Arrow(IO_Actor):
    def __init__(self,property : IO_Property,name="arrow",axis = -1):
        super().__init__(property,name)
        self.texture = IO_TextureManager.getInstance().textureMap["Rock2"]
        self.force= IO_Vector(x=5,y=0)
        self.rigidBody.gravity = IO_Vector()
        self.force *= axis
        self.axis = axis
        
    def update(self,dt,game):
        self.rigidBody.applyForceX(self.force.x)

        self.rigidBody.update(dt)
        self.transform.translateX(self.rigidBody.position.x)
        
        self.rigidBody.unSetForce()

        for actor in game.level.characters.values():
            
            if IO_CollisonHandler.getInstance().CheckCollision(actor.collider.box,self.collider.box):
                if (actor != game.level.pink and actor.isFrozen == False):
                    
                    actor.isDead =  True
                    actor.rigidBody.applyForceX(self.force.x)
                    actor.rigidBody.gravity = IO_Vector(y=0)
                    
                elif (actor != game.level.pink and actor.isFrozen):
                    actor.rigidBody.applyForceX(self.axis* 4)  
                    game.level.pink.projectiles.remove(self)
    
            if self.transform.x < 0 or self.transform.x > 608:
                if self in game.level.pink.projectiles:
                    game.level.pink.projectiles.remove(self)

    def render(self,dt):
        super().render(dt)

class Stone(IO_Actor):
    def __init__(self,property : IO_Property,name="Stone",axis = -1):
        super().__init__(property,name)
        self.texture = IO_TextureManager.getInstance().textureMap["Rock2"]
        self.force= IO_Vector(x=4,y=0)
        self.axis = axis
        self.rigidBody.gravity = IO_Vector()
        self.force *= axis
        self.time  = 10
        self.actor = None
        
    def update(self,dt,game):
        self.rigidBody.applyForceX(self.force.x)
        if self.actor != None and self.time > 0:
            self.actor.rigidBody.applyForceX(self.axis * 10) 
            self.actor.rigidBody.applyForceY(-self.time)
            self.actor.rigidBody.update(dt)
            self.time -= dt
        self.rigidBody.update(dt)
        self.transform.translateX(self.rigidBody.position.x)
        
        self.rigidBody.unSetForce()

        if self.time < 0:
            game.level.owlet.projectiles.remove(self)

        for actor in game.level.characters.values():
            if IO_CollisonHandler.getInstance().CheckCollision(actor.collider.box,self.collider.box):
                if (actor != game.level.owlet):
                    actor.isDead =  True
                
                    actor.rigidBody.gravity.y = 2
                    self.actor = actor
        
        if self.transform.x < 0 or self.transform.x > 608:
                if self in game.level.owlet.projectiles:
                    game.level.owlet.projectiles.remove(self)        
    

    def render(self,dt):
        super().render(dt)