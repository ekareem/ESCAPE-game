
from __future__ import annotations
from IO_Collision import IO_CollisonHandler
from IO_Actor import IO_Property,IO_Actor

class Goal(IO_Actor):
    def __init__(self,x,y):
        super().__init__(IO_Property(x=x,y=y,w=32,h=46),name=Goal)
        self.atGoal =  False
    
    def update(self,dt,game):
        for actor in game.level.characters.values():
            if(actor.isDead == False):
                if IO_CollisonHandler.getInstance().CheckCollision(actor.collider.box,self.collider.box):
                    self.isPressed = True
                    self.atGoal = True
                if self.atGoal:
                    actor.dance = True

