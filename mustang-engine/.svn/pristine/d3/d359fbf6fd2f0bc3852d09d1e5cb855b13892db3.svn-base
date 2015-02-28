from pygame import mouse,key

class InputManager():
    mx,my = 0,0
    mb = None
    kb = None
    events = None

    #called once per frame or so to update all input conditions
    # previously called Update
    @classmethod
    def updateInputConditions(cls, events):
        '''
        Called once per frame by Engine to update all input conditions
        '''
        cls.mb = mouse.get_pressed()
        cls.mx,cls.my = mouse.get_pos()
        cls.keys = key.get_pressed()
        cls.events = events
