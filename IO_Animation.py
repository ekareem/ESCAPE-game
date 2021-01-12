from __future__ import annotations

from pygame.sprite import Sprite
from pygame.transform import scale
from IO_XmlHandler import IO_XmlHandler
from IO_Texture import IO_Texture, IO_TextureManager
from IO_Object import IO_Entity, IO_Object
import pygame

class IO_Animation(IO_Object):
    def __init__(self,
                id : str,
                frameCount : int,
                repeat : bool = True,
                isEnded : bool = False,
                pause : bool = False,
                speed=100,
                scale = None,
                roatation = None,
                flip = None):
        """
        @member repeat conttollers wheter animation repeats after cycle\n
        @member isEnded checks if animation is ended\n
        @member pause pauses animation\n
        @member frame current frame\n
        """
        super().__init__()
        self.id = id
        self.repeat = repeat
        self.isEnded = isEnded
        self.pause = pause
        self.currentFrame = 0
        self.speed = speed
        self.frameCount = frameCount
        self.scale = scale
        self.roatation = roatation
        self.flip = flip
    
    def update(self,dt : float =0,scrollRatio : float = 0):
        raise NotImplementedError()

    def render(self,x,y):
        raise NotImplementedError()

    def setAttrib(self,
                frameCount : int = None,
                repeat : bool = None,
                isEnded : bool  = None,
                pause : bool = None,
                currentFrame : int  = None,
                speed= None,
                scale = None,
                rotation = None,
                flip = None):

        if (repeat != None): self.repeat = repeat
        if (isEnded != None): self.isEnded = isEnded
        if (pause != None): self.pause = pause
        if (currentFrame != None): self.currentFrame = currentFrame
        if (speed != None): self.speed = speed
        if (frameCount != None): self.frameCount = frameCount
        if (scale != None): self.scale = scale
        if (rotation != None): self.roatation = rotation
        if (flip != None): self.flip = flip

    def __iter__(self):
        yield 'class', self.__class__
        yield 'repeat', self.repeat
        yield 'pause', self.pause
        yield 'isEnded', self.isEnded
        yield 'currentFrame', self.currentFrame
        yield 'speed',self.speed
        yield 'frameCount' , self.frameCount

class IO_SpriteAnimation(IO_Animation):
    def __init__(self,
                texture :IO_Texture,
                id : str,
                frameArea : tuple[int,int],
                row : int,
                frameCount : int,
                repeat : bool = True,
                isEnded : bool = False,
                pause : bool = False,
                speed=100,
                scale = None,
                rotation = None,
                flip = None):
        """

        """
        super().__init__(id,frameCount,repeat,isEnded,pause,speed,scale,rotation,flip)
        
        self.row = row
        self.frameArea = frameArea
        self.texture : IO_Texture = texture
        self.texture.transform(scale,rotation,flip)

    def update(self, dt : float = 0):
        """
        update current frame
        """
        #ondDlength = self.frameCount * self.rowCount
        ondDlength = self.frameCount
        
        if (self.repeat or self.isEnded == False) and self.pause == False:
            self.isEnded = False
            self.currentFrame = int((pygame.time.get_ticks()/self.speed)% ondDlength)

        if self.repeat == False and self.currentFrame == ondDlength -1:
            self.isEnded = True
            self.currentFrame = ondDlength -1

    def setAttrib(self,
                frameCount : int = None,
                repeat : bool = None,
                isEnded : bool  = None,
                pause : bool = None,
                currentFrame : int  = None,
                speed= 100,
                scale = None,
                rotation = None,
                flip = None):
        
        super().setAttrib(frameCount=frameCount,repeat=repeat,isEnded=isEnded,pause=pause,currentFrame=currentFrame,speed=speed,scale =scale,rotation=rotation,flip=flip)
        self.texture.transform(scale,rotation,flip)

    def render(self,x,y,scrollRatio =1):

        destination=(x,y)
        frame = int(self.currentFrame % self.frameCount)
        frameArea = (self.frameArea[0] * self.scale[0],self.frameArea[1] * self.scale[1])
        self.texture.drawFrame(source=frameArea,destination=destination,frame=frame,row=self.row,scrollRatio=scrollRatio)


class IO_SequenceAnimation(IO_Animation):
    def __init__(self,
                textures :list[IO_Texture] | list[None],
                id : str,
                frameCount : int,
                repeat : bool = True,
                isEnded : bool = False,
                pause : bool = False,
                speed=100,
                scale = None,
                rotation = None,
                flip = None):
        """

        """
        super().__init__(id,frameCount,repeat,isEnded,pause,speed,scale,rotation,flip)
        self.textures : list[IO_Texture] | list[None] = textures
        for texture in self.textures:
            texture.transform(scale,rotation,flip)
        
    def setAttrib(self,
                frameCount : int = None,
                repeat : bool = None,
                isEnded : bool  = None,
                pause : bool = None,
                currentFrame : int  = None,
                speed= 100,
                scale = None,
                rotation = None,
                flip = None):

        super().setAttrib(frameCount=frameCount,repeat=repeat,isEnded=isEnded,pause=pause,currentFrame=currentFrame,speed=speed,scaleX=scaleX,scaleY=scaleY)
        for texture in self.textures:
            texture.transform(scale,rotation,flip)

    def update(self,dt=0):
        if (self.repeat or self.isEnded == False) and self.pause == False:
            self.isEnded = False
            self.currentFrame = int((pygame.time.get_ticks() /self.speed) % self.frameCount)

        if self.repeat == False and self.currentFrame == (self.frameCount-1):
            self.isEnded = True
            self.currentFrame = (self.frameCount-1)

    def render(self,x,y,scrollRatio =1):
        destination = (x,y)
        self.textures[self.currentFrame].draw(destination=destination,scrollRatio=scrollRatio)


class IO_AnimationHandler(IO_Object):

    __instance = None
    def __init__(self):
        if IO_AnimationHandler.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            IO_AnimationHandler.__instance = self

        self.animationMap = {}

    def parse(self,source):
        xmlRoot = IO_XmlHandler.getRoot(source)
        xmlspriteanimations = IO_XmlHandler.getChild(xmlRoot,"spriteanimations")
        xmlspriteanimation = xmlspriteanimations[0]
        xmlspriteanimations = IO_XmlHandler.getChild(xmlspriteanimation,"spriteanimation")
        
        for xmlspriteanimation in xmlspriteanimations:
            id = IO_XmlHandler.getAttribute(xmlspriteanimation,"id")
            texture = IO_XmlHandler.getAttribute(xmlspriteanimation,"texture")
            frameW = float(IO_XmlHandler.getAttribute(xmlspriteanimation,"frameW"))
            frameH = float(IO_XmlHandler.getAttribute(xmlspriteanimation,"frameH"))
            row = int(IO_XmlHandler.getAttribute(xmlspriteanimation,"row"))
            frameCount = int(IO_XmlHandler.getAttribute(xmlspriteanimation,"frameCount"))
            repeat = IO_XmlHandler.getAttribute(xmlspriteanimation,"repeat") == "True"
            speed = float(IO_XmlHandler.getAttribute(xmlspriteanimation,"speed"))
            scaleX = float(IO_XmlHandler.getAttribute(xmlspriteanimation,"scaleX"))
            scaleY = float(IO_XmlHandler.getAttribute(xmlspriteanimation,"scaleY"))
            angle = float(IO_XmlHandler.getAttribute(xmlspriteanimation,"angle"))
            flipX = IO_XmlHandler.getAttribute(xmlspriteanimation,"flipX") == "True"
            flipY = IO_XmlHandler.getAttribute(xmlspriteanimation,"flipY") == "True"

            texture =IO_TextureManager.getInstance().textureMap[texture]
            self.animationMap[id] = IO_SpriteAnimation(texture,id,(frameW,frameH),row,frameCount,repeat,speed=speed,scale= (scaleX,scaleY),rotation=angle,flip=(flipX,flipY))
        
        xmlsequenceanimations = IO_XmlHandler.getChild(xmlRoot,"sequenceanimations")
        xmlsequenceanimation = xmlsequenceanimations[0]
        xmlsequenceanimations = IO_XmlHandler.getChild(xmlsequenceanimation,"sequenceanimation")
        
        for xmlsequenceanimation in xmlsequenceanimations:
            id = IO_XmlHandler.getAttribute(xmlsequenceanimation,"id")
            repeat = IO_XmlHandler.getAttribute(xmlsequenceanimation,"repeat") == "True"
            speed = float(IO_XmlHandler.getAttribute(xmlsequenceanimation,"speed"))
            scaleX = float(IO_XmlHandler.getAttribute(xmlsequenceanimation,"scaleX"))
            scaleY = float(IO_XmlHandler.getAttribute(xmlsequenceanimation,"scaleY"))
            angle = float(IO_XmlHandler.getAttribute(xmlsequenceanimation,"angle"))
            flipX = IO_XmlHandler.getAttribute(xmlsequenceanimation,"flipX") == True
            flipY = IO_XmlHandler.getAttribute(xmlsequenceanimation,"flipY") == True

            xmltextures =IO_XmlHandler.getChild(xmlsequenceanimation,"texture")
            frameCount = len(xmltextures)
            textures = []
            for xmltexture in xmltextures:
                textureid = IO_XmlHandler.getAttribute(xmltexture,"id")

    @staticmethod 
    def getInstance():
        if IO_AnimationHandler.__instance == None:
            IO_AnimationHandler()
        return IO_AnimationHandler.__instance