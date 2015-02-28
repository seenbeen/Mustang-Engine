from m_engine import *
from pygame import *
from random import *
import math
import eng_math

"""
Physx is a class that handles calculations that are physics related
-May grow in the future
"""
class Physx():
    rbcToResolve = eng_math.PriorityQueue()
    
    def moveRigidBody(rigidBodyControl):
        v = rigidBodyControl.updateVelocity
        Physx.rbcToResolve.push(rigidBodyControl)
##        pos = rigidBodyControl.bound.location
##        vect = rigidBodyControl.updateVelocity
##        pos+=vect
##        
##        #when we're done, reset it.
##        vect-=vect
##        #supposed to compute collisions/determines what moves where
        
    def updatePhysx():
        #after all of the move operations are done,
        #we must resolve what happened to determine order obj's,etc.
        order = []
        while Physx.rbcToResolve.hasNext():
            order.append(rbcToResolve.pop())

        speedThreshold = abs(order[0].velocity)

        for i in range(int(speedThreshold)):
            for j in range(len(order)-1,-1,-1):
                rbc = order[j]
                rbc.velocity+=rbc.velocity/speedThreshold
                rect = Rect(rbc.bound.location["x"]-400,
                            rbc.bound.location["y"]-300,
                            800,600)
                for obj in SceneManager.query(rect):
                    c = obj.getControl(RigidBodyControl)
                    if not c == None and not c.id == rbc.id:
                        if c.getRect().colliderect(rbc.getRect()):
                            c.alertCollision(obj)
                            del(order[j])
            
                
        
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
        
    def update(self):
        if self.bound == None:
            print ("Fatal: Force not bound to RigidBodyControl!")
            return
        self.bound.velocity+=self.vect
        
class RigidBodyControl(Control):
    
    def __init__(self,width,height,solid = True):
        #if solid is false, this object will pass through other objects
        #however, listeners will still function
        Control.__init__(self)
        self.velocity = eng_math.Vect2D()
        self.forces = {}
        self.listeners = {}
        self.dimensions = [width,height]
        self.solid = solid
        
        #this is the resultant velocity that will be parsed
        #by physx to determine wtf happened to the objects
        self.updateVelocity = eng_math.Vect2D()

    #comparator operators
    def __eq__(self,rbc):
        return abs(self.velocity)==abs(rbc.velocity)
    def __lt__(self,rbc):
        return abs(self.velocity)>abs(rbc.velocity)
    def __gt__(self,rbc):
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

    def addTempForce(self,vect2D):
        self.updateVelocity+=vect2D
        
    def update(self):
        for f in self.forces.values():
            f.update()

        self.updateVelocity+=self.velocity
        msg = GameMessage(Physx.moveRigidBody,[self])
        Engine.addEvent(msg)
        
    def alertCollision(self,gameObject):
        for listener in self.listeners.values():
            listener.updateListener(gameObject)

    def getRect(self):
        return Rect(self.bound.location["x"]-self.dimensions[0]/2,
                    self.bound.location["y"]-self.dimensions[1]/2,
                    self.dimensions[0],self.dimensions[1])
    
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
        update(collision)
        
    def onCollision(self,collision):
        #listener effect implemented here!
        pass
