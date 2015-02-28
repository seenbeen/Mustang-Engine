from m_engine.engine import *
from m_engine.control import *
from m_engine.eng_math import *
from m_engine.gamespace import *

import math

class KeyControl(Control):
    def __init__(self,up,down,left,right):
        Control.__init__(self)
        self.UP = up
        self.DOWN = down
        self.LEFT = left
        self.RIGHT = right

    def update(self):
        for evt in InputManager.events:
            if evt.type == KEYDOWN and evt.key == self.DOWN:
                v = self.bound.rigidBodyControl.velocity
                v-=v

        if InputManager.keys[self.LEFT]:
            self.bound.setRotation(self.bound.rotation+5)
        elif InputManager.keys[self.RIGHT]:
            self.bound.setRotation(self.bound.rotation-5)
        if InputManager.keys[self.UP]:
            ang = math.radians(self.bound.rotation+90)
            v = Vect2D(math.sin(ang),math.cos(ang))/2
            self.bound.move(v)
            self.bound.changeSprite("Moving")
        else:
            self.bound.changeSprite("Standing")

class CharacterControl(KeyControl):
    def __init__(self,up,down,left,right):
        KeyControl.__init__(self,up,down,left,right)

    def update(self):
        for evt in InputManager.events:
            if evt.type == KEYDOWN:
                if evt.key == K_ESCAPE:
                    Engine.pcontrol.disable()

        KeyControl.update(self)

class AdminControl(KeyControl):
    def __init__(self,up,down,left,right):
        KeyControl.__init__(self,up,down,left,right)
        self.toggle = True

    def update(self):
        for evt in InputManager.events:
            if evt.type == KEYDOWN:
                if evt.key == K_SPACE:
                    self.bound.hide()

                if evt.key == K_TAB:
                    if self.toggle:
                        Engine.cam1.setFocus(Engine.otherBlock)
                    else:
                        Engine.cam1.setFocus(Engine.player)

                    self.toggle = not self.toggle

        if InputManager.keys[K_4]:
            Engine.cam1.zoomf=min(Engine.cam1.zoomf+0.05,2.0)
        elif InputManager.keys[K_3]:
            Engine.cam1.zoomf=max(Engine.cam1.zoomf-0.05,0.1)
        KeyControl.update(self)
