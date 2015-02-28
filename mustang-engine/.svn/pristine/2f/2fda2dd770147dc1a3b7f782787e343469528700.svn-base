'''
Scene module manages all scenes and cameras/render related/culling
'''

from pygame import Surface,Rect,transform,draw
from m_engine import eng_math

class AbstractScene():
    def __init__(self):
        self.vars = None
        
    def _load(self):
        self.vars = space.objects
        space.objects = {}
        self.load()
        
    def load(self):
        #do some loading code here
        pass

class Camera():
    allCameras = {}
    ids = 0
    def render(screen):
        if len(Camera.allCameras.values()) == 0:
            print("Warning: No cameras to render!")
            return
        for cam in Camera.allCameras.values():
            cam.renderCamera(screen)

    def update():
        for cam in Camera.allCameras.values():
            cam.updateCamera()

    def __init__(self,x,y,width,height,space):
        self.id = Camera.ids
        Camera.ids += 1
        Camera.allCameras[self.id] = self

        self.location = eng_math.Point2D(x,y)
        self.width = width
        self.height = height
        self.focus = None
        self.zoom = 1.0
        self.zoomf = 1.0
        self.buffer = Surface((int(self.width*self.zoom),int(self.height*self.zoom)))

        self.windowLocation = eng_math.Point2D()
        self.space = space
        
    def renderCamera(self,screen):
        toRender = self.space.query(self.getRect())

        self.buffer.fill((0,0,0))
        for each in toRender:
            nx,ny = self.xFormCoords(each.location)
            each._render(self.buffer,nx,ny)

        buffer = transform.scale(self.buffer,(self.width,self.height))

        screen.blit(buffer,(self.windowLocation["x"],
                            self.windowLocation["y"]))
        draw.rect(screen,(0,0,255),(self.windowLocation["x"],self.windowLocation["y"],self.width,self.height),2)

    #used for culling purposes
    def getRect(self):
        return Rect(self.location["x"]-self.width/2,
                    self.location["y"]-self.height/2,
                    self.width,self.height)

    def xFormCoords(self,point2D):
        x,y = point2D["x"],point2D["y"]
        return [x-self.location["x"]+self.width*self.zoom/2,
                y-self.location["y"]+self.height*self.zoom/2]

    def setFocus(self,obj):
        if obj.boundVar["objId"] == -1:
            print ("Warning: this object is not in the game!")
        self.focus = obj

    def setWindowLocation(self,point2D):
        self.windowLocation = point2D

    def updateCamera(self):
        if self.focus == None:
            return

        delta = (self.focus.location-self.location)*0.2
        self.location+=delta
        zoomDelta = (self.zoomf-self.zoom)*0.05
        if zoomDelta != 0:
            self.zoom += zoomDelta
            self.buffer = Surface((int(self.width*self.zoom),int(self.height*self.zoom)))

    #determines which space we're rendering from
    def bindSpace(self,space):
        self.space = space
