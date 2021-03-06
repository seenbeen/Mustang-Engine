#-------------------------------------------------------------------------------
# Name:        menus.py
# Purpose:     I have a bunch of things for Mustang Cannon's menus
#
# Author:      Simon
#
# Created:     16/12/2013
# Copyright:   (c) Simon 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import pygame
import abc

import utils
from m_engine import Engine
from m_engine import InputManager
from gui import overlay # THERE'S A PYGAME.OVERLAY WTFWTF
import achievements

pygame.font.init()

class MenuHandler:
    '''
    This guy manages all of the menus outside of gameplay.
    Known issue: flashes the main menu for one frame after starting gameplay.
    '''

    def __init__(self, screenDimensions=(800,600), startingMenuKey="MAIN"):
        '''
        Loads the info for all of the menus.
        '''
        self.dimensions = self.w,self.h = screenDimensions
        self.menus = dict()
        self.menus["MAIN"] = Menu(self, "Main Menu", [('Play Game', 'CHOOSESTAGE'), ('Achievements', 'ACHIEVEMENTS'), ('Options', "OPTIONS"), ('Exit', 'QUIT')], self.dimensions)
        self.menus["CHOOSESTAGE"] = Menu(self, "Choose Stage", [('Front Rotunda (right now just launches the game)', 'PLAYGAME\tFront Rotunda'),('Back', 'MAIN')], self.dimensions)

        # ====== load achievements menu ======
        achBadges = [achievements.AchievementBadge(ach) for ach in achievements.achievements]
        # line up the achBadges; might make this follow the screen dimensions in the future
        left, top, nAcross, xPadding, yPadding = 120, 200, 8, 2, 4
        for i in range(len(achBadges)):
            x = (i % nAcross)
            y = (i // nAcross)
            achBadges[i].topleft = (left + x*(achievements.AchievementBadge.WIDTH_NORMAL + xPadding), top + y*(achievements.AchievementBadge.HEIGHT_NORMAL+yPadding))
        self.menus["ACHIEVEMENTS"] = Menu(self, "Achievements", [("Back", "MAIN")], self.dimensions, pygame.Color(0,0,0,255), achBadges)

        self.menus["OPTIONS"] = Menu(self, "Options",
                                      [("Play SFX (doesn't do anything yet): True/False will be displayed here", "SETOPTION\tSFX"),
                                      ("Play Music (nothing gets changed yet): ", "SETOPTION\tMUSIC"),
                                      ("Back", "MAIN")], self.dimensions)

        self.currentMenuKey = startingMenuKey

    def _setCurrentKey(self, key):
        self.currentMenuKey = key

    def update(self):
        self.menus[self.currentMenuKey].update()

    def parseAction(self, action):
        ''' Takes the a string from a MenuItem that was clicked '''
        if action == "QUIT":
            Engine.state = "QUIT"
        elif action.startswith("PLAYGAME"): # something else would go here later on but just whatever
            Engine.state = "Game"
            self._setCurrentKey("MAIN")
        elif action.startswith("SETOPTION"): # this will disappear once options are fixed up
            self._setCurrentKey("OPTIONS")
        else:
            self._setCurrentKey(action)

    def render(self, surf):
        self.menus[self.currentMenuKey].render(surf)

class Menu(overlay.Overlay):
    '''
    This class can be used for in-game menus as well as the main menu.
    '''

    TITLE_FONT = pygame.font.SysFont("Comic Sans MS", 18)
    ITEM_FONT = pygame.font.SysFont("Comic Sans MS", 14)

    def __init__(self, menuHandler, name, menuItems, screenDimensions, bkg=pygame.Color(0,0,0,255), otherItems=None):
        '''
        name is a str.  It appears at the top of the screen

        menuItems is a list of form [("label1", "target1"), ...].  label1
        appears onscreen.  target1 is the string that is passed into MenuHandler
        to be parsed, upon mouse click.

        bkg is a pygame.Surface, colour tuple or None.  If None then it's
        completely transparent.

        otherItems is a list of MenuSprite instances.
        '''
        self.menuHandler = menuHandler
        self.menuButtons = self.makeMenuButtons(menuItems, screenDimensions)
        super().__init__(screenDimensions,
                         self.menuButtons + (otherItems if otherItems is not None else []),
                         bkg)

        self.dimensions = screenDimensions

        titlePic = type(self).TITLE_FONT.render(name, True, (255,255,255))
        titlePos = titlePic.get_rect(midtop=(screenDimensions[0]//2,10)).topleft
        titleElement = overlay.BasicOverlayElement(titlePic, titlePos, MenuItem.FOREGROUND_LAYER_NUMBER+1)
        self.add(titleElement)

    def makeMenuButtons(self, menuItems, dimensions):
        btns = []
        for i in range(len(menuItems)):
            posx, posy = 50, dimensions[1]-self.ITEM_FONT.get_height()*(len(menuItems)-i-1)-100
            btns.append(MenuItem(self.menuHandler, menuItems[i][0], menuItems[i][1], posx, posy, self.ITEM_FONT))
        return btns

class MenuItem(overlay.TextOverlayElement):

    FOREGROUND_LAYER_NUMBER = 9999

    def __init__(self, menuHandler, label, action, left, top, itemFont, col=(255,255,255), hoverCol = (255,255,0)):
        super().__init__(itemFont, label, (left,top), col, hoverCol)
        self.menuHandler = menuHandler
        self.action = action

        self._layer = type(self).FOREGROUND_LAYER_NUMBER # higher layer number makes foreground

    def onClick(self):
        print('clicked ' + self.label)
        self.menuHandler.parseAction(self.action)
