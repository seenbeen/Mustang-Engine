from m_engine import eng_math

class GameObject():
    def __init__(self):
        self.boundVar = {"objId":-1}
        self.location = eng_math.Point2D()
        self.controls = {}
        self.hidden = False
        self.space = None
    #variable binding, incase other engine processing
    #units want some form of tracking (mostly types of ids)
    def bindVar(self,key,value):
        self.boundVar[key] = value

    def unbindVar(self,key):
        del(self.bound[key])

    def destroy(self):
        Engine.removeObject(self)

    def bindControl(self,control):
        control.bind(self)
        self.controls[control.id] = control

    def removeControl(self,control):
        try:
            control.unbind()
            del(self.controls[control.id])
        except:
            print("Warning: Trying to delete non-existent control!")

    def getControl(self,controlType):
        for c in self.controls.values():
            if isinstance(c,controlType):
                return c
        return None

    def _update(self):
        for control in self.controls.values():
            control.UpdateControl()
        self.update()

    def update(self):
        #this should be self-implemented
        #by any inherriting classes
        return

    def _render(self,screen,x,y):
        if not self.hidden:
            self.render(screen,x,y)
        
    def render(self,screen,x,y):
        #again, this should be self-implemented
        #by children
        return

    def hide(self,value=None):
        if value == None:
            self.hidden = not self.hidden
        elif isinstance(value,bool):
            self.hidden = value
        else:
            print("Warning: can only hide with true or false")

    def bindSpace(self,space):
        self.space = space
    def unbindspace(self):
        self.space = None
