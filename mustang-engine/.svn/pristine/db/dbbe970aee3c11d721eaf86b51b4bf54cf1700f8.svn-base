#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Simon
#
# Created:     03-01-2014
# Copyright:   (c) Simon 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from pygame import *

from m_engine import *
from gui import overlay
import achievements
import utils

class HUD(overlay.Overlay):
    '''
    In-game HUD
    '''

    LOG_FONT = font.SysFont("Courier New", 14)

    class TempHUDMainMenuButton(overlay.OverlayElement):
        ''' this will disappear soon '''
        def __init__(self):
            super().__init__()
            self.image = font.SysFont("Comic Sans MS", 14).render("main menu", True, (255,0,0))
            self.rect = self.image.get_rect(topleft = (100,100))
            self.collideMode = type(self).RECT_COLLIDE
        def onClick(self):
            print("dawg")
            Engine.state = "Menu"


    def __init__(self, bounds=(0,0,800,600)):
        super().__init__(bounds, [], None)

        self._visibleNotifications = []

        # make a neat button that makes the Engine go back to menu.
        coolBtn = HUD.TempHUDMainMenuButton()
        self.add(coolBtn)

        self.add(FPSBox(self, (100,100)))

        # set up log messages functionality
        self.logArea = LogArea(Rect(self.bounds.x+10, self.bounds.bottom-10-110, 300, 110))
        self.logArea._visible = False
        self._showLogMessages = True
        self.appendLogMessage("Press 'L' to toggle log visibility; scroll funct. forthcoming")
        self.add(self.logArea)

        # temporary thing for that message of encouragement
        self.notifDelay = 100


    def update(self):
        '''
        Calls super().update()

        Might go somewhere else:
            - Calls .update() on all loaded achievements

        - Keystroke 'L' toggles visibility of message log (not notifications)

        Temporary things:
            shows a dummy notification to encourage developers.
        '''
        super().update()

        if self.notifDelay == 0:
            self.showNotification("Notification", "Keep up the hard work!", None, Color(0,0,0,125))
            self.notifDelay = -1
        elif self.notifDelay > 0:
            self.notifDelay -= 1

        for evt in InputManager.events:
            if evt.type == KEYDOWN:
                if evt.key == K_l:
                    self._showLogMessages = not self._showLogMessages

        for ach in achievements.achievements:
            ach.update()

    def showNotification(self, title, message, icon=None, bkg=None):
        '''
        The notification is shown immediately.  Drops in from top and fades away.
        title and message are strings.  icon is pygame.Surface or None.
        bkg is pygame.Surface or pygame.Color or tuple or None.
        '''
        self._elements.add(Notification(self, title, message, icon, bkg))

    def calculateNotificationDestination(self, notif):
        '''
        Determines where a notification (so far only for achievements) should
        go on-screen.  Returns the y-position of the top of the
        notification's ideal position.
        '''
        # not visible; remove and kill.
        if notif.findAlpha() <= 0:
            if notif in self._visibleNotifications:
                self._visibleNotifications.remove(notif)
            notif.kill()
            return -notif.rect.height

        # is visible
        if notif not in self._visibleNotifications:
            self._visibleNotifications.append(notif)

        ind = self._visibleNotifications.index(notif)
        if ind == 0:
            return 0
        return self._visibleNotifications[ind-1].rect.bottom + 4

    def appendLogMessage(self, message):
        ''' message is a string. '''
        self.logArea.appendLogMessage(message)

    def render(self, surf):
        super().render(surf)

class LogArea(overlay.OverlayElement):
    '''
    Displays the logged messages.  For debugging, not in-game info.
    '''
    LOG_FONT = font.SysFont("Courier New", 14)
    def __init__(self, bounds):
        super().__init__()
        self.rect = bounds
        self._image = None
        self.__needsRender = True
        self.msgs = []
        self.textFont = type(self).LOG_FONT
        self.lineHeight = self.textFont.get_height()
        self.scrollLines = -1 # set to -1 to always display most recent messages
                             # this represents the number of lines from the top
                             # to offset.
        self.__dummyPic = Surface((1,1), SRCALPHA, 32)
        self._visible = True

    def update(self):
        for evt in InputManager.events:
            if evt.type == KEYDOWN and evt.key == K_l:
                self._visible = not self._visible

    @property
    def image(self):
        # This is more efficient than updating every single time
        def makeImage(self):
            img = Surface(self.rect.size, SRCALPHA, 32)
            ##img = Surface(self.rect.size)
            ##img.fill((100,100,100))
            if self.scrollLines >= 0:
                x = y = 0
                i = max(0, len(self.msgs)-1-self.getNumRows())
                while i < len(self.msgs) and y < self.rect.height:
                    pic = self.textFont.render(self.msgs[i], True, (255,255,255))
                    draw.rect(img, (0,0,0), pic.get_rect(topleft=(x,y)))
                    img.blit(pic, (x,y))
                    y += self.lineHeight ##pic.get_height()
                    i += 1
            else: # draw from bottom up
                x = 0
                y = self.rect.height
                i = len(self.msgs)-1
                while i >= 0 and y+self.lineHeight > 0:
                    pic = self.textFont.render(self.msgs[i], True, (255,255,255))
                    r = pic.get_rect(bottomleft=(x,y))
                    draw.rect(img, (0,0,0), r)
                    img.blit(pic, r)
                    y -= self.lineHeight
                    i -= 1

            return img

        if not self._visible:
            return self.__dummyPic
        if self.__needsRender:
            self.__needsRender = False
            self._image = makeImage(self)
        return self._image

    def getNumRows(self):
        return int(math.ceil(self.rect.height/self.textFont.get_height()))

    def appendLogMessage(self, message):
        ''' message is a string. '''
        self.__needsRender = True
        self.msgs += utils.splitStringToLineWrap(self.textFont, message, self.rect.width)

    def onClick(self):
        self.appendLogMessage("click")

class FPSBox(overlay.TextOverlayElement):
    ''' Shows the current framerate '''
    def __init__(self, hud, pos):
        super().__init__(None, "one million pounds", pos, Color(0,255,0,0))
        self.__counter = 0
    def update(self):
        if self.__counter == 0:
            self.__counter = 50
            self.setLabel(str(Engine.getFPS()))
        self.__counter -= 1


class Notification(overlay.OverlayElement):
    ''' Useful.  Internal use. '''
    LABEL_FONT = font.SysFont("Comic Sans MS", 20)
    DESC_FONT = font.SysFont("Comic Sans MS", 14)
    WIDTH = 300
    PADDING = 12
    FADE_OUT_DELAY = 150 # this delay and fadeout speed system will change

    def __init__(self, hud, title, message, icon=None, bkg=None):
        super().__init__()
        self.hud = hud
        self.title, self.message, self.icon, self.bkg = title, message, icon, bkg
        self.destination = 0
        self.fadeOutCounter = 0
        self.generateImage()
        self.rect = self.image.get_rect(midbottom = (400,0))
        self.moveCounter = 0
        self.clicked = False

    def update(self):
        keys = InputManager.kb
        self.destination = self.hud.calculateNotificationDestination(self)
        if self.findAlpha() == 0: # temp. fix for jumping around; still doesn't fix -_-
            self.rect.y = self.destination
        else:
            self.rect.top = (self.rect.top*2+self.destination)//3
            if abs(self.rect.top - self.destination) < 3:
                self.rect.top = self.destination
            if self.rect.top == self.destination:
                self.fadeOutCounter += (4 if self.clicked else 1)
            self.image.set_alpha(self.findAlpha())

    def generateImage(self):
        self.nameImg = self.LABEL_FONT.render(self.title, True, (255,255,255))
        self.textImg = utils.multilineRender(self.DESC_FONT, self.message, self.WIDTH-self.PADDING*2-64-4, (255,255,255))

        vShift = utils.getNumTransparentRows(self.nameImg)
        self.image = Surface((self.WIDTH,
                              max(64 + self.PADDING*2,
                                  self.PADDING*2 + self.nameImg.get_height() + self.textImg.get_height())))
        self.image.blit(self.nameImg, (self.PADDING+64+self.PADDING,self.PADDING-vShift))
        self.image.blit(self.textImg, (self.PADDING+64+self.PADDING,self.PADDING+self.LABEL_FONT.get_linesize()-vShift))
        if self.icon != None:
            self.image.blit(self.icon, (self.PADDING,self.PADDING))

    def findAlpha(self):
        return min(255, max(255 - self.fadeOutCounter*2 + type(self).FADE_OUT_DELAY, 0))

    def onClick(self):
        self.clicked = True
