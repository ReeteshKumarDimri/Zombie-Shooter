import pygame
from pygame import mixer
import random
pygame.init()

screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width,screen_height))
icon = pygame.image.load("zombie.png")
background = pygame.image.load("bg.png")
background = pygame.transform.scale(background,(800,600))
mixer.music.load("Sneaky Snitch.mp3")
mixer.music.play()
#Title and icon
pygame.display.set_caption("Zombie Shooter")
pygame.display.set_icon(icon)

#Player
PlayerX = 400
PlayerY = 400
Velocity = 0.4
PlayerVelocity = 0
PlayerIdle = pygame.image.load("player-idle.png")
Idle = 1
#Bullet 
bullet = pygame.image.load("bullet.png")
bulletX = PlayerX
bulletY = PlayerY
bulletVelocity = 1.5
bulletDir = 1

#Gun Sprites
GunIdle = pygame.image.load("gun-idle1.png")
GunWalk = []
for i in range(0,5):
    GunWalk.append(pygame.image.load("gun-walk%s.png"%str(i+1)))
Shot = False
#Player Walking Sprites
PlayerWalk = []
for i in range(0,5):
    PlayerWalk.append(pygame.image.load("player-walk%s.png"%str(i+1)))
PlayerLeft = False 
PlayerRight = False
WalkCount = 0




#Enemy

EnemyX = [5,788,788,20]
EnemyY = 400
EnemyVelocity = 0.3
EWalk = []
EnemyWalk = []
for i in range(0,9):
    img = pygame.image.load("Walk (%s).png"%str(i+1))
    img = pygame.transform.scale(img,(90,90))
    EWalk.append(img)
for j in range(0,4):
    EnemyWalk.append(EWalk)

EnemyWalkCount = 0
EnemyDeath = [False,False,False,False]
EnemySpawnPosition = [0,1,1,0]

#Enemy Animation
def Enemy_Animation(i):
    global EnemyDeath
    global EnemyX
    global EnemyY
    global EnemyWalkCount
    global EnemySpawnPosition
        
    if EnemyDeath[i]:
        EnemySpawnPosition[i] = random.randrange(0,2,1)
        if EnemySpawnPosition[i] == 0:
           EnemyX[i] = 10
        else :
            EnemyX[i] = 790
        EnemyDeath[i] = False        

    if  (EnemyWalkCount) > 9:
        EnemyWalkCount = 0
    


    
    if EnemySpawnPosition[i] == 0:
        screen.blit(EnemyWalk[i][int(EnemyWalkCount)],(EnemyX[i],EnemyY))
        EnemyWalkCount+=0.04
    else:
        screen.blit(pygame.transform.flip(EnemyWalk[i][int(EnemyWalkCount)],True,False),(EnemyX[i],EnemyY))
        EnemyWalkCount+=0.04


#Score
ScoreValue = 0
ScoreFont = pygame.font.Font("freesansbold.ttf",32)
def ShowScore():
    score = ScoreFont.render("Score : "+str(ScoreValue),True,(255,255,255))
    screen.blit(score,(10,10))


#GameOver
OverFont = pygame.font.Font("freesansbold.ttf",50)
def GameOver():
    over =OverFont.render("GAME OVER",True,(255,0,0))
    score = ScoreFont.render("Final Score : "+str(ScoreValue),True,(255,255,255))
    screen.blit(over,(250,200))
    screen.blit(score,(290,260))
isOver = False

#Bullet physics
def bullet_fire(x,y):
    global Shot
    Shot = True
    screen.blit(bullet,(x,y))



    
#Player Animation

def Player_Animation():
    global WalkCount
    
    if WalkCount >4:
        WalkCount = 0

    if PlayerRight:
        screen.blit(PlayerWalk[int(WalkCount)],(PlayerX,PlayerY))
        screen.blit(GunWalk[int(WalkCount)],(PlayerX,PlayerY))
        WalkCount+=0.05
    
    elif PlayerLeft:
        screen.blit(pygame.transform.flip(PlayerWalk[int(WalkCount)],True,False),(PlayerX,PlayerY))
        screen.blit(pygame.transform.flip(GunWalk[int(WalkCount)],True,False),(PlayerX,PlayerY))
        WalkCount+=0.05

    else:
        if Idle == 1:
            screen.blit(PlayerIdle,(PlayerX,PlayerY))
            screen.blit(GunIdle,(PlayerX,PlayerY))
        else:
            screen.blit(pygame.transform.flip(PlayerIdle,True,False),(PlayerX,PlayerY))
            screen.blit(pygame.transform.flip(GunIdle,True,False),(PlayerX,PlayerY))

#The Window
def Draw():
    global bulletX
    global bulletY
    global Shot

    if Shot == True:
        bullet_fire(bulletX,bulletY)
        bulletX += bulletVelocity*bulletDir
    if not isOver: 
        ShowScore()
    else:
        GameOver()
    for i in range(0,4):
        Enemy_Animation(i)
    Player_Animation()

    pygame.display.update()



EnemyRect = []
for j in range(0,4):
    EnemyRect.append(pygame.Rect((EnemyX[j],EnemyY),(80,70)))
#GAME LOOP
running = True
while running:
    
    screen.fill((0,0,0))
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                PlayerVelocity = -Velocity
                PlayerLeft = True
                PlayerRight = False

            if event.key == pygame.K_RIGHT:
                PlayerVelocity = Velocity
                PlayerRight = True
                PlayerLeft = False
            if event.key == pygame.K_SPACE:
                if Shot == False:
                    if PlayerRight:
                        bulletDir = 1
                    elif PlayerLeft:
                        bulletDir = -1
                    elif Idle == -1:
                        bulletDir = -1
                    else: 
                        bulletDir = 1
                    bulletX = PlayerX + 50
                    bulletY = PlayerY + 60
                    bulletsound = mixer.Sound("shotgun-firing-4-6746.wav")
                    bulletsound.play()
                    bulletsound = mixer.Sound("rifle-or-shotgun-reload-6787.wav")
                    bulletsound.play()
                    bullet_fire(bulletX,bulletY)
            if isOver and event.key == pygame.K_RETURN:
                EnemyX = [5,10,15,20]
                EnemyVelocity = 0.3
                isOver = False
                ScoreValue = 0


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                PlayerVelocity = 0
                PlayerLeft = False
                PlayerRight = False
                EnemyWalkCount = 0
                WalkCount = 0
                if event.key == pygame.K_LEFT:
                    Idle = -1
                else:
                    Idle = 1



    bulletRect = pygame.Rect((bulletX,bulletY),(14,8))
    PlayerRect = pygame.Rect((PlayerX+20,PlayerY),(30,50))
    for i in range(0,4):
        EnemyRect[i].x = EnemyX[i]

    if(bulletX<=0 or bulletX>=788):
        bulletX = PlayerX
        Shot = False

    PlayerX+=PlayerVelocity
    for i in range(0,4):
        if EnemyX[i]<=0 or EnemyX[i]>=800:
            EnemyDeath[i] = True
            continue
        if EnemySpawnPosition[i]==0:
            EnemyX[i]+=EnemyVelocity
        else:
            EnemyX[i]-=EnemyVelocity
        if pygame.Rect.colliderect(bulletRect,EnemyRect[i]):
            EnemyDeath[i] = True
            Shot = False
            bulletX = PlayerX
            if not isOver:
                ScoreValue+=1
        if pygame.Rect.colliderect(EnemyRect[i],PlayerRect):
            EnemyVelocity = 0
            isOver = True
        

    if(PlayerX<=0):
        PlayerX = 0
    elif(PlayerX>=730):
        PlayerX = 730
    Draw()

