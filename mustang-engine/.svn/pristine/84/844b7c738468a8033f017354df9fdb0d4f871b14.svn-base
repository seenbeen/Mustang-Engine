from m_engine.gameobject import *
from m_engine.sprite import *
from m_engine.physx import *
from m_engine.eng_math import *

from spritetriggers import *
from listeners import *

class TestSprite(SpriteObject):
    def __init__(self):
        SpriteObject.__init__(self,AssetManager.getSpriteData("TestSprite"))
        self.rigidBodyControl = RigidBodyControl(48,46,0.2,True)
        self.rigidBodyControl.addListener(TestListener())
        self.rigidBodyControl.setFriction(1)
        self.rigidBodyControl.elasticity = -0.6
        self.bindControl(self.rigidBodyControl)
        
        self.setRotation(90)

        self.testTrig = TestTrigger()
        self.bindTrigger("Moving",self.testTrig)
        
    def move(self,vect2D):
        self.rigidBodyControl.velocity+=vect2D

    def render(self,screen,x,y):
        dims = self.rigidBodyControl.dimensions
        draw.rect(screen,(255,0,0),(x-dims[0]/2,y-dims[1]/2,dims[0],dims[1]),2)
        SpriteObject.render(self,screen,x,y)

#add a background :D
class Background(GameObject):
    def __init__(self):
        GameObject.__init__(self)
        self.pic = AssetManager.getAsset("background")
        #make sure the image starts off nicely relative to the player
        self.location = Point2D(-400,-300)

    def render(self,screen,x,y):
        screen.blit(self.pic,(x,y))

class Ground(GameObject):
    def __init__(self):
        GameObject.__init__(self)
        self.location = Point2D(-400,600)
        self.rigidBodyControl = RigidBodyControl(10000,20,0,True,0.6)
        self.rigidBodyControl.setFriction(1)
        self.bindControl(self.rigidBodyControl)

    def render(self,screen,x,y):
        draw.rect(screen,(0,255,255),(x-5000,y-10,10000,20))
