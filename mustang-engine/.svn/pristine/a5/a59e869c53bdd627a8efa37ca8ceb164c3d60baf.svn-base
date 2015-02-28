from pygame import Rect
from m_engine.scene import *
from m_engine.control import *
from m_engine.gameobject import *

from m_engine import eng_math


"""
Physics section :DDD

Physx is a class that handles calculations that are physics related
-May grow in the future
"""
class Collision():
    def __init__(self,A,B,nature):
        self.A = A
        self.B = B
        self.nature = nature

class Physx():
    def mapRect(x):
        return [x[i]-1 if i < 2 else x[i]+2 for i in range(len(x))]
    
    def rectCollideNature(rectA,rectB):
        aLeft,aTop,aRight,aBottom = rectA
        aBottom+=aTop
        aRight+=aLeft
        bLeft,bTop,bRight,bBottom = rectB
        bBottom+=bTop
        bRight+=bLeft
        possible = [[abs(aTop-bBottom),"TOP"],[abs(aBottom-bTop),"BOTTOM"],[abs(aLeft-bRight),"LEFT"],[abs(aRight-bLeft),"RIGHT"]]
        possible.sort()
        if possible[0][0] == possible[1][0]:
            return "CORNER"
        return possible[0][1]
    
    def __init__(self,space):
        self.space = space
        space.bindPhysx(self)
        self.rbcToResolve = []

    def checkCollisions(self,rigidBodyControl,static=False):
        rect = rigidBodyControl.getRect()
        if static:
            rect = Physx.mapRect(rect)
        collisions = []
        for obj in self.space.query(rect):
            c = obj.getControl(RigidBodyControl)
            if not c == None and c.getRect().colliderect(rect) and not c.id == rigidBodyControl.id:
                collisions.append(c)

        return collisions

    #objects must be registered into the physics space before getting
    #affected by it; objects must have a rigidbodycontrol to do this
    def registerObject(self,gameObject):
        if not isinstance(gameObject,GameObject):
            print ("Fatal: Trying to add "+repr(gameObject)+". Required: GameObject!")
            return
        rbc = gameObject.getControl(RigidBodyControl)
        if rbc == None:
            print ("Fatal: GameObject must have a rigidBodyControl!")
            return
        rbc.bindSpace(self)
    
    def updatePhysx(self):
        '''
        after all of the move operations are done,
        we must resolve what happened to determine order obj's,etc.
        '''

        for rbc in self.rbcToResolve:
            collisions = self.checkCollisions(rbc,True)
            friction = eng_math.Vect2D()

            x,xx,y,yy = True,True,True,True
            for c in collisions:
                if c.solid and rbc.solid:
                    nature = Physx.rectCollideNature(Physx.mapRect(rbc.getRect()),c.getRect())
                    if nature == "LEFT":
                        x = False
                        friction.components["y"]+=c.friction
                    if nature == "RIGHT":
                        xx = False
                        friction.components["y"]+=c.friction
                    if nature == "TOP":
                        y = False
                        friction.components["x"]+=c.friction
                    if nature == "BOTTOM":
                        yy = False
                        friction.components["x"]+=c.friction

            for force in rbc.forces.values():
                dx,dy = True,True
                if not x and force.vect["x"] < 0 or not xx and force.vect["x"] > 0:
                    dx = False
                    rbc.normal.components["y"]+= abs(force.vect["x"])
                elif not y and force.vect["y"] < 0 or not yy and force.vect["y"] > 0:
                    dy = False
                    rbc.normal.components["x"]+= abs(force.vect["y"])

                force.apply(dx,dy)

            rbc.normal.components["x"]*= friction["x"] #friction in the x and y axis
            rbc.normal.components["y"]*= friction["y"]

            V = rbc.velocity
            normal = rbc.normal

            if V.components["x"] < 0:
                V.components["x"] = min(V["x"]+normal["x"],0)
            elif V.components["x"] > 0:
                V.components["x"] = max(V["x"]-normal["x"],0)
            if V.components["y"] < 0:
                V.components["y"] = min(V["y"]+normal["y"],0)
            if V.components["y"] > 0:
                V.components["y"] = max(V["y"]-normal["y"],0)

        priority = eng_math.PriorityQueue()
        
        while self.rbcToResolve:
            priority.push(self.rbcToResolve.pop())

        order = []
        while priority.hasNext():
            order.append(priority.pop())

        speedThreshold = abs(order[0].velocity)

        for i in range(int(speedThreshold)):
            for j in range(len(order)-1,-1,-1):
                old = order[j].bound.location.copy()
                V = order[j].velocity
                delta = V/speedThreshold
                order[j].bound.location+=delta
                collisions = self.checkCollisions(order[j])
                for c in collisions:
                    nature = Physx.rectCollideNature(order[j].getRect(),c.getRect())
                    order[j].alertCollision(Collision(order[j],c,nature))
                    if c.solid and order[j].solid:
                        if nature == "LEFT" or nature == "RIGHT":
                            order[j].bound.location.components["x"] = old["x"]
                            V.components["x"] *= c.elasticity
                            if abs(V.components["x"]) < 1:
                                V.components["x"] = 0
                        elif nature == "TOP" or nature == "BOTTOM":
                            order[j].bound.location.components["y"] = old["y"]
                            V.components["y"] *= c.elasticity
                            if abs(V.components["y"]) < 1:
                                V.components["y"] = 0
                        else:
                            order[j].bound.location.components["x"] = old["x"]-delta["x"]
                            order[j].bound.location.components["y"] = old["y"]-delta["y"]
        #clear normals
        for x in order:
            x.normal-=x.normal

class Force():
    """
    I do call this forces, but its a bit of a misnomer.
    It's more like something that causes acceleration per loop.
    Ex: gravity
    """
    ids = 0
    def __init__(self,vect2D):
        self.id = Force.ids
        Force.ids+=1
        self.vect = vect2D
        self.bound = None

    def bind(self,rigidBodyControl):
        self.bound = rigidBodyControl

    def unbind(self):
        self.bound = None

    def apply(self,x,y):
        vect = self.vect.copy()
        if not x:
            vect.components["x"] = 0
        if not y:
            vect.components["y"] = 0
        self.bound.velocity+=vect

class RigidBodyControl(Control):

    def __init__(self,width,height,gravity=0,solid=True,elasticity=0):
        #if solid is false, this object will pass through other objects
        #however, listeners will still function
        #Elasticity is a measure of the percent of rebound that occurs
        Control.__init__(self)
        self.velocity = eng_math.Vect2D()
        self.normal = eng_math.Vect2D()
        self.forces = {}
        self.listeners = {}
        self.dimensions = [width,height]
        self.solid = solid
        self.elasticity = -elasticity
        self.friction = 0
        self.mass = width*height/100/2000
        if gravity > 0:
            self.addForce(Gravity(gravity))
        #this is the resultant velocity that will be parsed
        #by physx to determine wtf happened to the objects
        self.space = None

    #should be called when added into the game
    def bindSpace(self,space):
        self.space = space
        
    def __repr__(self):
        return "RigidBodyControl id:"+str(self.id);
    def __str__(self):
        return "RigidBodyControl id:"+str(self.id);
    def setFriction(self,value):
        self.friction = value

    #comparator operators
    def __eq__(self,rbc):
        if isinstance(rbc,RigidBodyControl):
            return abs(self.velocity)==abs(rbc.velocity)
    def __lt__(self,rbc):
        if isinstance(rbc,RigidBodyControl):
            return abs(self.velocity)>abs(rbc.velocity)
    def __gt__(self,rbc):
        if isinstance(rbc,RigidBodyControl):
            return abs(self.velocity)<abs(rbc.velocity)

    def addListener(self,listener):
        if not listener.bound == None:
            print ("Fatal: Listener has already been bound to another rigidbody!")
            return
        self.listeners[listener.id] = listener
        listener.bind(self)

    def removeListener(self,listener):
        if listener.bound == None:
            print ("Fatal: Trying to remove listener that doesn't belong to rigidbody!")
            return
        listener.unbind()
        del(self.listeners[listener.id])

    def addForce(self,force):
        if not force.bound == None:
            print ("Fatal: Force has already been bound to another rigidbody!")
            return
        self.forces[force.id] = force
        force.bind(self)

    def removeForce(self,force):
        if force.bound == None:
            print ("Fatal: Trying to remove force that doesn't belong to rigidbody!")
            return
        force.unbind()
        del(self.forces[force.id])

    def update(self):
        if self.space == None:
            print ("Warning: Rigid body has no physix space!")
            return
        self.space.rbcToResolve.append(self)

    def alertCollision(self,gameObject):
        for listener in self.listeners.values():
            listener.updateListener(gameObject)

    def getRect(self):
        return Rect(self.bound.location["x"]-self.dimensions[0]/2,
                    self.bound.location["y"]-self.dimensions[1]/2,
                    self.dimensions[0],self.dimensions[1])
    
"""
Standardized gravity force
"""
class Gravity(Force):
    def __init__(self,strength):
        Force.__init__(self,eng_math.Vect2D(0,strength))

class CollisionListener():
    ids = 0
    def __init__(self):
        self.id = CollisionListener.ids
        CollisionListener.ids+=1
        self.bound = None

    def bind(self,rigidBodyControl):
        self.bound = rigidBodyControl

    def unbind(self):
        self.bound = None

    def updateListener(self,collision):
        if self.bound == None:
            print ("Fatal: Listener has no bound object!")
            return
        self.onCollision(collision)

    def onCollision(self,collision):
        #listener effect implemented here!
        pass


