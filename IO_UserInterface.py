from __future__ import annotations

from pygame.display import update
from Game import ChangeCommand, Game

from pygame.transform import average_color
from IO_XmlHandler import IO_XmlHandler
from IO_Texture import IO_Texture, IO_TextureManager
from IO_Collision import IO_CollisonHandler
from Level import LevelManager
from IO_Input import IO_InputHandler
import pygame
from IO_Object import IO_Entity, IO_Object
from IO_Actor import IO_Actor, IO_Property
from IO_Screen import IO_SCREEN_SIZE, IO_Screen


class IO_UserInterface:
    __instance = None

    def __init__(self):
        """ Virtually private constructor. """
        if IO_UserInterface.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            IO_UserInterface.__instance = self

            self.activities : dict[str,IO_Activity]= {}
            self.currnetActivity : IO_Activity= None

    def parse(self,source):
        xmlRoot = IO_XmlHandler.getRoot(source)
        xmlActivites = IO_XmlHandler.getChild(xmlRoot,"activity")
        

        for xmlActivity in xmlActivites:
            activiy = IO_Activity()
            xmlbuttons = IO_XmlHandler.getChild(xmlActivity,"button")
            levelcount =  1
            for xmlbutton in xmlbuttons:
                x = float(IO_XmlHandler.getAttribute(xmlbutton,"x"))
                y = float(IO_XmlHandler.getAttribute(xmlbutton,"y"))
                w = float(IO_XmlHandler.getAttribute(xmlbutton,"w"))
                h = float(IO_XmlHandler.getAttribute(xmlbutton,"h"))
                name = IO_XmlHandler.getAttribute(xmlbutton,"name")

                button = None
                if name == "quit": button = QuitButton(IO_Property(x=x,y=y,w=w,h=h),name,activiy)
                elif name == "instruct": button = InstructButton(IO_Property(x=x,y=y,w=w,h=h),name,activiy)
                elif name == "restart":  button = RestartButton(IO_Property(x=x,y=y,w = w,h=h),name,activiy)
                elif name == "current":  button = CurrentButton(IO_Property(x=x,y=y,w = w,h=h),name,activiy)
                else: 
                    button = LevelButton(IO_Property(x=x,y=y,w = w,h=h),name,levelcount,activiy)
                    levelcount += 1
                activiy.buttons[name] = button

            activiy.activityObjects["game"] = Game.getInstance()
            IO_UserInterface.getInstance().activities["start"] = activiy

        xmlCurrent = IO_XmlHandler.getChild(xmlRoot,"current")[0]
        name = IO_XmlHandler.getAttribute(xmlCurrent,"name")
        IO_UserInterface.getInstance().currnetActivity = IO_UserInterface.getInstance().activities[name]

    def init(self):
        self.currnetActivity.init()

    def event(self,dt):
        if self.currnetActivity != None:
            self.currnetActivity.event(dt)

    def update(self,dt):
        if self.currnetActivity != None:
            self.currnetActivity.update(dt)

    def render(self,dt):
        if self.currnetActivity != None:
            self.currnetActivity.render(dt)

    @staticmethod 
    def getInstance():
        """ Static access method. """
        if IO_UserInterface.__instance == None:
            IO_UserInterface()
        return IO_UserInterface.__instance

class IO_Activity(IO_Object):
    def __init__(self):
        self.buttons :dict[str,IO_Buttons] = {}
        self.activityObjects: dict[str,object] = {}
        
    def init(self):
        for activityObject in self.activityObjects.values():
            activityObject.init()

    def event(self, dt: float) -> None:
        for activityObject in self.activityObjects.values():
            activityObject.event(dt)

    def update(self,dt):

        for activityObject in self.activityObjects.values():
            activityObject.update(dt)

        for button in self.buttons.values():
            button.update(dt)
    
    def render(self,dt):
        
        for activityObject in self.activityObjects.values():
            activityObject.render(dt)

        for button in self.buttons.values():
            button.render(dt)

class IO_Buttons(IO_Actor):
    def __init__(self,prop,name,activity):
        super().__init__(property=prop,name=name)
        self.color = (255,255,255)
        self.hover = (0,255,255)
        self.nothover = (255,225,255)
        self.activity:IO_Activity = activity

    def onHover(self):
        if self.collider.box.collidepoint(pygame.mouse.get_pos()):
            self.color = self.hover
            return True
        else:
            self.color = self.nothover
        return False

    def onClick(self):
        raise NotImplementedError()

    def update(self,dt):
        if self.onHover():
            self.onClick()
        
    def render(self,dt):
        pygame.draw.rect(pygame.display.get_surface(),self.color,self.collider.box,2)
        destination = (self.collider.box.x,self.collider.box.y)
        if (self.texture != None):
            self.texture.draw(destination=destination,screenPos=True)

class LevelButton (IO_Buttons):
    def __init__(self,prop,name,level,activity):
        super().__init__(prop=prop,name=name,activity=activity)
        self.level = level
        self.texture = IO_TextureManager.getInstance().textureMap["level"+str(self.level)]

    def onClick(self):
        if IO_InputHandler.getInstance().mousePressed(0):
            game = self.activity.activityObjects["game"]
            LevelManager.getInstance().parse("asset/level.xml")
            game.level = LevelManager.getInstance().levelMap["level"+str(self.level)]
            IO_CollisonHandler.getInstance().setTileMap(game.level.wall.data,(game.level.map.tileWidth,game.level.map.tileWidth))
            game.player = game.level.characters["Dude"]
            game.currentLevel = self.level -1
        
class QuitButton (IO_Buttons):
    def __init__(self,prop,name,activity):
        super().__init__(prop=prop,name=name,activity=activity)
        self.texture = IO_TextureManager.getInstance().textureMap["quit"]

    def onClick(self):
        if IO_InputHandler.getInstance().mousePressed(0):
            IO_Screen.getInstance().running = False

class RestartButton (IO_Buttons):
    def __init__(self,prop,name,activity):
        super().__init__(prop=prop,name=name,activity=activity)
        self.texture = IO_TextureManager.getInstance().textureMap["restart"]

    def onClick(self):
        if IO_InputHandler.getInstance().mousePressed(0):
            game = self.activity.activityObjects["game"]
            LevelManager.getInstance().parse("asset/level.xml")
            game.level = LevelManager.getInstance().levelMap["level"+str(game.currentLevel+ 1)]
            IO_CollisonHandler.getInstance().setTileMap(game.level.wall.data,(game.level.map.tileWidth,game.level.map.tileWidth))
            game.player = game.level.characters["Dude"]

class CurrentButton(IO_Buttons):
    def __init__(self,prop,name,activity):
        super().__init__(prop=prop,name=name,activity=activity)
        self.texture = IO_TextureManager.getInstance().textureMap["curr_Dude"]
        self.leveltexture = IO_TextureManager.getInstance().textureMap["level1"]

    def update(self, dt):
        super().update(dt)
        game = self.activity.activityObjects["game"]
        self.texture = IO_TextureManager.getInstance().textureMap["curr_"+game.player.name]
        self.leveltexture = IO_TextureManager.getInstance().textureMap["level"+str(game.currentLevel+1)]
        
    def onClick(self):
        if IO_InputHandler.getInstance().mousePressed(0):
            ChangeCommand().execute()

    def render(self, dt):
        super().render(dt)
        destination = (self.collider.box.x+64,self.collider.box.y)
        if (self.leveltexture != None):
            self.leveltexture.draw(destination=destination,screenPos=True)

class InstructButton (IO_Buttons):
    def __init__(self,prop,name,activity):
        super().__init__(prop=prop,name=name,activity=activity)
        self.texture = IO_TextureManager.getInstance().textureMap["instruct"]
        self.instruct = IO_TextureManager.getInstance().textureMap["rule"]

    def update(self, dt: float) -> None:
        pass

    def onClick(self):
        pass

    def render(self, dt: float) -> None:
        super().render(dt)
        if super().onHover():
            IO_TextureManager.getInstance().textureMap["rule"].draw(destination=(84,20),screenPos=True)
