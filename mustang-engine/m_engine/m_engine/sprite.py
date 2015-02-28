from pygame import transform
from m_engine.control import *
from m_engine.asset import *
from m_engine.gameobject import *

class Sprite():
    def __init__(self,imageData):
        self.imageSet = imageData.imageSet
        self.frames = len(self.imageSet)
        self.frame = 0
        self.rotation = 0
        self.rotations = [0 for i in range(self.frames)]
        self.renderedImages = [x.copy() for x in self.imageSet]
        self.imgDims = {"x":self.renderedImage.get_width(),"y":self.renderedImage.get_height()}
        self.delay = imageData.delay
        self.counter = 0

        self.triggers = [[] for i in range(self.frames)]
        self.lastFired = -1
        
    def bindTrigger(self,trigger):
        n = trigger.frame
        self.triggers[n].append(trigger)
        
    @property
    def renderedImage(self):
        return self.renderedImages[self.frame]

    @property
    def setImage(self):
        return self.imageSet[self.frame]

    def getOffset(self):
        return [self.imgDims["x"],self.imgDims["y"]]

    def setRotation(self,rotation):
        self.rotation = rotation%360

    def updateRotation(self):
        if not self.rotations[self.frame] == self.rotation:
            self.rotations[self.frame] = self.rotation
            self.renderedImages[self.frame] = transform.rotate(self.setImage,self.rotation)
            self.imgDims["x"] = self.renderedImage.get_width()/2
            self.imgDims["y"] = self.renderedImage.get_height()/2

    def nextFrame(self):
        if self.counter == 0:
            self.frame = (self.frame+1)%self.frames
        self.counter = (self.counter+1)%self.delay

    def render(self,screen,x,y):
        self.updateRotation()
        ox,oy = self.getOffset()
        screen.blit(self.renderedImage,(x-ox,y-oy))

    def reset(self):
        self.frame = 0
        self.counter = 0
        self.rotation = 0

    def fireTriggers(self):
        if not self.lastFired == self.frame:
            self.lastFired = self.frame
            for trigger in self.triggers[self.frame]:
                trigger._triggered(self)
        
            
class SpriteObject(GameObject):
    def __init__(self,spriteData):
        GameObject.__init__(self)
        self.sprites = {}
        for k in spriteData.keys():
            self.sprites[k] = Sprite(spriteData[k])
        self.currentSprite = list(self.sprites.keys())[0]
        self.rotation = 0

    @property
    def sprite(self):
        return self.sprites[self.currentSprite]

    def changeSprite(self,spriteId):
        if spriteId not in self.sprites:
            print ("Warning: Trying to change to non existent sprite! "+str(self.boundVar["objId"]))
        if not self.currentSprite == spriteId:
            self.currentSprite = spriteId
            self.sprite.reset()
            self.sprite.setRotation(self.rotation)

    def render(self,screen,x,y):
        self.sprite.render(screen,x,y)

    def setRotation(self,ang):
        self.rotation = ang%360
        self.sprite.setRotation(ang)

    def _update(self):
        GameObject._update(self)
        self.sprite.nextFrame()
        self.sprite.fireTriggers()
        self.update()
        
    def bindTrigger(self,spritekey,trigger):
        self.sprites[spritekey].bindTrigger(trigger)
        
class SpriteTrigger():
    def __init__(self,frame):
        self.enabled = True
        self.frame = frame-1
        
    def toggleTrigger(self, Bool = None):
        if not Bool == None:
            if isinstance(Bool,bool):
                self.enabled = Bool
            else:
                print("Warning: Enable Trigger takes in a boolean argument!")
        else:
            self.enabled = not self.enabled

    def _triggered(self,sprite):
        if self.enabled:
            self.triggered(sprite)
        
    def triggered(self,sprite):
        '''
        Implement trigger effect here
        '''
        pass
