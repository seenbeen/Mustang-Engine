import math
import heapq

class Vect2D():
    def __init__(self,x=0,y=0):
        self.components = {"x":x,"y":y}
        
    def __str__(self):
        return "Vect2D: "+repr(self.components)
    def __repr__(self):
        return "Vect2D: "+repr(self.components)

    def __getitem__(self,value):
        if isinstance(value,str):
            unpack = list(value)
            endl = []
            for x in unpack:
                if x == "x":
                    endl.append(self.components["x"])
                if x == "y":
                    endl.append(self.components["y"])
            if len(endl) == 1:
                return endl[0]
            return endl
        elif isinstance(value,int):
            return list(self.components.values())[value]

        raise TypeError("unsupported operand type(s) for subscript: '{}' and '{}'".format(type(self).__name__,type(value).__name__))
            
    def __mul__(self,value):
        a = self.components
        if isinstance(value,Vect2D): #dot
            b = value.components
            return a["x"]*b["x"]+a["y"]*b["y"]
        elif isinstance(value,int) or isinstance(value,float): #scale
            return Vect2D(a["x"]*value,a["y"]*value)

        raise TypeError("unsupported operand type(s) for *: '{}' and '{}'".format(type(self).__name__,type(value).__name__))

    def __imul__(self,value):
        a = self.components
        if isinstance(value,int) or isinstance(value,float):
            a["x"]*=value
            a["y"]*=value
            return self

        raise TypeError("unsupported operand type(s) for *=: '{}' and '{}'".format(type(self).__name__,type(value).__name__))

    def __div__(self,value):
        if isinstance(value,int) or isinstance(value,float):
            return self*(1.0/value)

        raise TypeError("unsupported operand type(s) for /: '{}' and '{}'".format(type(self).__name__,type(value).__name__))
    def __idiv__(self,value):
        if isinstance(value,int) or isinstance(value,float):
            self*=(1.0/value)
            return self

        raise TypeError("unsupported operand type(s) for /=: '{}' and '{}'".format(type(self).__name__,type(value).__name__))
                        
    def __truediv__(self,value):
        return self.__div__(value)
    
    def __add__(self,value):
        a = self.components
        if isinstance(value,Vect2D):
            b = value.components
            return Vect2D(a["x"]+b["x"],a["y"]+b["y"])
                        
        raise TypeError("unsupported operand type(s) for +: '{}' and '{}'".format(type(self).__name__,type(value).__name__))

    def __iadd__(self,value):
        a = self.components
        if isinstance(value,Vect2D):
            b = value.components
            a["x"]+=b["x"]
            a["y"]+=b["y"]
            return self
                        
        raise TypeError("unsupported operand type(s) for +=: '{}' and '{}'".format(type(self).__name__,type(value).__name__))

    def __sub__(self,value):
        if isinstance(value,Vect2D):
            return self+value*(-1)

        raise TypeError("unsupported operand type(s) for -: '{}' and '{}'".format(type(self).__name__,type(value).__name__))

    def __isub__(self,value):
        if isinstance(value,Vect2D):
            self+=value*(-1)
            return self

        raise TypeError("unsupported operand type(s) for -=: '{}' and '{}'".format(type(self).__name__,type(value).__name__))

    def __neg__(self):
        return self*(-1)
    
    def __pos__(self):
        return self

    def __abs__(self):
        a = self.components
        return math.hypot(a["x"],a["y"])
    
    def unit(self):
        return self/abs(self)
    def copy(self):
        return Vect2D(self.components["x"],self.components["y"])
class Point2D():
    def __init__(self,x=0,y=0):
        self.components = {"x":x,"y":y}
        
    def __str__(self):
        return "Point2D: "+repr(self.components)
    def __repr__(self):
        return "Point2D: "+repr(self.components)

    def __getitem__(self,value):
        if isinstance(value,str):
            unpack = list(value)
            endl = []
            for x in unpack:
                if x == "x":
                    endl.append(self.components["x"])
                if x == "y":
                    endl.append(self.components["y"])
            if len(endl) == 1:
                return endl[0]
            return endl
        elif isinstance(value,int):
            return list(self.components.values())[value]

        raise TypeError("unsupported operand type(s) for subscript: '{}' and '{}'".format(type(self).__name__,type(value).__name__))
                        
    def __sub__(self,value):
        a = self.components
        if isinstance(value,Point2D):
            b = value.components
            return Vect2D(a["x"]-b["x"],a["y"]-b["y"])
        if isinstance(value,Vect2D):
            b = value.components
            return Point2D(a["x"]-b["x"],a["y"]-b["y"])
        
        raise TypeError("unsupported operand type(s) for -: '{}' and '{}'".format(type(self).__name__,type(value).__name__))

    def __isub__(self,value):
        a = self.components
        if isinstance(value,Vect2D):
            b = value.components
            a["x"]-=b["x"]
            a["y"]-=b["y"]
            return self

        raise TypeError("unsupported operand type(s) for -=: '{}' and '{}'".format(type(self).__name__,type(value).__name__))            

    def __add__(self,value):
        a = self.components
        if isinstance(value,Vect2D):
            b = value.components
            return Point2D(a["x"]+b["x"],a["y"]+b["y"])

        raise TypeError("unsupported operand type(s) for +: '{}' and '{}'".format(type(self).__name__,type(value).__name__))

    def __iadd__(self,value):
        a = self.components
        if isinstance(value,Vect2D):
            b = value.components
            a["x"]+=b["x"]
            a["y"]+=b["y"]
            return self

        raise TypeError("unsupported operand type(s) for +=: '{}' and '{}'".format(type(self).__name__,type(value).__name__))
                        
    def dist(self,point2D):
        a,b = self.components,point2D.components
        return math.hypot(a["x"]-b["x"],a["y"]-b["y"])
    def copy(self):
        return Vect2D(self.components["x"],self.components["y"])

class PriorityQueue():
    def __init__(self):
        self.queue = []
    def push(self,item):
        heapq.heappush(self.queue,item)
    def pop(self):
        return heapq.heappop(self.queue)
    def hasNext(self):
        return len(self.queue)>0
    def clear(self):
        self.queue = []
        
def sign(n):
    if n < 0:
        return -1
    if n > 0:
        return 1
    return 0
