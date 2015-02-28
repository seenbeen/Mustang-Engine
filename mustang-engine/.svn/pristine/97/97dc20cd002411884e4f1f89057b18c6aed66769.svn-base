#-------------------------------------------------------------------------------
# Name:        properties_example_1.py
# Purpose:
#
# Author:      Simon
#
# Created:     01/01/2014
# Copyright:   (c) Simon 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

"""
In pygame.rect.Rect, this works:
    r = Rect(10,20,5,6)
    r.bottom = 0
    print(r.y) # prints -6; somehow by just changing r.bottom, it knew to change r.y

In this example I will try to replicate the powers of pygame.rect.Rect, but in
one dimension, using properties.
"""

def main():
    a = LineSegment(0, 10)
    b = LineSegment(1,3)
    print("a",a)
    print("b",b)
    print("moving a.right to 15")
    a.right = 15
    print("a",a)
    print("making b.width -1")
    b.width = -1
    print("b",b)
    print("a.left",a.left)

class LineSegment:
    '''
    Has left, right, x, width as properties
    '''

    def __init__(self, x, w):
        self._x, self._w = x, w

    def __str__(self):
        return "<Line segment [x={}, w={}]>".format(self.x, self.width)

    # Making x a property (so you can do myLineSegment.x; myLineSegment.x = something; etc.)
    # this one is very trivial
    @property
    def x(self): # a getter
        return self._x
    @x.setter
    def x(self, val):
        try:
            assert(isinstance(val, int))
        except AssertionError:
            raise ValueError("Expected int value")
        self._x = val
    ''' could also do this if I wanted to be able to delete this value
    @x.deleter
    def x(self):
        del self._x
    '''

    left = x # x is an object of type <property>; now using left will refer to x

    # Less trivial; allow user to set the attribute "right"
    @property
    def right(self):
        return self._x + self._w
    @right.setter
    def right(self, val):
        # note that now we pass the intended "right" value but end up modifying self._x
        try:
            assert(isinstance(val, int))
        except AssertionError:
            raise ValueError("Expected int value")
        self._x = val - self._w

    @property
    def width(self):
        return self._w
    @width.setter
    def width(self, val):
        try:
            assert(isinstance(val, int))
        except AssertionError:
            raise ValueError("Expected int value")
        self._w = val

    # I think this is all you need for a line segment in 1D

if __name__ == '__main__':
    main()
