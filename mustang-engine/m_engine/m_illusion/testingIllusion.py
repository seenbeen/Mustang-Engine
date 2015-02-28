import sys; import os
sys.path.insert(0, os.path.abspath('..'))

from mustangillusion import *

screen = display.set_mode((800,600))

running = True

count = 0

clock = time.Clock()

ParticleSpace.addForce(AreaGravity(400,300,1,500))
ParticleSpace.addForce(AreaGravity(600,450,1,400))
ParticleSpace.addForce(AreaGravity(600,150,1,400))
ParticleSpace.addForce(AreaGravity(200,150,1,400))
ParticleSpace.addForce(AreaGravity(200,450,1,400))

ang = 0
col = [(255,255,0),(255,0,0),(0,255,0),(0,255,255),(0,0,0)]*5

while running:
    for evt in event.get():
        if evt.type == QUIT:
            running = False
        if evt.type == MOUSEBUTTONDOWN:
            if evt.button == 5:
                ang = (ang+10)%360
            if evt.button == 4:
                ang = (ang-10)%360

    count = (count+1)%5 if count > 0 else 0
    mb = mouse.get_pressed()
    mx,my = mouse.get_pos()
    if mb[0] == 1 and count == 0:
        for i in range(5):
            p = Beam(mx,my,500,col)
            p.velocity += Vect2D(math.cos(math.radians(ang))*10+randint(-2,2),math.sin(math.radians(ang))*10)
            ParticleSpace.addParticle(p)
        count = 1
    ParticleSpace.update()
    screen.fill((0,0,0))
    draw.circle(screen,(255,0,0),(400,300),20)
    draw.circle(screen,(255,0,0),(600,450),20)
    draw.circle(screen,(255,0,0),(600,150),20)
    draw.circle(screen,(255,0,0),(200,450),20)
    draw.circle(screen,(255,0,0),(200,150),20)
    draw.line(screen,(0,0,255),(mx,my),(mx+math.cos(math.radians(ang))*10,my+math.sin(math.radians(ang))*10))
    ParticleSpace.render(screen)
    display.update()
    clock.tick(30)
quit()
