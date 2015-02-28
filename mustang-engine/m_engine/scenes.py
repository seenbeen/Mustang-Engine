from m_engine import *
from m_engine.eng_math import Vect2D, Point2D
from m_engine.scene import *
import utils, entities

class FrontRotunda(AbstractScene):
    def load(self,space):
        space.addObject(entities.Background())
        
        ground = entities.Ground()
        space.addObject(ground)
        space.physx.registerObject(ground)

        Engine.player.bindControl(Engine.pcontrol)
        space.addObject(Engine.player)
        
        Engine.otherBlock.bindControl(Engine.otherControl)
        Engine.otherBlock.location = Point2D(150,100)
        space.addObject(Engine.otherBlock)

        Engine.thirdBlock.bindControl(Engine.thirdControl)
        Engine.thirdBlock.location = Point2D(200,100)
        space.addObject(Engine.thirdBlock)
        
        Engine.cam1.setFocus(Engine.player)
        Engine.cam2.setFocus(Engine.otherBlock)
        Engine.cam3.setFocus(Engine.thirdBlock)
        Engine.cam4.setFocus(Engine.player)
