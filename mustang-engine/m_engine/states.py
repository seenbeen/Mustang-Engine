from m_engine.engine import *

from m_engine.gamestate import *
from m_engine.gamespace import *
from m_engine.physx import *
from m_engine.scene import *
from m_engine.eng_math import Point2D

from gui.menus import MenuHandler
from gui.hud import HUD

import utils, controls, entities

class Playing(AbstractGameState):
    def __init__(self):
        AbstractGameState.__init__(self)
        self.space = GameSpace()
        self.physx = Physx(self.space)
        self.hud = HUD()

        #Notes: objects that are registered must have a
        #rigidbodycontrol and must be a gameobject or it prints a mean msg
        Engine.player = entities.TestSprite()
        Engine.pcontrol = controls.AdminControl(K_w,K_s,K_a,K_d)
        self.physx.registerObject(Engine.player)

        Engine.otherBlock = entities.TestSprite()
        Engine.otherControl = controls.CharacterControl(K_UP,K_DOWN,K_LEFT,K_RIGHT)
        self.physx.registerObject(Engine.otherBlock)

        Engine.thirdControl = controls.CharacterControl(K_y,K_h,K_g,K_j)
        Engine.thirdBlock = entities.TestSprite()
        self.physx.registerObject(Engine.thirdBlock)
        
        Engine.cam1 = Camera(0,0,400,300,self.space)
        Engine.cam2 = Camera(0,0,400,300,self.space)
        Engine.cam3 = Camera(0,0,400,300,self.space)
        Engine.cam4 = Camera(0,0,400,300,self.space)

        Engine.cam2.setWindowLocation(Point2D(400,0))
        Engine.cam3.setWindowLocation(Point2D(0,300))
        Engine.cam4.setWindowLocation(Point2D(400,300))
        
    def update(self):
        Engine.screen.fill((0,0,0))
        self.space.update()
        self.physx.updatePhysx()
        Camera.update()
        Camera.render(Engine.screen)
        self.hud.update()
        self.hud.render(Engine.screen)
        
class Menu(AbstractGameState):
    def __init__(self):
        AbstractGameState.__init__(self)
        self.menu = MenuHandler()
    def update(self):
        self.menu.update()
        self.menu.render(Engine.screen)
