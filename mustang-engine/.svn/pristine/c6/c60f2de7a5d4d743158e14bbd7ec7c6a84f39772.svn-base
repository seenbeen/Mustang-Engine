#-------------------------------------------------------------------------------
# Name:        overlay.py
# Purpose:     Superclass things for HUD, menus, etc.
#
# Author:      Simon
#
# Created:     31/12/2013
# Copyright:   (c) Simon 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import abc
from pygame import *

from m_engine import InputManager
import utils

font.init() # this is pygame.font.init()

"""
notes to self:
    LayeredUpdates.sprites() gives background sprites first
    lower layer = background, higher layer = foreground
"""

class Overlay(metaclass=abc.ABCMeta):
    '''
    An Overlay has OverlayElements that are drawn onto the screen and can be
    interacted with using the mouse.
    The current behaviour is that all *visible* elements are interacted via
    mouse rollover, but only the top one is clicked.
    '''

    def __init__(self, bounds, elements, bkg):
        '''
        bounds is one of:
            Rect
            (width,height) - defaults to Rect(0,0,width,height)
            (left,top,width,height) - still converted to Rect
        elements is a list of OverlayElements.
        bkg is a pygame.Surface, colour tuple or None.  If None then it's
        completely transparent.
        '''
        if len(bounds) == 2:
            self.bounds = Rect((0,0), bounds)
        else:
            self.bounds = Rect(bounds)
        self._elements = sprite.LayeredUpdates(elements)
        self.bkg = bkg
        self._hovering = sprite.Group()

    @property
    def elements(self):
        return self._elements

    @property
    def offset(self):
        return self.bounds.topleft

    def add(self, *overlayElements):
        for overlayElement in overlayElements:
            self._elements.add(overlayElement)

    def update(self):
        '''
        Updates stored OverlayElements.
        '''
        # Check for mouse-clicking
        for evt in InputManager.events:
            if evt.type == MOUSEBUTTONDOWN:
                if evt.button in (1,3): # left or right mouse button
                    clicked = True
                    break
        else:
            clicked = False

        # Update hovering over things; hovered element(s) are no longer made foreground.
        pos = InputManager.mx - self.offset[0], InputManager.my - self.offset[1]
        hovers = [i for i in self._elements.get_sprites_at(pos) if (i.collideMode == i.RECT_COLLIDE or i.getAlphaAtAbsolute(*pos) > 0)] # background first
        for i in range(len(hovers)-1, -1, -1): # foreground first
            el = hovers[i]
            if el not in self._hovering:
                self._hovering.add(el)
                el.onHover()
            if el.getAlphaAtAbsolute(*pos) == 255:
                break
        if clicked and len(hovers) > 0:
            hovers[-1].onClick()
        for hover in self._hovering:
            if hover not in hovers:
                hover.onUnhover()
                self._hovering.remove(hover)

        self._elements.update()

    def render(self, surf):
        '''
        Redraws the entire background every time (might change in future)
        Uses pygame.sprite.LayeredUpdates.draw for OverlayElements
        '''
        # draw bkg
        if isinstance(self.bkg, Surface):
            surf.blit(self.bkg, self.topleft)
        elif self.bkg is None:
            pass
        else: # should be a colour
            surf.fill(self.bkg)

        # draw elements
        ##self._elements.draw(surf)
        # draw with offset
        for el in self._elements.sprites():
            surf.blit(el.image, el.rect.move(self.offset[0], self.offset[1]))

class OverlayElement(sprite.Sprite, metaclass=abc.ABCMeta):
    '''
    Things that are put into an overlay screen that can be clicked, hovered, etc.
    Decided against making the functions below abc.abstractmethod since it would
    just be inconvenient.
    '''
    ALPHA_COLLIDE, RECT_COLLIDE = 0, 1
    def __init__(self):
        super().__init__()
        self.collideMode = type(self).ALPHA_COLLIDE

    def onHover(self):
        pass

    def onUnhover(self):
        pass

    def onClick(self):
        pass

    def inRelativeBounds(self, x, y):
        return 0 <= x < self.rect.width and 0 <= y < self.rect.height

    def getAlphaAtRelative(self, x, y):
        if self.inRelativeBounds(x,y):
            try:
                return self.image.get_at((x,y)).a
            except IndexError: # self.image is smaller than self.rect; behaviour may change to follow image size instead of rect size
                return 0
        return 0

    def getAlphaAtAbsolute(self, x, y):
        return self.getAlphaAtRelative(x-self.rect.x, y-self.rect.y)

class BasicOverlayElement(OverlayElement):
    '''
    Give it an image and a position.  It does nothing.
    '''
    def __init__(self, img, pos, layer=0):
        '''
        img is Surface, pos is tuple (len 2) for center of element, layer is int
        (optional) for LayeredUpdates to use.
        '''
        super().__init__()
        self.image, self.rect, self._layer = img, img.get_rect(topleft=pos), layer

class TextOverlayElement(OverlayElement):
    '''
    Give it the font, the label, position, the colour(s).
    It will set itself to use RECT_COLLIDE.
    This simple implementation doesn't do anything upon hover/click.
    '''
    DEFAULT_FONT = font.SysFont("Comic Sans MS", 12)

    def __init__(self, fontObj, label, pos, normalCol, hoverCol=None):
        '''
        fontObj is of type font.Font, or None if you wanna use Comic Sans MS 12
        label is str
        pos is topleft (tuple)
        normalCol and hoverCol are ideally pygame.Color; if not, then a tuple.
        '''
        super().__init__()

        self.__pos = pos
        self.font = type(self).DEFAULT_FONT if fontObj is None else fontObj
        self.normalCol = normalCol
        self.hoverCol = self.normalCol if hoverCol is None else hoverCol

        self.setLabel(label)

    def setLabel(self, label):
        self.label = label
        # make images
        self.normalImg = self.font.render(self.label, True, self.normalCol)
        if self.hoverCol != None:
            self.hoverImg = self.font.render(self.label, True, self.hoverCol)
        else:
            self.hoverImg = self.normalImg
        self.image = self.normalImg
        self.rect = self.image.get_rect(topleft = (self.__pos))
        self.collideMode = type(self).RECT_COLLIDE

    def onHover(self):
        self.image = self.hoverImg

    def onUnhover(self):
        self.image = self.normalImg

"""
ANY CLASSES BELOW THIS ARE TEMPORARY
"""
class BkgBox(OverlayElement):
    ''' temporary- used in testing out LayeredUpdates. '''
    def __init__(self):
        super().__init__()
        self.image = Surface((100,100))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect(topleft=(10,400))
