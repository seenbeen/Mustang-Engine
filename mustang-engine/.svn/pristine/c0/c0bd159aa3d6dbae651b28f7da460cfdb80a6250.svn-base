from m_engine.scene import *

class GameSpace():
    def __init__(self):
        self.objId = 0
        self.objects = {}
        self.events = []
        self.physx = None
        
    def addObject(self,obj):
        obj.bindVar("objId",self.objId)
        self.objects[self.objId] = obj
        self.objId +=1
        obj.bindSpace(self)

    def removeObject(self,obj):
        del(self.objects[obj.boundVar["objId"]])
        obj.boundVar["objId"] = -1 #not bound to engine
        obj.unbindSpace()
        
    def update(self):
        #simple update method - we'll let the gameobject
        #take care of the implementation details
        for each in self.objects.values():
            each._update()
        #resolve all messages that occured during this frame
        while self.events:
            self.events.pop().do()

    def query(self,rect):
        return self.objects.values()

    def addEvent(self,evt):
        self.events.append(evt)

    def loadScene(self,scene):
        scene.load(self)

    def bindPhysx(self,physx):
        self.physx = physx
        
class GameEvent():
    def __init__(self,function,parameters):
        self.function = function
        self.parameters = parameters

    def do(self):
        self.function(*self.parameters);
