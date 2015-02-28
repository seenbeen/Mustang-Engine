from pygame import *
from m_engine.eng_math import *
from m_engine.scene import *
from random import *
import math

def interp(cols,time,totalTime):
    percent = time/totalTime
    val = percent*(len(cols)-1)
    p1,p2 = cols[math.floor(val)],cols[math.ceil(val)]
    denom = totalTime/(len(cols)-1)
    percent = (time%denom)/denom
    return [x1+(x2-x1)*percent for x1,x2 in zip(p1,p2)]

class ParticleMessage():
    def __init__(self,function,parameters):
        self.function = function
        self.parameters = parameters

    def do(self):
        self.function(*self.parameters);

class ParticleSpace():
    particles = {}
    generators = {}
    forces = {}
    forceId = 0
    partId = 0
    genId = 0
    messages = []
    
    @classmethod
    def update(cls):
        gens = cls.generators.values()
        for gen in gens:
            gen.Update()
        parts = cls.particles.values()
        forces = cls.forces.values()
        for part in parts:
            part.Update()
            for force in forces:
                force.affect(part)
        
        while cls.messages:
            cls.messages.pop(0).do()
            
    @classmethod
    def render(cls,screen):
        #draw.rect(buffer,(0,0,0,0),(0,0,800,600))
        parts = cls.particles.values()
        for part in parts:
            part.render(screen)
            #Camera.render(screen)
        #screen.blit(buffer,(0,0))
    @classmethod
    def remove(cls,obj):
        if isinstance(obj,Particle):
            del(cls.particles[obj.id])
        elif isinstance(obj,AbstractGenerator):
            del(cls.generators[obj.id])

    @classmethod
    def addMsg(cls,msg):
        cls.messages.append(msg)

    @classmethod
    def addParticle(cls,particle):
        particle.id = cls.partId
        cls.particles[cls.partId] = particle
        cls.partId+=1
        
    @classmethod
    def addForce(cls,force):
        force.id = cls.forceId
        cls.forces[force.id] = force
        cls.forceId+=1
        
class Particle():
    def __init__(self,x,y,lifespan):
        self.pos = Point2D(x,y)
        self.velocity = Vect2D()
        self.lifespan = lifespan
        self.olifespan = lifespan
        self.id = -1
        
    def render(self,screen):#,x,y):
        #by default: (something)
        pass

    def Update(self):
        self.lifespan-=1
        self.pos += self.velocity
        if self.lifespan == 0:
            msg = ParticleMessage(ParticleSpace.remove,[self])
            ParticleSpace.addMsg(msg)
        self.update()

    def update(self):
        #do whatever fanciful shizz needed here
        pass
    
class Beam(Particle):
    def __init__(self,x,y,lifespan,colours):
        Particle.__init__(self,x,y,lifespan)
        self.colours = colours

    def render(self,screen):#,x,y):
        percent = 1-self.lifespan/self.olifespan
        col = list(map(int,interp(self.colours,percent,1)))
        draw.aaline(screen,col,self.pos["xy"],(self.pos+self.velocity*1.5)["xy"])

class AbstractGenerator():
    def __init__(self,x,y,particleClass,interval):
        self.pos = Point2D(x,y)
        self.particleClass = particleClass
        self.interval = interval
        self.timer = 0
        self.id = -1
        
    def Update(self):
        if self.timer == 0:
            self.generate()
        self.timer = (self.timer+1)%self.interval

        self.update()
        
    def update(self):
        #to be implemented
        pass

    def generate(self):
        
        #to be overridden
        pass

class AreaGravity():
    def __init__(self,x,y,strength,radius):
        self.strength = strength
        self.radius = radius
        self.pos = Point2D(x,y)
        
    def affect(self,particle):
        dif = self.pos-particle.pos
        dist = abs(dif)
        if dist == 0 or dist > self.radius:
            return

        percent = self.radius/dist/1000
        
        if dist < self.radius:
            particle.velocity+=dif*percent*self.strength
    
