class Control():
    ids = 0

    def __init__(self):
        self.bound = None
        self.id = Control.ids
        Control.ids+=1
        self.disabled = False
        
    def bind(self,obj):
        self.bound = obj

    def unbind(self):
        self.bound = None

    def update(self):
        #this should be overridden
        #to do whatever we want this input to do
        return

    def UpdateControl(self):
        if self.bound == None:
            print ("Warning: control has no bound object!")
            return
        if self.disabled:
            return
        self.update();
        
    def disable(self,disabled = None):
        if disabled == None:
            self.disabled = not self.disabled
        elif isinstance(disabled,bool):
            self.disabled = disabled
        else:
            print ("Warning: method Control.disabled takes in boolean")
