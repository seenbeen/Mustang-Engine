#-------------------------------------------------------------------------------
# Name:        achievements.py
# Purpose:     Things for in-game achievements (e.g. "Marathon Runner- 42km")
#
# Author:      Simon
#
# Created:     18/12/2013
# Copyright:   (c) Simon 2013
# Licence:     Currently licensed for the MCannon team's eyes only.
#-------------------------------------------------------------------------------

# temporary thing: module loads the achievement data from ini file and direct image.load calls as soon as module is loaded

from pygame import *
import configparser

from m_engine import Engine
from gui.overlay import OverlayElement
import utils as utils

init() # this is pygame.init()

achievements = []

def loadAchievementDataFromIniFile(file):
    '''
    Loads the achievements from a file-like object (type of .ini), overwriting
    any previously loaded Achievement objects.
    Use this module's achievements attribute to access the achievements.
    Returns None
    '''
    global achievements
    if hasattr(list, "clear"):
        achievements.clear() # if there's a method then use it
    else: #stupid python 3.2 and earlier #smh
        achievements = []

    cp = configparser.ConfigParser()
    cp.read_file(file)
    for name in cp.sections():
        desc = cp.get(name, "description")
        iconInfo = cp.get(name, "icon")
        if iconInfo == "None":
            icon = None
        else:
            icon = image.load("assets/achievements/" + iconInfo)
        achieved = cp.getboolean(name, "achieved")
        ach = Achievement(name, desc, icon, achieved)

        # get requirements for passing
        # a lot of things are floats because I can represent +/- infinity
        ach.minDist = cp.getfloat(name, "minDist")
        ach.maxDist = cp.getfloat(name, "maxDist")
        ach.minLaunchAngle = cp.getfloat(name, "minLaunchAngle")
        ach.maxLaunchAngle = cp.getfloat(name, "maxLaunchAngle")

        achievements.append(ach)

def saveAchievementDataToIniFile(self, file):
    '''
    Saves the Achievements in this module's achievements attribute to a file
    in INI format.'''
    raise NotImplementedError("DON'T USE ME YET")

    cp = configparser.ConfigParser()
    # write the default stuff here

    # after writing the default stuff, write the individual Achievement data stuff
    for achievement in achievements:
        pass
    cp.write(file)

class Achievement:
    '''
    An in-game achievement.
    It stores its requirements for being achieved, like minimum height (which is
    float("-inf") by default) for example.
    It has its pygame.Surface for its icon (optional), it has a name,
    description, etc. as well, and whether or not it's already been achieved.
    The related AchievementBadge class is used for displaying the Achievement
    in the Achievements menu screen.
    TODO: Revise the AchievementBadge class and the function that gets the badges
    TODO: Combine this with the main_game stuff so it can perform these checks.
    '''
    _MISSING_KEYS = set()

    def __init__(self, name, desc, icon=None, achieved=False):
        ''' all of the requirements will be passed into this initializer eventually '''
        super().__init__()

        self.name, self.desc = name, desc
        if icon == None:
            self.icon = Surface((64,64))
            self.icon.fill((100,100,100))
        else:
            self.icon = icon

        self.achieved = achieved

    def update(self):
        if (not self.achieved) and self._findOutIfAchieved():
            self.achieved = True

    def _findOutIfAchieved(self):
        '''
        Will implement checks based on things like self.minDist, using
        m_engine.Engine.var["key"].
        TODO: implement this
        '''

        # Passed all the tests
        return True

class AchievementBadge(OverlayElement):
    '''
    Used in the Achievements menu.  See Achievement for the more important one.
    This one just acts as something to appear on the grid showing what
    Achievements have and haven't been achieved.
    '''
    WIDTH_NORMAL, HEIGHT_NORMAL = 64, 64
    WIDTH_EXPANDED = 128

    PADDING = 4

    NAME_FONT = font.SysFont("Comic Sans MS", 12)
    DESC_FONT = font.SysFont("Comic Sans MS", 9)

    def __init__(self, ach, topleft=(0,0)):
        '''
        ach is the associated Achievement.
        topleft is of form (left,top) of this AchievementBadge's rectangle.
        '''
        super().__init__()
        self.ach = ach

        self._topleft = topleft

        self.icon = self.ach.icon.copy()
        descImg = utils.multilineRender(self.DESC_FONT, self.ach.desc, self.WIDTH_NORMAL - self.PADDING * 2, (255,255,255))
        nameImg = utils.multilineRender(self.NAME_FONT, self.ach.name, self.WIDTH_NORMAL - self.PADDING * 2, (255,255,255))
        self.overlay = Surface(self.icon.get_size())
        self.overlay.fill((0,0,0))
        self.overlay.set_alpha(100)

        self.expandedImg = Surface((self.WIDTH_NORMAL, self.HEIGHT_NORMAL + self.PADDING + descImg.get_height() + self.PADDING))
        self.expandedImg.blit(self.icon, (0,0))
        self.expandedImg.blit(self.overlay, (0,0))
        self.expandedImg.blit(nameImg, (self.PADDING, self.PADDING - utils.getNumTransparentRows(nameImg)))
        self.expandedImg.blit(descImg, (self.PADDING, self.HEIGHT_NORMAL + self.PADDING - utils.getNumTransparentRows(descImg)))

        self.normalImg = Surface((self.WIDTH_NORMAL, self.HEIGHT_NORMAL))
        self.normalImg.blit(self.icon, (0, 0))

        self.normalRect = self.normalImg.get_rect(topleft=self.topleft)
        self.updateImage(False)

    @property
    def topleft(self):
        return self._topleft

    @topleft.setter
    def topleft(self, value):
        self._topleft = value
        self.rect.topleft = value
##        self.expandedRect.topleft = (self.rect.left, self.rect.top - self.nameImgHeight)

    def updateImage(self, withDescription):
        if withDescription:
            self.image = self.expandedImg
##            self.rect = self.expandedRect
        else:
            self.image = self.normalImg
        if True: # remove this line later
            self.rect = self.normalRect
##            self.rect = Rect(self.topleft, self.image.get_size())
        ##self.image.set_alpha(255 if self.ach.achieved else 100)
        self.image.set_alpha(255)


    def onHover(self):
        ''' makes itself expanded, and moves itself slightly above the rest of the badges '''
        ##self.updateImage(self.ach.achieved)
        self.updateImage(True)
        for g in self.groups():
            if isinstance(g, sprite.LayeredUpdates):
                g.change_layer(self, 1)

    def onUnhover(self):
        ''' retracts description section, moves itself back to same level as rest of badges '''
        self.updateImage(False)
        for g in self.groups():
            if isinstance(g, sprite.LayeredUpdates):
                g.change_layer(self, 0)

# this part will likely move somewhere else in the future.
try:
    loadAchievementDataFromIniFile(open("Assets/achievements/achievements data.ini"))
except FileNotFoundError as e:
    print(e)
    print("Gotta keep Assets folder in same folder as launched py file")