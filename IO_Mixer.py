from IO_XmlHandler import IO_XmlHandler
from IO_Object import IO_Entity
import pygame

class IO_MusicManager(IO_Entity):

    __instance = None
    @staticmethod 
    def getInstance():
        """ Static access method. """
        if IO_MusicManager.__instance == None:
            IO_MusicManager()
        return IO_MusicManager.__instance

    def playMusic(self,id,duration = 0):
        pygame.mixer.music.load(self.musicMap[id])
        pygame.mixer.music.play(duration)
        pygame.mixer.music.set_volume(0.01)

    def pause(self):
        pygame.mixer.music.pause()
 
    def unpause(self):
        pygame.mixer.music.unpause()
    
    def stop(self):
        pygame.mixer.music.stop()

    def loadMusic(self,id,source):
        self.musicMap[id] = source

    def playEffect(self,id):
        pygame.mixer.Sound.play(self.effectMap[id])

    def loadEffect(self,id,source):
        effect = pygame.mixer.Sound(source)
        effect.set_volume(0.01)
        self.effectMap[id] = effect

    def clean(self):
        self.musicMap.clear()
        self.effectMap.clear()  
    
    def parse(self,source):
        xmlRoot = IO_XmlHandler.getRoot(source)
        xmleffects = IO_XmlHandler.getChild(xmlRoot,"effect")
        for xmleffect in xmleffects:
            path = IO_XmlHandler.getAttribute(xmleffect,"source")
            id = IO_XmlHandler.getAttribute(xmleffect,"id")
            self.loadEffect(id,path)

        xmlmusics = IO_XmlHandler.getChild(xmlRoot,"music")
        for xmlmusic in xmlmusics:
            path = IO_XmlHandler.getAttribute(xmlmusic,"source")
            id = IO_XmlHandler.getAttribute(xmlmusic,"id")
            self.loadMusic(id,path)
    
    def __iter__(self):
        yield 'musicMap', self.musicMap
        yield 'effectMap', self.effectMap

    def __init__(self):
        """ Virtually private constructor. """
        if IO_MusicManager.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            IO_MusicManager.__instance = self
        super().__init__()
        self.musicMap : dict[str,str] = {}
        self.effectMap : dict[str,pygame.mixer.Sound] = {}

