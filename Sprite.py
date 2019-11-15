#Sprite File for Jumpy
import pygame as pg
from Settings import *
vec = pg.math.Vector2
import random 



class Player(pg.sprite.Sprite):
    def __init__(self,game,right,left, spawnX,PlayerTwo):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        if PlayerTwo:
            self.image = pg.image.load("standing - Copy.png")
        else:
            self.image = pg.image.load("standing.png")
        self.rect = self.image.get_rect()
        self.rect.center = (spawnX, HEIGHT/2)
        self.pos = vec(spawnX, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.offset = vec(10,0)
        self.left = False
        self.right = False
        self.walkCount = 0
        self.score = 0
        self.health = 5
        self.sheild = 0
        self.LazerCount = 3
        self.healthUp = False
        self.KillCount = 0
        self.rightkey = right
        self.leftkey = left
        self.spriteTwo= PlayerTwo
        #self.hitbox= (self.pos.x-15,self.pos.y+40,30,50)

    def jump(self):
        #Jump Only if standing on a platform
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self,self.game.platforms, False)
        if hits:
            self.vel.y = -16

##    def fallback(self):
##        self.rect.x -= 1
##        hits = pg.sprite.spritecollide(self,self.game.platforms, False)
##        if hits:
##            self.vel.y = GRAVITY


    def update(self):
        self.acc = vec(0,GRAVITY)
        #self.hitbox= (self.pos.x-15,self.pos.y-50,30,50)
        #self.hitbox = self.pos
        #self.hitbox.center = self.pos + self.offset
        keys = pg.key.get_pressed()
        if keys[self.leftkey]:
            self.acc.x = -PLAYER_ACC
            self.left = True
            self.right = False
            if self.spriteTwo == False:
                if self.left:
                    self.image = (self.game.walkLeft[self.walkCount//3])
                    self.walkCount = self.walkCount + 1
                    if self.walkCount + 1 >= 27 :
                        self.walkCount = 0
            else:
                if self.left:
                    self.image = (self.game.walkLeft2[self.walkCount//3])
                    self.walkCount = self.walkCount + 1
                    if self.walkCount + 1 >= 27 :
                        self.walkCount = 0
                        
        if keys[self.rightkey]:
            self.acc.x = PLAYER_ACC
            self.left = False 
            self.right = True
            if self.spriteTwo == False:
                if self.right:
                    self.image = (self.game.walkRight[self.walkCount//3])
                    self.walkCount = self.walkCount + 1  
                    if self.walkCount + 1 >= 27 :
                        self.walkCount = 0
            else:
                if self.right:
                    self.image = (self.game.walkRight2[self.walkCount//3])
                    self.walkCount = self.walkCount + 1  
                    if self.walkCount + 1 >= 27 :
                        self.walkCount = 0
        #self.hitbox.x,self.hitbox.y=self.pos.x,self.pos.y


        #Applies frictiom
        self.acc.x += self.vel.x * PLAYER_FRICTION
        #Equations of Motiion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        #Stops at the edges of the screen
        if self.pos.x >= WIDTH - 15 :
            self.pos.x = WIDTH - 15
        if self.pos.x <= 15:
            self.pos.x = 15

        self.rect.midbottom = self.pos


##    def shoot(self,facing):
##        bullet = Projectile(self.rect.centerx,self.rect.top,facing)
##        all_sprites.add(bullet)
##        bullets.add(bullet)

class Platform(pg.sprite.Sprite):
    def __init__(self,x,y,w,h,game,PlatformVal):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((w, h))
        if PlatformVal == 1:
            image = self.game.P01Graphics
        elif PlatformVal == 2:
            image = self.game.midPlatformGraphics
        elif PlatformVal == 3:
            image = self.game.P34Graphics
        else:
            image = self.game.topMidPlatformGraphics
            
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Mob(pg.sprite.Sprite):
    def __init__(self,game,direction):
        pg.sprite.Sprite.__init__(self)
        self.walkRight = [pg.image.load('R1E.png'), pg.image.load('R2E.png'),
             pg.image.load('R3E.png'), pg.image.load('R4E.png'),
             pg.image.load('R5E.png'), pg.image.load('R6E.png'),
             pg.image.load('R7E.png'), pg.image.load('R8E.png'),
             pg.image.load('R9E.png')]


        self.walkLeft = [pg.image.load('L1E.png'), pg.image.load('L2E.png'),
            pg.image.load('L3E.png'), pg.image.load('L4E.png'),
            pg.image.load('L5E.png'), pg.image.load('L6E.png'),
            pg.image.load('L7E.png'), pg.image.load('L8E.png'),
            pg.image.load('L9E.png')]
        
        self.game = game
        self.image = pg.image.load("R1E.png")
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2,0)
        self.pos = vec(WIDTH/2,0)
        self.vel = vec(0,0)
        self.direction = direction
        self.acc = vec(self.direction,0)
        self.left = False
        self.right = False
        self.walkCount = 0
        self.health = 3

    def update(self):
        
        self.hitbox = (self.pos.x-20,self.pos.y-40,20,40)
        if self.direction < 0:
            self.left = True
            self.right = False
        else:
            self.right = True
            self.left = False

        if self.left:
                self.image = (self.walkLeft[self.walkCount//3])
                self.walkCount = self.walkCount + 1
                if self.walkCount + 1 >= 27 :
                    self.walkCount = 0

        if self.right:
                self.image = (self.walkRight[self.walkCount//3])
                self.walkCount = self.walkCount + 1  
                if self.walkCount + 1 >= 27 :
                    self.walkCount = 0
        if self.game.ball == False:
            self.acc = vec(self.direction,GRAVITY)
            #Applies frictiom
            self.acc += self.vel * MOB_FRICTION
            #Equations of Motiion
            self.vel += self.acc
            self.pos += self.vel + 0.5 * self.acc
            #cant pass the sides of the screen
            if self.pos.x >= WIDTH - 10 :
                self.pos.x = WIDTH - 10
                self.direction = self.direction * -1
                self.acc.x = self.acc.x *-1
                self.vel.x = self.vel.x *-1
            if self.pos.x <= 10:
                self.pos.x = 10
                self.direction = self.direction * -1
                self.acc.x = self.acc.x *-1
                self.vel.x = self.vel.x *-1
            if self.pos.y >= HEIGHT + 20:
                self.pos.y = 0

        #Platform and Mob Collision

        if self.game.ball == False:
            if self.pos.y >= 105 and self.pos.y <= 115 and self.pos.x >= WIDTH/2 - 150 and self.pos.x <= WIDTH/2 + 150:
                onPlatform=True
                if onPlatform:
                    self.pos.y = 110
                    self.vel = vec(0,0)
                    onPlatform=False

            if self.pos.y >= 200 and self.pos.y <= 210 and self.pos.x >= WIDTH - 100:
                onPlatform=True
                if onPlatform:
                    self.pos.y = 205
                    self.vel = vec(0,0)
                    onPlatform=False

            if self.pos.y >= 200 and self.pos.y <= 210 and self.pos.x >= 0 and self.pos.x <= 100:
                onPlatform=True
                if onPlatform:
                    self.pos.y = 205
                    self.vel = vec(0,0)
                    onPlatform=False

            if self.pos.y >= 335 and self.pos.y <= 345 and self.pos.x >= WIDTH/2 - 200 and self.pos.x <= WIDTH/2 + 200:
                onPlatform=True
                if onPlatform:
                    self.pos.y = 340
                    self.vel = vec(0,0)
                    onPlatform=False

            if self.pos.y >= HEIGHT - 10 and self.pos.y <= HEIGHT and self.pos.x >= 0 and self.pos.x <= 250:
                onPlatform=True
                if onPlatform:
                    self.pos.y = HEIGHT - 10
                    self.vel = vec(0,0)
                    onPlatform=False

            if self.pos.y >= HEIGHT - 10 and self.pos.y <= HEIGHT and self.pos.x >= WIDTH-250 and self.pos.x <= WIDTH:
                onPlatform=True
                if onPlatform:
                    self.pos.y = HEIGHT - 10
                    self.vel = vec(0,0)
                    onPlatform=False
        else:
            if self.pos.y<self.game.Blackholey - 5:
                self.pos.y += 1
            #change y down -
            if self.pos.y>self.game.Blackholey - 5 :
                self.pos.y -= 1
            if self.pos.x>self.game.Blackholex:
                #change x left -
                self.pos.x -= 1
            if self.pos.x<self.game.Blackholex:
                #change x right +
                self.pos.x += 1
        
            if self.pos == (self.game.Blackholex,self.game.Blackholey):
                self.kill()
                
            

        self.rect.midbottom = self.pos

class Projectile(pg.sprite.Sprite):
    def __init__(self,x,y,facing,colour):
        pg.sprite.Sprite. __init__(self)
        self.image = pg.Surface((20,10))
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x 
        self.facing = facing
        self.speedx = 8 * facing
        


    def update(self):
        self.rect.x += self.speedx
        #Delete if off the screen
        if self.rect.centerx > WIDTH or self.rect.centerx < 0:
            self.kill()

#"heal","sheild","Lazer","Ghost","Blackhole"
class pUP(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.type= random.choice(["Lazer","Ghost","Blackhole"])
        self.image = pg.Surface((10,10))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.pos = vec(random.choice([50,100,150,200,300,350,400,450,500,550]),random.choice([20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440]))
        self.rect.center = self.pos 
        self.vel = vec(0,GRAVITY+1)

    def update(self):
        self.pos.y += self.vel.y
        self.rect.center = self.pos

        if self.pos.y >= 105 and self.pos.y <= 115 and self.pos.x >= WIDTH/2 - 150 and self.pos.x <= WIDTH/2 + 150:
            onPlatform=True
            if onPlatform:
                self.pos.y = 110 - 10
                self.vel = vec(0,0)
                onPlatform=False

        elif self.pos.y >= 200 and self.pos.y <= 210 and self.pos.x >= WIDTH - 100:
            onPlatform=True
            if onPlatform:
                self.pos.y = 205 - 10
                self.vel = vec(0,0)
                onPlatform=False

        elif self.pos.y >= 200 and self.pos.y <= 210 and self.pos.x >= 0 and self.pos.x <= 100:
            onPlatform=True
            if onPlatform:
                self.pos.y = 205 - 10
                self.vel = vec(0,0)
                onPlatform=False

        elif self.pos.y >= 335 and self.pos.y <= 345 and self.pos.x >= WIDTH/2 - 200 and self.pos.x <= WIDTH/2 + 200:
            onPlatform=True
            if onPlatform:
                self.pos.y = 340 - 10 
                self.vel = vec(0,0)
                onPlatform=False

        elif self.pos.y >= HEIGHT - 10 and self.pos.y <= HEIGHT and self.pos.x >= 0 and self.pos.x <= 250:
            onPlatform=True
            if onPlatform:
                self.pos.y = HEIGHT - 15
                self.vel = vec(0,0)
                onPlatform=False

        elif self.pos.y >= HEIGHT - 10 and self.pos.y <= HEIGHT and self.pos.x >= WIDTH-250 and self.pos.x <= WIDTH:
            onPlatform=True
            if onPlatform:
                self.pos.y = HEIGHT - 15
                self.vel = vec(0,0)
                onPlatform=False
        
class GhostMobs(pg.sprite.Sprite):
    def __init__(self,game, huntTwo):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.image.load("GR.png")
        self.rect = self.image.get_rect()
        self.pos = vec(WIDTH/2,0)
        self.rect.center = self.pos
        self.left = False
        self.right = False
        self.walkCount = 0
        self.health = 2
        self.huntTwo = huntTwo

        
    def update(self):
        if self.game.twoPlayers:        
            if self.game.playerTwo.health < 0:
                    self.huntTwo = False
            if self.game.player.health < 0:
                    self.huntTwo = True
                
        if self.huntTwo == False:
            if self.pos.y<self.game.player.pos.y:
                self.pos.y += 2
                #change y down -
            if self.pos.y>self.game.player.pos.y:
                self.pos.y -= 2
            if self.pos.x>self.game.player.pos.x:
                #change x left -
                self.pos.x -= 2
                self.left = True
                self.right = False
            if self.pos.x<self.game.player.pos.x:
                #change x right +
                self.pos.x += 2
                self.right = True
                self.left = False
        else:
            if self.pos.y<self.game.playerTwo.pos.y:
                self.pos.y += 2
                #change y down -
            if self.pos.y>self.game.playerTwo.pos.y:
                self.pos.y -= 2
            if self.pos.x>self.game.playerTwo.pos.x:
                #change x left -
                self.pos.x -= 2
                self.left = True
                self.right = False
            if self.pos.x<self.game.playerTwo.pos.x:
                #change x right +
                self.pos.x += 2
                self.right = True
                self.left = False
            
        if self.right:
            self.image = pg.image.load("GR.png")
        if self.left:
            self.image = pg.image.load("GL.png")
        #cant pass the sides of the screen
        if self.pos.x >= WIDTH - 10 :
            self.pos.x = WIDTH - 10
            self.direction = self.direction * -1
            self.acc.x = self.acc.x *-1
            self.vel.x = self.vel.x *-1
        if self.pos.x <= 10:
            self.pos.x = 10
            self.direction = self.direction * -1
            self.acc.x = self.acc.x *-1
            self.vel.x = self.vel.x *-1
        if self.pos.y >= HEIGHT + 20:
            self.pos.y = 0

        self.rect.midbottom = self.pos
        #self.follow()
class blackHole(pg.sprite.Sprite):
     def __init__(self,game,x,y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.x = int(x)
        self.y = int(y)
        #pg.draw.circle(self.game.screen, WHITE , (self.x,self.y), 40)
        self.image = pg.draw.circle(self.game.screen, WHITE , (self.x,self.y), 40)
     def update(self):
         pg.draw.circle(self.game.screen, WHITE , (self.x,self.y), 40)
        
