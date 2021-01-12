from __future__ import annotations
from IO_XmlHandler import IO_XmlHandler
from IO_Animation import IO_AnimationHandler
from IO_Collision import IO_CollisonHandler
from IO_Physics import IO_Vector
from IO_Map import IO_Layer, IO_Map, IO_MapManager
from Character import Dude, IO_Character, Owlet, Pink
from IO_Actor import IO_Actor, IO_Property
from IO_Object import IO_Entity
from Obstacle import Barrier, Button,Spike
from Goal import Goal
from IO_Actor import IO_ActorManager

class Level(IO_Entity):
    def __init__(self):
        self.name : str
        self.dude : IO_Character
        self.pink : IO_Character
        self.owlet : IO_Character
        self.characters : dict[str,IO_Character] = {}
        self.map : IO_Map
        self.wall : IO_Layer
        self.barriers : list[Barrier] = []
        self.spikes : list[Spike] = []
        self.goal : Goal
        self.player : IO_Actor

    def init(self):
        pass

    def update(self,dt,game):
        
        for barrier in self.barriers:
            barrier.update(dt,game)

        for spike in self.spikes:
            spike.update(dt,game)

        self.goal.update(dt,game)

        # for character in self.characters.values():
        #       character.update(dt)

    def render(self,dt):
        self.map.render()

        for barrier in self.barriers:
            barrier.render(dt)

        for spike in self.spikes:
            spike.render(dt)

        self.goal.render(dt)

        for character in self.characters.values():
              character.render(dt)

class LevelManager:
    __instance = None

    def __init__(self):
        if LevelManager.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            LevelManager.__instance = self
        self.levelMap :dict[str,Level] = {}

    def parse(self,source):
        xmlRoot =  IO_XmlHandler.getRoot(source)

        xmllevels = IO_XmlHandler.getChild(xmlRoot,"level")
        for xmllevel in xmllevels:
            level = Level() 

            name = IO_XmlHandler.getAttribute(xmllevel,"name")
            map = IO_XmlHandler.getAttribute(xmllevel,"map")
            self.levelMap[name] = level
             
            level.name = name
            level.map = IO_MapManager.getInstance().maps[map]
            level.wall = IO_MapManager.getInstance().maps[map].layers["wall"]
            xmlcharacters = IO_XmlHandler.getChild(xmllevel,"character")[0]
            
            for xmlcharacter in xmlcharacters:
                #print(xmlcharacter.tag)
                #xmlActor = IO_XmlHandler.getChild(xmlcharacter,xmlcharacter.tag)[0]
                x = float(IO_XmlHandler.getAttribute(xmlcharacter,"x"))
                y = float(IO_XmlHandler.getAttribute(xmlcharacter,"y"))
                w = float(IO_XmlHandler.getAttribute(xmlcharacter,"w"))
                h = float(IO_XmlHandler.getAttribute(xmlcharacter,"h"))

                actor = None

                if xmlcharacter.tag == "Dude":
                    actor = level.dude = Dude(IO_Property(animation=IO_AnimationHandler.getInstance().animationMap[xmlcharacter.tag+"_Monster_Idle_4"], x=x,y=y,w=w,h=h))
                if xmlcharacter.tag == "Owlet":
                    actor = level.owlet = Owlet(IO_Property(animation=IO_AnimationHandler.getInstance().animationMap[xmlcharacter.tag +"_Monster_Idle_4"], x=x,y=y,w=w,h=h))
                if xmlcharacter.tag == "Pink":
                    actor = level.pink = Pink(IO_Property(animation=IO_AnimationHandler.getInstance().animationMap[xmlcharacter.tag +"_Monster_Idle_4"], x=x,y=y,w=w,h=h))
                    
                level.characters[xmlcharacter.tag] = actor 
            
            xmlBarriers = IO_XmlHandler.getChild(xmllevel,"barrier")
            num =0
            for xmlBarrier in xmlBarriers:
                x = float(IO_XmlHandler.getAttribute(xmlBarrier,"x"))
                y = float(IO_XmlHandler.getAttribute(xmlBarrier,"y"))
                w = float(IO_XmlHandler.getAttribute(xmlBarrier,"w"))
                h = float(IO_XmlHandler.getAttribute(xmlBarrier,"h"))
                forceX = float(IO_XmlHandler.getAttribute(xmlBarrier,"forceX"))
                forceY = float(IO_XmlHandler.getAttribute(xmlBarrier,"forceY"))
                barrier = Barrier(x=x,y=y,w=w,h=h,num=num,force=IO_Vector(x=forceX,y=forceY))
                num += 1

                xmlbuttons = IO_XmlHandler.getChild(xmlBarrier,"button")
                numb =0
                for xmlbutton in xmlbuttons:
                    x = float(IO_XmlHandler.getAttribute(xmlbutton,"x"))
                    y = float(IO_XmlHandler.getAttribute(xmlbutton,"y"))
                    buttons = Button(x=x,y=y,name=str(numb))
                    barrier.buttons.append(buttons)
                    numb += 1
                level.barriers.append(barrier)

            xmlSpikes = IO_XmlHandler.getChild(xmllevel,"spike")
            num = 0
            for xmlSpike in xmlSpikes:
                x = float(IO_XmlHandler.getAttribute(xmlSpike,"x"))
                y = float(IO_XmlHandler.getAttribute(xmlSpike,"y"))
                w = float(IO_XmlHandler.getAttribute(xmlSpike,"w"))
                h = float(IO_XmlHandler.getAttribute(xmlSpike,"h"))
                spike = Spike(x=x,y=y,w= w, h = h,num=str(num))
                level.spikes.append(spike)
                num += 1

            xmlGoal = IO_XmlHandler.getChild(xmllevel,"goal")[0]
            x = float(IO_XmlHandler.getAttribute(xmlGoal,"x"))
            y = float(IO_XmlHandler.getAttribute(xmlGoal,"y"))
            level.goal = Goal(x=x,y=y)
            
    @staticmethod
    def getInstance():
        if LevelManager.__instance == None:
            LevelManager()
        return LevelManager.__instance

        