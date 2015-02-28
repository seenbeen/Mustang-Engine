#-------------------------------------------------------------------------------
# Name:        utils.py
# Purpose:     Has misc. utilities like multilineRender.
#
# Author:      Simon
#
# Created:     21/12/2013
# Copyright:   (c) Simon 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from pygame import *
import getpass

font.init()

def getCurrentUsername():
    '''
    Returns the name of the user account currently logged in.  Don't trust it
    to be hacker-proof.
    Availability: Unix, Windows, Mac (tested on Zihao's Macbook Air)
    '''
    return getpass.getuser() # might or might not work for Mac OS

def splitStringToLineWrap(textFont, text, maxWidth):
    '''
    Returns a list of strings, each of which is not longer than maxWidth when
    rendered using textFont.  The text is ideally broken up by spaces, and
    always at existing newline characters.
    '''
    lines = []
    for line in text.split("\n"):
        words = line.split(" ")
        while len(words) > 0:
            for numWords in range(1, len(words)+1):
                lineWidth = textFont.size(" ".join(words[:numWords]))[0]
                if lineWidth > maxWidth:
                    numWords -= 1
                    break
            else:
                numWords = len(words)

            if numWords == 0: #wrap the word around
                for numLetters in range(1, len(words[0])+1):
                    wordWidth = textFont.size(words[0][:numLetters])[0]
                    if wordWidth > maxWidth:
                        numLetters -= 1
                        break
                numWords = 1
                words.insert(1,words[0][numLetters:])

            textLine = " ".join(words[:numWords])
            lines.append(textLine)
            words = words[numWords:]
    return lines


def multilineRender(textFont, text, maxWidth, col, antiAliasing=True):
    '''
    Returns Pygame's rendering of the text in the given font, but on multiple
    lines with the max width given in pixels.  A word longer than maximum width
    will wrap around.
    '''
    rowH = textFont.get_linesize()
    lines = splitStringToLineWrap(textFont, text, maxWidth)
    rend = Surface((maxWidth, rowH * len(lines)), SRCALPHA, 32)
    for ind,line in enumerate(lines):
        rend.blit(textFont.render(line, antiAliasing, col), (0,ind*rowH))
    return rend

def getNumTransparentRows(surf, fromTop = True):
    '''
    surf is a pygame.Surface.
    Gets the number of fully transparent rows starting from the top by default.
    if fromTop is False then it's from bottom.
    '''
    for vShift in (range(surf.get_height()) if fromTop else range(surf.get_height()-1, -1, -1)):
        for x in range(surf.get_width()):
            if surf.get_at((x,vShift)).a > 0: # not a fully transparent pixel
                return vShift if fromTop else (surf.get_height()-1-vShift)

def getNumTransparentColumns(surf, fromLeft = True):
    '''
    surf is a pygame.Surface.
    Gets the number of fully transparent columns starting from the left by default.
    if fromRight is False then it's from right.
    '''
    for hShift in (range(surf.get_width()) if fromLeft else range(surf.get_width()-1, -1, -1)):
        for y in range(surf.get_height()):
            if surf.get_at((hShift,y)).a > 0: # not a fully transparent pixel
                return hShift if fromLeft else (surf.get_width()-1-hShift)