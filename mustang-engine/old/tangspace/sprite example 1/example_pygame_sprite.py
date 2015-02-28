#-------------------------------------------------------------------------------
# Name:        example_pygame_sprite.py
# Purpose:
#
# Author:      Simon
#
# Created:     01/01/2014
# Copyright:   (c) Simon 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

"""
So this module gives a basic example of how Pygame's sprite module can be used.
There's some more advanced stuff that I haven't looked into, like RenderUpdates
and other types of Groups which can be used for more efficient drawing and
possibly other things.

You may find this to be of use, or you may just decide to avoid it altogether.
You might or might not be able to combine this with the pro quad-space stuff and
other optimization things out there.  If this can be adapted to our needs,
though, then it will give a good standard API that can be more familiar overall.

Another major thing you might not like is the maintaining of a self.image
attribute; this would make it costly to handle rotating images.  The only
workaround I've thought of is extending pygame.sprite.Group and overriding .draw(surf)
so that it checks for a draw(surf) method of each sprite:
    def draw(surf):
        for sprite in self.sprites():
            if hasattr(sprite, "draw"):
                sprite.draw(surf)
            else:
                surf.blit(sprite.image, sprite.rect)

All subclasses of pygame.sprite.Sprite need to have these attributes:
    update() # optional; default implementation does nothing
    image # pygame.Surface
    rect  # pygame.rect.Rect
    layer # int; optional; used for more advanced groups like LayeredUpdates
    kill() # removes itself from all of its groups
    alive() # bool; tells if it's in any groups
Note that pygame.sprite.DirtySprite has some more advanced stuff too

All pygame.sprite.Group and related classes have these attributes of interest:
    add(sprite), remove(sprite), empty()
    update() # just calls sprite.update() for each sprite
    clear(dest, bkg) # uses the rect attr. of each sprite to selectively redraw bkg onto dest (use before moving sprites)
    draw(dest) # uses each sprite's image and rect attribute
pygame.sprite.GroupSingle is a Group that always has at most one Sprite:
    sprite # returns None if there is no sprite in the group
Note that only some groups have layers, ordered iteration, etc.
You can use in, len, bool and iter on any Group.

Documentation gives info on these convenience methods:
pygame.sprite.spritecollide 	— 	Find sprites in a group that intersect another sprite.
pygame.sprite.collide_rect 	— 	Collision detection between two sprites, using rects.
pygame.sprite.collide_rect_ratio 	— 	Collision detection between two sprites, using rects scaled to a ratio.
pygame.sprite.collide_circle 	— 	Collision detection between two sprites, using circles.
pygame.sprite.collide_circle_ratio 	— 	Collision detection between two sprites, using circles scaled to a ratio.
pygame.sprite.collide_mask 	— 	Collision detection between two sprites, using masks.
pygame.sprite.groupcollide 	— 	Find all sprites that collide between two groups.
pygame.sprite.spritecollideany 	— 	Simple test if a sprite intersects anything in a group.

See http://www.pygame.org/docs/ref/sprite.html for info
"""

from pygame import *
import math

def run():
    screen = display.set_mode((640,480))
    bkg = image.load("menu_bkg.png").convert()
    screen.blit(bkg, (0,0))
    display.set_caption("WASD to shoot.  Mouse to move.  Kill the enemies!")

    goodGuy = sprite.GroupSingle(GoodGuy((100,100)))
    badGuys = sprite.Group()
    for i in range(4):
        badGuys.add(BadGuy(i*100, 10, goodGuy.sprite))
    bullets = sprite.Group()

    gameClock = time.Clock()

    running = True
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                running = False
            elif evt.type == KEYDOWN:
                if evt.key == K_ESCAPE:
                    running = False
                if goodGuy.sprite is not None: # or len(goodGuy) > 0:
                    if evt.key == K_a:
                        bullets.add(Bullet(goodGuy.sprite.rect.centerx, goodGuy.sprite.rect.centery, math.pi))
                    elif evt.key == K_w:
                        bullets.add(Bullet(goodGuy.sprite.rect.centerx, goodGuy.sprite.rect.centery, 3.0/2*math.pi))
                    elif evt.key == K_s:
                        bullets.add(Bullet(goodGuy.sprite.rect.centerx, goodGuy.sprite.rect.centery, math.pi/2))
                    elif evt.key == K_d:
                        bullets.add(Bullet(goodGuy.sprite.rect.centerx, goodGuy.sprite.rect.centery, 0.0))
                    display.set_caption("# bullets: " + str(len(bullets)))


        # redraw background over all sprites; I think advanced groups use the
        # "Dirty" attribute to determine if it's necessary for a given sprite
        for group in (goodGuy, badGuys, bullets):
            group.clear(screen, bkg)

        # calls .update() on each sprite
        for group in (goodGuy, badGuys, bullets):
            group.update()

        # bullets hitting badguys?  both disappear.
        #now this logic might go somewhere else or it could stay here
        # see http://www.pygame.org/docs/ref/sprite.html#pygame.sprite.groupcollide
        sprite.groupcollide(badGuys, bullets, True, True) # bool flags are dokill and dokill2

        # badguys hitting goodguy?
        result = sprite.groupcollide(goodGuy, badGuys, True, False)
        # result is a dict of form {goodguysprite: [collidingbadguy1, ...],...}
        if len(result) > 0: # a badguy touching the goodguy
            display.set_caption("hohoho you lose")
            bullets.empty()

        # does screen.blit(sprite.image, sprite.rect)
        for group in (goodGuy, badGuys, bullets):
            group.draw(screen)

        gameClock.tick(30)

        display.flip()
    quit()

class GoodGuy(sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = image.load("moon.png").convert()
        self.rect = self.image.get_rect(center = pos)

    def update(self):
        # default implementation is empty so not necessary to call super().update()
        self.rect.center = mouse.get_pos()

class BadGuy(sprite.Sprite):
    pic = None
    def __init__(self, x, y, target: sprite.Sprite):
        super().__init__()
        if type(self).pic is None:
            type(self).pic = image.load("runner.png").convert()
        self.image = type(self).pic
        self.rect = self.image.get_rect(center = (x,y))
        self.target = target
    def update(self):
        ''' run towards the target '''
        tx, ty = self.target.rect.center
        if self.rect.centerx < tx:
            self.rect.centerx += 1
        elif self.rect.centerx > tx:
            self.rect.centerx -= 1
        if self.rect.centery < ty:
            self.rect.centery += 1
        elif self.rect.centery > ty:
            self.rect.centery -= 1

class Bullet(sprite.Sprite):
    pic = None
    def __init__(self, x, y, direction):
        super().__init__()
        # dir is an angle in radians
        self.dir = direction
        if type(self).pic is None:
            type(self).pic = Surface((10,10))
            type(self).pic.fill((0,0,0))
        self.image = type(self).pic
        self.rect = self.image.get_rect(center = (x,y))
        self.screenConstraints = Rect((0,0),display.get_surface().get_size())
        # or display.get_surface().get_rect() which has default pos of (0,0) I think
    def update(self):
        self.rect.move_ip(math.cos(self.dir)*4, math.sin(self.dir)*4)
        # kill self if off screen
        if not self.rect.colliderect(self.screenConstraints):
            display.set_caption("# bullets: " + str(len(self.groups()[0])-1)) # for this example we can assume there's only one group for bullets
            self.kill() # removes self from all pygame sprite groups that it's in

if __name__ == "__main__":
    run()