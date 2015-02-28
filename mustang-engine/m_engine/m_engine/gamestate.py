class AbstractGameState():
    def __init__(self):
        self.surface = None
        self.engId = -1 #USED FOR SPECIAL IDENTIFICATION BY ENGINE
        
    def bindSurf(self,surface):
        self.surface = surface;

    def bindId(self,Id):
        self.engId = Id

    def getId(self):
        return self.engId
    
    def update(self):
        #to be implemented
        pass
    
