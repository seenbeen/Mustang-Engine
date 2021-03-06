from pygame import *
from m_engine.asset import *
from m_engine import eng_math
from m_engine.inputmanager import *

class engine(type):
    ''' metatype engine, allows for a static __getattr__ '''

    states = {"QUIT":{}}
    stateIds = {}
    private = ["var","states","stateIds"]

    var = {"screen":None,"state":None}

    def __setattr__(cls,key,value):
        if key not in engine.private:
            engine.var[key] = value
        else:
            raise AttributeError("You don't have permission to modify this variable")

    def __getattr__(cls,key):
        if key not in engine.private:
            if key in engine.var:
                return engine.var[key]
            else:
                raise AttributeError(key+" doesn't exist")
        else:
            raise AttributeError("You don't have permission to this variable")

    def init(cls,displayFlags = []):
        cls.screen = display.set_mode((800,600),*displayFlags)
        display.set_caption("Powered by Mustang Engine v0.9")

    def setTitle(cls,title):
        display.set_caption(title+" Powered by Mustang Engine v0.9")

    def addState(cls,state,key):
        if key in cls.states:
            Id = cls.stateIds[key]
            cls.states[key][Id] = state
            state.bindId(Id)
            cls.stateIds[key]+=1
        else:
            cls.states[key] = {}
            cls.stateIds[key] = 1
            cls.states[key][0] = state
            state.bindId(0)

    def removeState(cls,state):
        if key in cls.states and state.engId in cls.states[key]:
            del (cls.states[key][state.engId])

    def run(cls):
        if cls.screen == None:
            print ("FATAL: Engine not initialized!")
            return
        #use a default state as first one added
        #if state hasn't been manually set
        if cls.state == None:
            cls.state = cls.states.keys()[0]

        running = True

        cls.clock = time.Clock()

        init()

        while running:
            events = event.get()
            for evt in events:
                if evt.type == QUIT:
                    running = False

            InputManager.updateInputConditions(events)
            states = cls.states[cls.state].values()
            for state in states:
                state.update()

            if cls.state == "QUIT":
                #Note: any state registered under quit will be run
                #similar to a clean up destructor script (once and program ends)
                running = False
                break

            display.flip()
            cls.clock.tick(60)
        quit()

    def getFPS(cls):
        ''' Gets the actual framerate of own clock '''
        return cls.clock.get_fps()

class Engine(metaclass=engine): pass
