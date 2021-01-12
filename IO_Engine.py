
from __future__ import annotations
from IO_UserInterface import IO_Activity, IO_UserInterface, LevelButton, QuitButton, RestartButton
from IO_Mixer import IO_MusicManager
from Game import Game
from Level import Level, LevelManager
from pygame.display import update
from IO_Physics import IO_Transform
from IO_Collision import IO_CollisonHandler
from IO_Actor import IO_ActorManager, IO_Property
from Character import IO_Character
from IO_Object import IO_Object
from IO_Screen import IO_Screen
from IO_Screen import IO_SCREEN_SIZE,IO_SCREEN_COLOR,IO_SCREEN_TITLE
from IO_Input import IO_InputHandler
from IO_Texture import IO_TextureManager
from IO_Map import IO_MapManager
from IO_Animation import IO_SpriteAnimation,IO_AnimationHandler
from IO_Camera import IO_Camera
import pygame

class IO_Engine(IO_Object):
    """
    """
    __instance = None

    def __init__(self) -> None :
        super().__init__()
        """
        initilizing IO_Engine\n
        @member[0] screen pygame.Surface
        """
        if IO_Engine.__instance != None:
            raise Exception('This class is a Singloton!')
        else:
            IO_Engine.__instance = self

        self.screen : IO_Screen = None
        self.inputHandler : IO_InputHandler = None
        self.textureManager : IO_TextureManager = None
        self.mapManager : IO_MapManager = None
        self.animationHandler : IO_AnimationHandler = None
        self.player  = None
        self.camera : IO_Camera = None
        self.collisionHandler : IO_CollisonHandler = None
        self.actorManager : IO_ActorManager = None
        self.game : Game = None
        self.levelManager : LevelManager = None
        self.mixer : IO_MusicManager = None
        self.ui : IO_UserInterface = None

    def init(self,
        screenSize : tuple[int,int] = IO_SCREEN_SIZE,
        screenColor : tuple[int,int,int,int] = IO_SCREEN_COLOR,
        screenTitle : str = IO_SCREEN_TITLE) -> None :
        """
        @purpose initlize IO_Screen member variable\n
        @param[0] self IO_Screen\n
        @param[1] self screenSize\n
        @param[2] self screenColor\n
        @param[3] self screenTitle\n
        """
        pygame.init()
        self.screen = IO_Screen.getInstance()
        self.inputHandler = IO_InputHandler.getInstance()
        self.textureManager = IO_TextureManager.getInstance()
        self.animationHandler = IO_AnimationHandler.getInstance()
        self.mapManager = IO_MapManager.getInstance()
        self.collisionHandler = IO_CollisonHandler.getInstance()
        self.camera = IO_Camera.getInstance()
        self.actorManager = IO_ActorManager.getInstance()
        self.mixer = IO_MusicManager.getInstance()
        self.game = Game.getInstance()
        self.levelManager = LevelManager.getInstance()
        self.ui = IO_UserInterface.getInstance()

        self.textureManager.parse("asset/texture.xml")
        self.animationHandler.parse("asset/animation.xml")
        self.mapManager.parse("asset/map.xml")
        self.levelManager.parse("asset/level.xml")
        self.mixer.parse("asset/sound.xml")
        self.ui.parse("asset/ui.xml")


        self.screen.init(screenSize,screenColor,screenTitle)
        self.camera.init(IO_SCREEN_SIZE)
        self.mapManager.origin.x = 259
        self.mapManager.origin.y = 165
        
        self.ui.init()

        self.camera.target =self.mapManager

    def update(self, dt: float = 0.0) -> None:
        """
        @purpose : updates entitiy attributes\n
        @param[0] : self IO_Object\n
        @param[1] : dt delta time\n
        """
        self.ui.update(dt)
        self.camera.update(dt)
        pass

    def event(self, dt: float = 0.0) -> None:
        """
        @purpose : handles event\n
        @param[0] : self IO_Object\n
        @param[1] : dt delta time\n
        """
        self.ui.event(dt)
        self.inputHandler.listen()

    def render(self, dt: float = 0.0) -> None:
        """
        @purpose : renders entity\n
        @param[0] : self IO_Object\n
        @param[1] : dt delta timen\n
        """
        
        self.screen.render(dt)
        
        self.ui.render(dt)
        
        pygame.display.update()

    def clean(self) -> None:
        """
        @purpose : clean entity\n
        @param[0] : self IO_Object\n
        @param[1] : dt delta time\n
        """
        pass

    def quit(self) -> None:
        """
        quits instance of pygame
        """
        self.screen.running = False

    @staticmethod
    def getInstance()->IO_Engine | None :
        if IO_Engine.__instance == None:
            IO_Engine()

        return IO_Engine.__instance