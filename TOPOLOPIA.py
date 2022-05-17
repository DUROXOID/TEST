#DANIEL BRANNON
#2022
import pygame
from random import randint, choice
import math
from time import sleep
pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("TOPOLOPIA")
screen.fill((0, 0, 100))
pygame.display.update()
player = pygame.image.load('/home/pi/Desktop/ASSETS/explorer.png')
x = 0
y = 0
alt = 0
#the smaller this value, the steeper the slopes of the peaks
islandSize = 100
rootXdist = 0
rootyDist = 0
alts = []
xRoots = []
yRoots = []
xDistsFromCen = []
yDistsFromCen = []
#control tide animation - bob is the actual variable that is used and wave is the template that changes.
bob = 0
wave = 0
waveSpeed = 0
waveSlowFactor = 0
running = True
def gen():
    global waveSpeed, waveSlowFactor, islandSize, alts, xRoots, yRoots, xDistsFromCen, yDistsFromCen
    alts = []
    xRoots = []
    yRoots = []
    xDistsFromCen = []
    yDistsFromCen = []
    waveSpeed = islandSize/100
    waveSlowFactor = islandSize/10000
    bob = 0
    wave = 0
    #adds layers
    maxAlt = randint(3, 7)
    for x in range (randint(1, 10)):
        #sets GENERAL base of each peak xRoots/yRoots do NOT matter after xDistsFromCen/yDistsFronCen are set
        xRoots.append(randint(-10*islandSize, 10*islandSize))
        yRoots.append(randint(-10*islandSize, 10*islandSize))
    for i in range (maxAlt):
        for j in range (len(yRoots)):
            alts.append(i)
            #adds the coordinates to the list with a offset for variation (actual value used)
            xDistsFromCen.append(xRoots[j] + round(randint(-0.4*islandSize, 0.4*islandSize)))
            yDistsFromCen.append(yRoots[j] + round(randint(-0.4*islandSize, 0.4*islandSize)))
    #how many stacks to affect (h is what stack is affected)
    for h in range(randint(0, len(xRoots))):
        #what value to start deleting values over
        newMaxAlt = randint(2, 7)
        for d in range(len(alts)):
            if alts[d]>newMaxAlt and d%len(xRoots)==h:
                alts[d] = -100
                #just any random float works - we just need to make sure that it is a number that can not be picked by randint
                xDistsFromCen[d] = 5.78
                yDistsFromCen[d] = 5.78
    alts = list(filter((-100).__ne__, alts))
    xDistsFromCen = list(filter((5.78).__ne__, xDistsFromCen))
    yDistsFromCen = list(filter((5.78).__ne__, yDistsFromCen))
while True:
    running = True
    gen()
    while running:
        pygame.time.delay(10)
        for event in pygame.event.get():
            mousex, mousey = pygame.mouse.get_pos()
            xLead = round((mousex-300)/(250 - (5*alt) - islandSize))
            yLead = round((mousey-300)/(250 - (5*alt) - islandSize))
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    islandSize=islandSize-5
                    gen()
                if event.button == 2:
                    gen()
                if event.button == 3:
                    islandSize=islandSize+5
                    gen()
        x -= xLead
        y -= yLead
        #wave code
        if(wave >0):
            waveSpeed = waveSpeed -waveSlowFactor
        else:
            waveSpeed = waveSpeed +waveSlowFactor
        wave += waveSpeed
        screen.fill((0, 0, 100))
        for i in range (len(alts)):
            if(alts[i] == 1):
                bob = round(islandSize/150*wave)
            elif(alts[i] == 0):
                bob = round((-0.01*islandSize)*wave + islandSize/2)
            else:
                bob = 0
            #color rule
            if(alts[i]== 0):
                shade = pygame.Color(0, 0, 200)
                if(math.hypot(x+xDistsFromCen[i]-300, y+yDistsFromCen[i]-300)< islandSize * 8):
                    alt = 0
            if(alts[i]== 1):
                shade = pygame.Color(205, 153, 102)
                if(math.hypot(x+xDistsFromCen[i]-300, y+yDistsFromCen[i]-300)< (islandSize * 7)+bob):
                    alt = 1
            if(alts[i]== 2):
                shade = pygame.Color(229, 201, 149)
                if(math.hypot(x+xDistsFromCen[i]-300, y+yDistsFromCen[i]-300)< islandSize * 6):
                    alt = 2
            if(alts[i]== 3):
                shade = pygame.Color(0, 100, 0)
                if(math.hypot(x+xDistsFromCen[i]-300, y+yDistsFromCen[i]-300)< islandSize * 5):
                    alt = 3
            if(alts[i]== 4):
                shade = pygame.Color(0, 200, 0)
                if(math.hypot(x+xDistsFromCen[i]-300, y+yDistsFromCen[i]-300)< islandSize * 4):
                    alt = 5
            if(alts[i]== 5):
                shade = pygame.Color(50, 50, 50)
                if(math.hypot(x+xDistsFromCen[i]-300, y+yDistsFromCen[i]-300)< islandSize * 3):
                    alt = 8
            if(alts[i]== 6):
                shade = pygame.Color(150, 150, 150)
                if(math.hypot(x+xDistsFromCen[i]-300, y+yDistsFromCen[i]-300)< islandSize * 2):
                    alt = 13
            if(alts[i]== 7):
                shade = pygame.Color(250, 250, 250)
                if(math.hypot(x+xDistsFromCen[i]-300, y+yDistsFromCen[i]-300)< islandSize):
                    alt = 21
            pygame.draw.circle(screen, (shade),[x+xDistsFromCen[i],y+yDistsFromCen[i]], (islandSize * (8-alts[i])) + bob, 0)
        pygame.draw.circle(screen, (0, 13, 13),[300, 300], alt+round((islandSize/3)),0)
        pygame.display.update()
