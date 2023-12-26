import pygame, sys
from pygame.locals import *
import random
import button

import time
pygame.init()

FPS = 120
FramePerSec = pygame.time.Clock()
 
# Predefined some colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (122, 122, 122)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
 
# Screen information
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
fontName = "Atlantis International"
font = pygame.font.SysFont(fontName, 100)
font2 = pygame.font.SysFont(fontName, 50)

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

pygame.display.flip()
pygame.display.set_caption("Pong")


#set variables
d = [4, 3]
p1 = 0
p2 = 0
maxAngle = 7
turns = 1
ddy = 0
p1Cool = 30
p2Cool = 30
scene = 'menu'

#options
singlePlayer = True
predictFrames = 30
curve = True
predictCurve = True
randomCurve = True


#buttons
p1img = font.render('1 player', True, WHITE)
p1button = button.Button(SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/3, p1img, 0.4)

p2img = font.render('2 player', True, WHITE)
p2button = button.Button(SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2, p2img, 0.4)

optionsimg = font.render('options', True, WHITE)
optionsbutton = button.Button(SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT*2/3, optionsimg, 0.4)

name = font.render('PONG', True, WHITE)
options = font.render('OPTIONS', True, WHITE)
curveimg = font2.render('Curve', True, WHITE)

check = pygame.image.load('check.png').convert_alpha()
check = pygame.transform.scale(check, (100, 100))
checkbutton = button.Button(SCREEN_WIDTH/2 + 50, SCREEN_HEIGHT/3, check, 0.4)

checked = pygame.image.load('checked.png').convert_alpha()
checked = pygame.transform.scale(checked, (100, 100))
checkedbutton = button.Button(SCREEN_WIDTH/2 + 50, SCREEN_HEIGHT/3, checked, 0.4)

pauseimg = pygame.image.load('pause.png').convert_alpha()
pauseimg = pygame.transform.scale(pauseimg, (100, 100))
pausebutton = button.Button(SCREEN_WIDTH - 50, 20, pauseimg, 0.4)

resumeimg = font.render('resume', True, WHITE)
resumebutton = button.Button(SCREEN_WIDTH/2 - 50, SCREEN_HEIGHT/2, resumeimg, 0.4)

menuimg = font.render('menu', True, WHITE)
menubutton = button.Button(SCREEN_WIDTH/2 - 50, SCREEN_HEIGHT/2 + 50, menuimg, 0.4)

backimg = font.render('back', True, WHITE)
backbutton = button.Button(SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2, backimg, 0.4)




#set object for background
class background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("bg.png")
        self.image = pygame.transform.scale(self.image, (15, 600))
        self.rect = self.image.get_rect()
        self.rect.center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/2) 
    def draw(self, surface):
        surface.blit(self.image, self.rect) 
#set object for ball
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("ball.png")
        self.rect = self.image.get_rect()
        self.rect.center=(300,300) 
        


    

    def move(self, d):
        p1 = False
        p2 = False
        stopcurve = False
        if (self.rect.top < 0 and d[1] < 0) or (d[1] >= 0 and self.rect.bottom > SCREEN_HEIGHT):
            d[1] *= -1
            stopcurve = True
        if self.rect.left < 0:
            p1 = True
            self.rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
            stopcurve = True
        if self.rect.right > SCREEN_WIDTH:
            p2 = True
            self.rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        self.rect.move_ip(d)
        
        return d[0], d[1], p1, p2, self.rect.center[0], self.rect.center[1], stopcurve

 
    def draw(self, surface):
        surface.blit(self.image, self.rect) 
 
#set object for player 1
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (50, SCREEN_HEIGHT/2)
 
    def update(self):
        pressed_keys = pygame.key.get_pressed()

        if self.rect.top > 0:
            if pressed_keys[K_w]:
                self.rect.move_ip(0, -5)
        if self.rect.bottom < SCREEN_HEIGHT:        
            if pressed_keys[K_s]:
                self.rect.move_ip(0, 5)


    def restart(self):
        self.rect.center = (50, SCREEN_HEIGHT/2)
    def draw(self, surface):
        surface.blit(self.image, self.rect)     

# set object for player 2
class Player2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH - 50, SCREEN_HEIGHT/2)
 


    def update(self, ballx, bally, dx, dy, ddy):
        pressed_keys = pygame.key.get_pressed()

        if self.rect.top > 0 and singlePlayer == False:
            if pressed_keys[K_i]:
                self.rect.move_ip(0, -5)
        if self.rect.bottom < SCREEN_HEIGHT and singlePlayer == False:        
            if pressed_keys[K_k]:
                self.rect.move_ip(0, 5)
        if singlePlayer == True:
            for i in range(round((SCREEN_WIDTH - 50 - ballx)/dx - predictFrames)):
                bally += dy
                if bally < 0 or bally > SCREEN_HEIGHT:
                    dy *= -1
                    if ddy < 0:
                        ddy += 0.15
                    else:
                        ddy -= 0.15
                if predictCurve == True:
                    dy += ddy
            if bally < self.rect.center[1] and abs(self.rect.center[1] - bally) > 10 and dx > 0:
                self.rect.move_ip(0, -5)
            elif bally > self.rect.center[1] and abs(self.rect.center[1] - bally) > 10 and dx > 0:
                self.rect.move_ip(0, 5)
            if dx < 0:
                if self.rect.center[1] < SCREEN_HEIGHT/2:
                    self.rect.move_ip(0, 5)
                if self.rect.center[1] > SCREEN_HEIGHT/2:
                    self.rect.move_ip(0, -5)

        
    def restart(self):
        self.rect.center = (750, SCREEN_HEIGHT/2)
    def draw(self, surface):
        surface.blit(self.image, self.rect)    



#make object
P1 = Player()
B1 = Ball()
P2 = Player2()
Background = background()

#creating sprite groups
balls = pygame.sprite.Group()
balls.add(B1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(P2)
all_sprites.add(B1)



#game loop
while True:  
    if scene == 'menu':
        DISPLAYSURF.fill(BLACK)
        DISPLAYSURF.blit(name, (300,50))
        if p1button.draw(DISPLAYSURF):
            singlePlayer = True
            score1 = 0
            score2 = 0
            scene = 'game'
        if p2button.draw(DISPLAYSURF):
            singlePlayer = False
            score1 = 0
            score2 = 0
            scene = 'game'
        if optionsbutton.draw(DISPLAYSURF):
            scene = 'options'
        
    if scene == 'options':
        DISPLAYSURF.fill(BLACK)
        DISPLAYSURF.blit(options, (250,50))
        DISPLAYSURF.blit(curveimg, (SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/3))
        if curve == True:
            if checkedbutton.draw(DISPLAYSURF):
                curve = False
        if curve == False:
            if checkbutton.draw(DISPLAYSURF):
                curve = True

        if backbutton.draw(DISPLAYSURF):
            scene = 'menu'
            time.sleep(0.1)

        
    if scene == 'pause':
        
        pygame.draw.rect(DISPLAYSURF, GRAY, (SCREEN_WIDTH/2 - 70, SCREEN_HEIGHT/2 - 10, 150, 100))
        if resumebutton.draw(DISPLAYSURF):
            scene = 'game'
        if menubutton.draw(DISPLAYSURF):
            scene = 'menu'

            

    
    for event in pygame.event.get():              
            if event.type == QUIT:
                pygame.quit()
                sys.exit()  
    if scene == 'game':
        

        #move ball and get its information
        output = B1.move(d)
        
        P1.update()
        P2.update(output[4], output[5], d[0], d[1], ddy)
        
        p1Cool += 1
        p2Cool += 1

        #change dx and xy
        d[0] = output[0]
        d[1] = output[1]
        
        #check if it hits either wall
        if output[2] == True:
            p2 += 1
        if output[3] == True:
            p1 += 1
        #reset position 
        if output[2] == True or output [3] == True:
            d = [random.randint(-1, 1), random.randint(-3,3)]
            P1.restart()
            P2.restart()
            maxAngle = 7
            turns = 1
            time.sleep(0.5)

        #fill background
        DISPLAYSURF.fill(BLACK)  
        Background.draw(DISPLAYSURF)

        #draw objects
        P1.draw(DISPLAYSURF)
        P2.draw(DISPLAYSURF)
        B1.draw(DISPLAYSURF)

        #search for pressed keys
        pressed_keys = pygame.key.get_pressed()

        #checks for cooldown and reflect if player 1 hits the ball
        if pygame.sprite.spritecollideany(P1, balls):
            if p1Cool > 30:
                d[0] *= -1
                p1Cool = 0
                turns += 1
                maxAngle += 0.1
            
            #slightly change dy to prevent stall
            d[1] += random.randint(-10,10)/10

            #change dy depending on which way player 1 was moving
            if pressed_keys[K_s] and d[1] >-maxAngle:
                d[1] += 2
                #curve 
                if curve == True and pressed_keys[K_c]:
                    ddy += -0.2
            if pressed_keys[K_w] and d[1] <maxAngle:
                d[1] -= 2
                if curve == True and pressed_keys[K_c]:
                    ddy += 0.2

        #checks for cooldown and reflect if player 2 hits the ball
        if pygame.sprite.spritecollideany(P2, balls):
            if p2Cool > 30:
                d[0] *= -1
                p2Cool = 0
                turns += 1
                maxAngle += 0.1
            #slightly change dy to prevent stall
            d[1] += random.randint(-10,10)/10

            #change dy depending on which way player 1 was moving
            if pressed_keys[K_k] and d[1] >-maxAngle:
                d[1] += 2
                if curve == True and singlePlayer == False and pressed_keys[K_n]:
                    ddy = -0.2
            
            if pressed_keys[K_i] and d[1] < maxAngle:
                d[1] -= 2
                if curve == True and singlePlayer == False and pressed_keys[K_n]:
                    ddy += 0.2
            if singlePlayer == True and randomCurve == True and curve == True:
                if random.randint(1,2) == 1:
                    ddy += 0.2
                    
                else:
                    ddy = -0.2
                    

        #curve system
        if curve == True:
            d[1] += ddy
        if output[6] and curve == True:
            if ddy < 0:
                ddy += 0.15
            else:
                ddy -= 0.15

        #prevent ball going too fast or steep
        if d[1] > maxAngle:
            d[1] = maxAngle
        elif d[1] < -maxAngle:
            d[1] = -maxAngle

        #control speed based on dy
        if d[0] < 0:
            if -1 - maxAngle + abs(d[1]) < -maxAngle-1:
                d[0] = -maxAngle - 1 + abs(d[1])
            else:
                d[0] = -maxAngle + 1
        else:
            if 8 - abs(d[1]) > maxAngle + 1:
                d[0] = maxAngle + 1 - abs(d[1])
            else:
                d[0] = maxAngle - 1



        

        #render scores
        score1 = font.render(str(p1), True, WHITE)
        score2 = font.render(str(p2), True, WHITE)
        DISPLAYSURF.blit(score1, (250,50))
        DISPLAYSURF.blit(score2, (SCREEN_WIDTH - 300,50))
        if pausebutton.draw(DISPLAYSURF) or pressed_keys[K_ESCAPE]:
            scene = 'pause'
    pygame.display.update()
    FramePerSec.tick(FPS)



