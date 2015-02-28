from m_engine.sprite import *

class TestTrigger(SpriteTrigger):
    def __init__(self):
        SpriteTrigger.__init__(self,0)

    def triggered(self,sprite):
        print ("TRIGGERED!",sprite.frame)
        
