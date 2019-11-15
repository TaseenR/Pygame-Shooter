import pygame as pg
import random
from Settings import *
from Sprite import *
import time
from os import path

mobList =["mob1","mob2","mob3"]            
bullets = []


class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        #pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        #self.timer.get_fps(60)
        icon = pg.image.load("Icon.png")
        pg.display.set_icon(icon)
        self.running = True
        self.twoPlayers = False
        self.Icounter=0
        self.Mcounter=0
        self.Fcounter=0
        self.font_name = pg.font.match_font(FONT_NAME)
        self.Lazerbeam = False
        self.LazerbeamText =  False
        self.LazerCount = 3
        self.healthUp = False
        self.ghostSpawn = False
        self.ghostText = False
        self.blackText = False
        self.pUpCount = 0
        self.itemCount = 0
        self.holeCount = 0
        self.bHoleAmmo = 0
        self.bHAText = False
        self.sheildText = False
        self.ball = False
        self.alivePlayers = 2
        
    def load_data(self):
        # load high score
        self.walkRight = [pg.image.load('R1.png'), pg.image.load('R2.png'),
             pg.image.load('R3.png'), pg.image.load('R4.png'),
             pg.image.load('R5.png'), pg.image.load('R6.png'),
             pg.image.load('R7.png'), pg.image.load('R8.png'),
             pg.image.load('R9.png')]


        self.walkLeft = [pg.image.load('L1.png'), pg.image.load('L2.png'),
            pg.image.load('L3.png'), pg.image.load('L4.png'),
            pg.image.load('L5.png'), pg.image.load('L6.png'),
            pg.image.load('L7.png'), pg.image.load('L8.png'),
            pg.image.load('L9.png')]

        self.walkRight2 = [pg.image.load('R1 - Copy.png'), pg.image.load('R2 - Copy.png'),
             pg.image.load('R3 - Copy.png'), pg.image.load('R4 - Copy.png'),
             pg.image.load('R5 - Copy.png'), pg.image.load('R6 - Copy.png'),
             pg.image.load('R7 - Copy.png'), pg.image.load('R8 - Copy.png'),
             pg.image.load('R9 - Copy.png')]


        self.walkLeft2 = [pg.image.load('L1 - Copy.png'), pg.image.load('L2 - Copy.png'),
            pg.image.load('L3 - Copy.png'), pg.image.load('L4 - Copy.png'),
            pg.image.load('L5 - Copy.png'), pg.image.load('L6 - Copy.png'),
            pg.image.load('L7 - Copy.png'), pg.image.load('L8 - Copy.png'),
            pg.image.load('L9 - Copy.png')]
        
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, HS_FILE), 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

        #sound effects
        self.pUpSound = pg.mixer.Sound("Powerup.wav")
        self.pUpSoundG = pg.mixer.Sound("Powerup Ghost.wav")
        self.jumpSound = pg.mixer.Sound("Jump.wav")
        self.bulletSound = pg.mixer.Sound("Bullet.wav")
        self.lazerSound = pg.mixer.Sound("laser_shoot.wav")
        self.blackholeSound = pg.mixer.Sound("Blackhole.wav")
        self.collideSound = pg.mixer.Sound("Hit_Hurt.wav")
        self.DropPupSound = pg.mixer.Sound("DropPup.wav")
        self.ghostBGSound = pg.mixer.Sound("BossMain.wav")
        self.deathPitSound = pg.mixer.Sound("Death Pit.wav")
        self.mobDeathSound = pg.mixer.Sound("Mob Death.wav")
        self.playerDeathSound = pg.mixer.Sound("Player Death.wav")
        #Platform graphis
        self.platformGraphics = pg.image.load("blocks.png")
        self.P01Graphics = pg.image.load("P01.png")
        self.midPlatformGraphics = pg.image.load("MidPlatform.png")
        self.P34Graphics = pg.image.load("P34.png")
        self.topMidPlatformGraphics = pg.image.load("MidPlatform2.png")
        
    def new(self):
        # start a new game
        pg.mixer.music.load("Map.wav")
        pg.mixer.music.play(loops = -1)
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.lazershots = pg.sprite.Group()
        self.ghosts = pg.sprite.Group()
        self.blackholes = pg.sprite.Group()
        if self.twoPlayers == True:
            self.player = Player(self,pg.K_RIGHT,pg.K_LEFT, WIDTH/2 + 50,False)
            self.all_sprites.add(self.player)
            self.playerTwo = Player(self,pg.K_d,pg.K_a, WIDTH/2 - 50,True)
            self.all_sprites.add(self.playerTwo)
        else:
            self.player = Player(self,pg.K_RIGHT,pg.K_LEFT, WIDTH/2,False)
            self.all_sprites.add(self.player)
        p0 = Platform(0, HEIGHT - 10,250, 10,self,1)
        self.all_sprites.add(p0)
        self.platforms.add(p0)
        p1 = Platform(WIDTH-250, HEIGHT - 10,250, 10,self,1)
        self.all_sprites.add(p1)
        self.platforms.add(p1)
        p2 = Platform(WIDTH/2 - 200, 335,400,20,self,2)#D
        self.all_sprites.add(p2)
        self.platforms.add(p2)
        p3 = Platform(0, 200,100,20,self,3)#d
        self.all_sprites.add(p3)
        self.platforms.add(p3)
        p4 = Platform(WIDTH-100,200,100,20,self,3)#d
        self.all_sprites.add(p4)
        self.platforms.add(p4)
        p5 = Platform(WIDTH/2 - 150, 105,300,20,self,0)#d
        self.all_sprites.add(p5)
        self.platforms.add(p5)
        #for m in range(3):
##        for i in (mobList):
##            i = Mob(self,random.choice([-1,1]))
##            self.all_sprites.add(i)
##            self.mobs.add(i)
        for i in range(3):
            self.m = Mob(self,random.choice([-1,-0.5,1,0.5]))
            self.all_sprites.add(self.m)
            self.mobs.add(self.m)
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        

    def update(self):
        # Game Loop - Update
        self.timer = int(time.time() - startTime)
        self.Icounter +=1
        self.Mcounter +=1
        self.Fcounter += 1
        items = ["Item"]
        self.trackx = self.player.pos.x
        self.tracky = self.player.pos.y
        #print(self.trackx , self.tracky)
        self.pUpCount += 1
        self.holeCount += 1
        self.all_sprites.update()

        #check if player hits platform - only if player is falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player,self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
        else:# self.player.vel.y < 0 :
            hits = pg.sprite.spritecollide(self.player,self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.bottom
                self.player.vel.y = 0
        #Player two
        if self.twoPlayers == True:
            if self.playerTwo.vel.y > 0:
                hits = pg.sprite.spritecollide(self.playerTwo,self.platforms, False)
                if hits:
                    self.playerTwo.pos.y = hits[0].rect.top
                    self.playerTwo.vel.y = 0
            else:# self.player.vel.y < 0 :
                hits = pg.sprite.spritecollide(self.playerTwo,self.platforms, False)
                if hits:
                    self.playerTwo.pos.y = hits[0].rect.bottom
                    self.playerTwo.vel.y = 0

        if self.twoPlayers == True:
            if self.player.pos.y >= HEIGHT + 40:
                self.player.kill()
                self.alivePlayers -=1
                self.deathPitSound.play()
            if self.playerTwo == True:
                if self.playerTwo.pos.y >= HEIGHT + 40:
                    self.playerTwo.kill()
                    self.alivePlayers -=1
                    self.deathPitSound.play()
        else:
            if self.player.pos.y >= HEIGHT + 40:
                self.deathPitSound.play()
                self.running = False
                self.playing = False
            
##            for sprite in self.all_sprites:
##                sprite.rect.y -= self.player.vel.y
##                sprite.kill()
                
        if self.Mcounter >=900:
            for i in range(3):
                    self.m = Mob(self,random.choice([-1,-0.5,1,0.5]))
                    self.all_sprites.add(self.m)
                    self.mobs.add(self.m)
                    self.Mcounter= 0



        #Mob collision with Bullets
        #This checks to see if the lazerbeam powerup is active
            #Bullets and ordinary Mobs 
        if self.m.health == 1:#checks the mobs health 
            mobHits = pg.sprite.groupcollide(self.mobs,self.bullets, True, True)
            if mobHits:#checks for collisions between mobs after checkin mob health
                self.player.score = self.player.score + 10
                self.player.KillCount += 1
                self.mobDeathSound.play()
                for i in range(1):
                    self.m = Mob(self,random.choice([-0.7,-1,1,0.7]))
                    self.all_sprites.add(self.m)
                    self.mobs.add(self.m)
                    self.collideSound.play()
        else:#Collision between the mob and bullet at >1 health 
            mobHits = pg.sprite.groupcollide(self.mobs,self.bullets, False, True)
            if mobHits:
                self.m.health -= 1 
                self.player.score = self.player.score + 1
                self.collideSound.play()
        #Ghost Mobs and bullets
        if self.ghostSpawn == True:
            self.ghostBGSound.play()
            if self.ghost.health == 1:#Ghost kill conditon
                GmobHits = pg.sprite.groupcollide(self.ghosts,self.bullets, True, True)
                if GmobHits:
                        self.player.score += 20
                        self.player.KillCount += 1
                        self.collideSound.play()
            else:#ghost shoot condition
                GmobHits = pg.sprite.groupcollide(self.ghosts,self.bullets, False, True)
                if GmobHits:
                        self.ghost.health -= 1 
                        self.player.score = self.player.score + 3
                        self.collideSound.play()
                
        if self.LazerCount >= 0 :#I have placed this after bullet colision as it wont be active constantly through out the game
            mobHits = pg.sprite.groupcollide(self.mobs,self.lazershots, True, False)
            if mobHits:
                self.player.score = self.player.score + 5
                self.player.KillCount += 1
                self.mobDeathSound.play()
                for i in range(1):
                    self.m = Mob(self,random.choice([-1,-0.5,1,0.5]))
                    self.all_sprites.add(self.m)
                    self.mobs.add(self.m)
            if self.ghostSpawn == True: #only if ghost spawn is active will ghost collisions be neccsary
                self.ghostBGSound.play()
                GmobHits = pg.sprite.groupcollide(self.ghosts,self.lazershots, True, False)
                if GmobHits:
                    self.player.score += 10
                    self.player.KillCount += 1
                    
        #MPHits = pg.sprite.groupcollide(self.mobs,self.platforms, False, False, )
        #if MPHits:
            #print (MPHits(0,0))
            #self.mobs.pos.y = MPHits[0][0].rect.top
           # self.mobs.vel.y = 0
           # self.mobs.acc.y = 0




        #Player collisions with the mob, e.g death or decrease in life.
        if self.twoPlayers == False:
            if self.player.sheild == 0 and self.player.health == 0:
                hits = pg.sprite.spritecollide(self.player,self.mobs, True)
                Ghits = pg.sprite.spritecollide(self.player,self.ghosts, True)
                if self.twoPlayers == False:
                    if hits or Ghits:
                        self.running = False
                        self.playing = False
                        self.playerDeathSound.play()
            elif self.player.sheild >= 1:#If the player has sheild it takes away from sheild instead
                    hits = pg.sprite.spritecollide(self.player,self.mobs, True)
                    Ghits = pg.sprite.spritecollide(self.player,self.ghosts, True)
                    if hits or Ghits:
                        self.m = Mob(self,random.choice([-0.7,-1,1,0.7]))
                        self.all_sprites.add(self.m)
                        self.mobs.add(self.m)
                        self.player.sheild -= 1
                        self.collideSound.play()
            else:
                    hits = pg.sprite.spritecollide(self.player,self.mobs, True)
                    Ghits = pg.sprite.spritecollide(self.player,self.ghosts, True)
                    if hits or Ghits:
                        self.m = Mob(self,random.choice([-0.7,-1,1,0.7]))
                        self.all_sprites.add(self.m)
                        self.mobs.add(self.m)
                        self.player.health -= 1
                        self.collideSound.play()
                    
        if self.twoPlayers == True:
            if self.player.sheild == 0 and self.player.health == 0:
                hits = pg.sprite.spritecollide(self.player,self.mobs, True)
                Ghits = pg.sprite.spritecollide(self.player,self.ghosts, True)
                if hits or Ghits:
                    self.player.health -= 1
                    self.player.kill()
                    self.playerDeathSound.play()
                    self.alivePlayers -= 1
                    self.collideSound.play()
                    
            if self.playerTwo.sheild == 0 and self.playerTwo.health == 0:
                hitsTwo = pg.sprite.spritecollide(self.playerTwo,self.mobs, True)
                GhitsTwo = pg.sprite.spritecollide(self.playerTwo,self.ghosts, True)
                if hitsTwo or GhitsTwo:
                    self.playerTwo.health -= 1
                    self.playerTwo.kill()
                    self.playerDeathSound.play()
                    self.alivePlayers -= 1
                    self.collideSound.play()
                    
            if self.playerTwo.sheild >= 1:#If the player has sheild it takes away from sheild instead
                hitsTwo = pg.sprite.spritecollide(self.playerTwo,self.mobs, True)
                GhitsTwo = pg.sprite.spritecollide(self.playerTwo,self.ghosts, True)
                if hitsTwo or GhitsTwo:
                    self.m = Mob(self,random.choice([-0.7,-1,1,0.7]))
                    self.all_sprites.add(self.m)
                    self.mobs.add(self.m)
                    self.playerTwo.sheild -= 1
                    self.collideSound.play()

            if self.player.sheild >= 1:#If the player has sheild it takes away from sheild instead
                hits = pg.sprite.spritecollide(self.player,self.mobs, True)
                Ghits = pg.sprite.spritecollide(self.player,self.ghosts, True)
                if hits or Ghits:
                    self.m = Mob(self,random.choice([-0.7,-1,1,0.7]))
                    self.all_sprites.add(self.m)
                    self.mobs.add(self.m)
                    self.player.sheild -= 1
                    self.collideSound.play()
                    
            if self.player.health >= 1:
                hits = pg.sprite.spritecollide(self.player,self.mobs, True)
                Ghits = pg.sprite.spritecollide(self.player,self.ghosts, True)
                if hits or Ghits:
                    self.m = Mob(self,random.choice([-0.7,-1,1,0.7]))
                    self.all_sprites.add(self.m)
                    self.mobs.add(self.m)
                    self.player.health -= 1
                    self.collideSound.play()
                    
            if self.playerTwo.health >= 1:
                hitsTwo = pg.sprite.spritecollide(self.playerTwo,self.mobs, True)
                GhitsTwo = pg.sprite.spritecollide(self.playerTwo,self.ghosts, True)
                if hitsTwo or GhitsTwo:
                    self.m = Mob(self,random.choice([-0.7,-1,1,0.7]))
                    self.all_sprites.add(self.m)
                    self.mobs.add(self.m)
                    self.playerTwo.health -= 1
                    self.collideSound.play()

##        hits = pg.sprite.spritecollide(self.player,self.ghosts, True)
##        if hits:
##            self.m = Mob(self,random.choice([-1,1]))
##            self.all_sprites.add(self.m)
##            self.mobs.add(self.m)
##            self.player.health -= 1



        #Spawning in Items per 10 seconds roughly. 
        spawnItem = True
        if self.Icounter >=600 and self.timer > 1 and spawnItem == True:
            self.PUP = pUP()
            self.DropPupSound.play()
            self.all_sprites.add(self.PUP)
            self.items.add(self.PUP)
            self.Icounter = 0
            spawnItem = False
            if self.Fcounter == self.Fcounter + 120:
                self.PUP.kill()
                
            #self.Icounter=0
            #self.player.score += 1



        #If ghost mob exists:
            #ghostmob.pos.x,ghostmob.pos.y=player.pos.x,player.pos.y
        
        #Item/Player Collision and powerups.    
        PIhits = pg.sprite.spritecollide(self.player,self.items, True)
        if PIhits:
            self.player.score += 20
            self.pUpCount = 0
            if self.PUP.type == ("heal"):
                self.healthUp = True
                self.player.health = 5
                self.pUpSound.play()
            elif self.PUP.type == ("sheild"):
                self.sheildText = True
                self.player.sheild = 2
                self.pUpSound.play()
                #self.blitText("Sheild Up")s
            elif self.PUP.type == ("Lazer"):
                self.LazerbeamText = True
                self.Lazerbeam = True
                self.pUpSound.play()
            elif self.PUP.type == ("Ghost"):
                self.ghostSpawn = True
                self.ghostText = True 
                self.ghost= GhostMobs(self,False)
                self.ghosts.add(self.ghost)
                self.all_sprites.add(self.ghost)
                self.pUpSoundG.play()
                #self.blitText("BOO"
            elif self.PUP.type == ("Blackhole"):
                self.bHoleAmmo += 1
                self.blackText = True
                self.bHAText = True
                self.pUpSound.play()
        if self.twoPlayers == True:
            PIhits = pg.sprite.spritecollide(self.playerTwo,self.items, True)
            if PIhits:
                self.player.score += 20
                self.pUpCount = 0
                if self.PUP.type == ("heal"):
                    self.healthUp = True
                    self.pUpSound.play()
                    self.playerTwo.health = 5
                elif self.PUP.type == ("sheild"):
                    self.sheildText = True
                    self.playerTwo.sheild = 2
                    self.pUpSound.play()
                    #self.blitText("Sheild Up")s
                elif self.PUP.type == ("Lazer"):
                    self.LazerbeamText = True
                    self.Lazerbeam = True
                    self.pUpSound.play()
                elif self.PUP.type == ("Ghost"):
                    self.ghostSpawn = True
                    self.ghostText = True
                    self.pUpSoundG.play()
                    self.ghost= GhostMobs(self,True)
                    self.ghosts.add(self.ghost)
                    self.all_sprites.add(self.ghost)
                    #self.blitText("BOO"
                elif self.PUP.type == ("Blackhole"):
                    self.bHoleAmmo += 1
                    self.blackText = True
                    self.bHAText = True
                    self.pUpSound.play()

        if self.alivePlayers <= 0:
            self.running = False
            self.playing = False
            self.twoPlayers = False

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                    self.running = False
            #checks if jump key is pressed
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.player.jump()
                    self.jumpSound.play()
                if self.twoPlayers == True:
                    if event.key == pg.K_w:
                        self.playerTwo.jump()
                        self.jumpSound.play()
            #checks if bullet key is pressed
            if self.twoPlayers == False:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        #if self.Lazerbeam == False:
                       if self.player.left:
                           bullet = Projectile(self.player.rect.centerx,self.player.rect.top+20,-1,WHITE)
                           self.all_sprites.add(bullet)
                           self.bullets.add(bullet)
                           self.bulletSound.play()
                       else:
                            bullet = Projectile(self.player.rect.centerx,self.player.rect.top+20,1,WHITE)
                            self.all_sprites.add(bullet)
                            self.bullets.add(bullet)
                            self.bulletSound.play()
                    if self.Lazerbeam == True:
                        if event.key == pg.K_z:
                            if self.player.left:
                                bullet = Projectile(self.player.rect.centerx,self.player.rect.top+20,-1,RED)
                                self.all_sprites.add(bullet)
                                self.lazershots.add(bullet)
                                self.LazerCount -= 1
                                self.lazerSound.play()
                            else:
                                bullet = Projectile(self.player.rect.centerx,self.player.rect.top+20,1,RED)
                                self.all_sprites.add(bullet)
                                self.lazershots.add(bullet)
                                self.LazerCount -= 1
                                self.lazerSound.play()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_x and self.bHoleAmmo >= 1:
                        self.Blackholex = int(self.player.pos.x)
                        self.Blackholey = int(self.player.pos.y)
                        self.ball = True 
                        self.holeCount = 0
                        self.bHoleAmmo -= 1
                        self.blackholeSound.play()


            else:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_j:
                        #if self.Lazerbeam == False:
                       if self.player.left:
                           bullet = Projectile(self.player.rect.centerx,self.player.rect.top+20,-1,WHITE)
                           self.all_sprites.add(bullet)
                           self.bullets.add(bullet)
                           self.bulletSound.play()
                       else:
                            bullet = Projectile(self.player.rect.centerx,self.player.rect.top+20,1,WHITE)
                            self.all_sprites.add(bullet)
                            self.bullets.add(bullet)
                            self.bulletSound.play()
                    if self.Lazerbeam == True:
                        if event.key == pg.K_k:
                            if self.player.left:
                                bullet = Projectile(self.player.rect.centerx,self.player.rect.top+20,-1,RED)
                                self.all_sprites.add(bullet)
                                self.lazershots.add(bullet)
                                self.LazerCount -= 1
                                self.lazerSound.play()
                            else:
                                bullet = Projectile(self.player.rect.centerx,self.player.rect.top+20,1,RED)
                                self.all_sprites.add(bullet)
                                self.lazershots.add(bullet)
                                self.LazerCount -= 1
                                self.lazerSound.play()
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_l and self.bHoleAmmo >= 1:
                            self.Blackholex = int(self.player.pos.x)
                            self.Blackholey = int(self.player.pos.y)
                            self.ball = True 
                            self.holeCount = 0
                            self.bHoleAmmo -= 1
                            self.blackholeSound.play()

                    if event.key == pg.K_c:
                        #if self.Lazerbeam == False:
                       if self.playerTwo.left:
                           bullet = Projectile(self.playerTwo.rect.centerx,self.playerTwo.rect.top+20,-1,WHITE)
                           self.all_sprites.add(bullet)
                           self.bullets.add(bullet)
                           self.bulletSound.play()
                       else:
                            bullet = Projectile(self.playerTwo.rect.centerx,self.playerTwo.rect.top+20,1,WHITE)
                            self.all_sprites.add(bullet)
                            self.bullets.add(bullet)
                            self.bulletSound.play()
                    if self.Lazerbeam == True:
                        if event.key == pg.K_v:
                            if self.playerTwo.left:
                                bullet = Projectile(self.playerTwo.rect.centerx,self.playerTwo.rect.top+20,-1,RED)
                                self.all_sprites.add(bullet)
                                self.lazershots.add(bullet)
                                self.LazerCount -= 1
                                self.lazerSound.play()
                            else:
                                bullet = Projectile(self.playerTwo.rect.centerx,self.playerTwo.rect.top+20,1,RED)
                                self.all_sprites.add(bullet)
                                self.lazershots.add(bullet)
                                self.LazerCount -= 1
                                self.lazerSound.play()
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_b and self.bHoleAmmo >= 1:
                            self.Blackholex = int(self.playerTwo.pos.x)
                            self.Blackholey = int(self.playerTwo.pos.y)
                            self.ball = True 
                            self.holeCount = 0
                            self.bHoleAmmo -= 1
                            self.blackholeSound.play()

                
                
                       
                
            if self.LazerCount == 0:
                self.Lazerbeam = False
                self.LazerCount = 3

            if self.bHoleAmmo == 0:
                self.bHAText = False
            
                    

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BGCOLOUR)
        self.all_sprites.draw(self.screen)
        self.drawText(str(self.player.score), 32, SILVER, WIDTH/2,0)
        self.drawText(("Kill Count: ")+ str(self.player.KillCount), 16, SILVER, WIDTH * 3/4 ,0)
        self.drawText(str(self.timer), 16, SILVER, WIDTH/2,32)
        if self.player.health >= 0:
            pg.draw.rect(self.screen,BLACK,(20,20,110,20))
            pg.draw.rect(self.screen,RED,(25,24,20 * self.player.health ,13))
            pg.draw.rect(self.screen,AQUA,(20,40,55*self.player.sheild,10))
        if self.twoPlayers:
            if self.playerTwo.health >= 0:
                pg.draw.rect(self.screen,BLACK,(20,60,110,20))
                pg.draw.rect(self.screen,RED,(25,64,20 * self.playerTwo.health ,13))
                pg.draw.rect(self.screen,AQUA,(20,80,55*self.playerTwo.sheild,10))
                self.drawText(("Player Two: "), 12, SILVER, 50,50)
        self.drawText(("Health: "), 16, SILVER, 50,4)
        if self.ball == True:
            self.circle = pg.draw.circle(self.screen, BGCOLOUR , (self.Blackholex,self.Blackholey), 4)
            self.blackhole = pg.image.load("blackhole.png")
            self.screen.blit(self.blackhole,self.circle)
            if self.holeCount == 200:
                self.ball = False
        if self.healthUp:
                self.drawText("HEAL UP", 22, SILVER, WIDTH / 2, HEIGHT * 3/4)
                if self.pUpCount >= 150:
                    self.healthUp = False
        if self.LazerbeamText:
                self.drawText("LAZERBEAM", 22, SILVER, WIDTH / 2, HEIGHT * 3/4)
                if self.pUpCount >= 150:
                    self.LazerbeamText = False
        if self.Lazerbeam == True:
            self.drawText(("Lazer Ammo: "+ str(self.LazerCount)),16,SILVER,WIDTH/2 -100,0)
        if self.ghostText:
            self.drawText("BOO", 22, SILVER, WIDTH / 2, HEIGHT * 3/4)
            if self.pUpCount >= 150:
                self.ghostText = False
        if self.sheildText:
            self.drawText("SHEILD UP", 22, SILVER, WIDTH / 2, HEIGHT * 3/4)
            if self.pUpCount >= 150:
                self.sheildText = False
        if self.blackText:
            self.drawText("BLACK AMMO", 22, SILVER, WIDTH / 2, HEIGHT * 3/4)
            if self.pUpCount >= 150:
                self.blackText = False
        if self.bHAText == True:
            self.drawText(("Black Hole: "+ str(self.bHoleAmmo)),16,SILVER,WIDTH/2 -100,16)
        #pg.draw.rect(self.screen,RED,self.player.rect,2)
##        if self.player.healthUp == True:
##                font1 = pg.font.Font("freesansbold.ttf", 16)
##                powerText = font1.render(("Healing"), True, SILVER)
##                textRect = powerText.get_rect()
##                textRect.midtop = (WIDTH/2,HEIGHT -250)
##                Fcount = self.Fcounter
##                self.screen.blit(powerText,textRect)
##                while self.Fcounter > 0:
##                    if self.Fcounter >= Fcount+120:
##                        self.Fcounter = 0
##                        self.player.healthUp = False
                        

        #pg.draw.rect(self.screen,RED,(self.m.hitbox),2)                 
                
                    
        # *after* drawing everything, flip the display
        pg.display.flip()
        

    def blitText(self,text):
        sceneExit = False
        time = 200  # 2000 milliseconds until we continue.
        print(time)
        while not sceneExit:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
            self.drawText(text,32,SILVER,WIDTH/2,HEIGHT*3/4)
            pg.display.update()
            passedTime = self.clock.tick(60)
            print(passedTime)
            time -= passedTime
            if time <= 0:
                sceneExit = True

    def show_start_screen(self):
        # game splash/start screen
        musicStart = True
        pg.mixer.music.load("music.mp3")
        if musicStart:
            pg.mixer.music.play(loops = -1)
        self.screen.fill(WHITE)
        #self.drawText(TITLE,48,BLACK,WIDTH/2,HEIGHT/4)
        self.Titlebox = pg.Rect(WIDTH/2 - 200,HEIGHT/4,300,50)
        self.titleDraw = pg.image.load("JumpyCuhh.png")
        self.screen.blit(self.titleDraw,self.Titlebox)
        #pg.draw.rect(self.screen, GREEN,(WIDTH/2 - 150,HEIGHT/2,300,50))
        self.green = pg.Rect(20,HEIGHT/2,300,50)
        self.startText = pg.image.load("Single Player.png")
        self.screen.blit(self.startText,self.green)
        self.Coop = pg.Rect(20,HEIGHT*3/4,300,50)
        self.startCoop = pg.image.load("CO OP.png")
        self.screen.blit(self.startCoop,self.Coop)
##        if self.green.collidepoint(mouse):
##            print("hit RED")
        #self.drawText("Arrows to move, Space to shoot", 22, WHITE, WIDTH/2,HEIGHT/2)
        #self.drawText("Press any KEY to Play or Press space for two players", 22, WHITE, WIDTH/2,HEIGHT * 3/4)
        self.drawText("Highscore: "+ str(self.highscore),22, WHITE, WIDTH/2, 0)
        pg.display.flip()
        #self.waitForStart()
        self.clickCheck()

    #pg.mouse.get_pressed()[0]
    def clickCheck(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
            mouse = pg.Rect(pg.mouse.get_pos()[0],pg.mouse.get_pos()[1],1,1)
            click = pg.mouse.get_pressed()[0]
            #print(click)
            if self.green.colliderect(mouse):
                self.startText = pg.image.load("Single Selected.png")
                self.screen.blit(self.startText,self.green)
                if click:
                    waiting = False
                    self.running = True
                    musicStart = False
            else:
                self.startText = pg.image.load("Single Player.png")
                self.screen.blit(self.startText,self.green)

            if self.Coop.colliderect(mouse):
                self.startText = pg.image.load("CO OP SEL.png")
                self.screen.blit(self.startText,self.Coop)
                if click:
                    waiting = False
                    self.twoPlayers = True
                    self.running = True
                    musicStart = False
            else:
                self.startText = pg.image.load("CO OP.png")
                self.screen.blit(self.startText,self.Coop)
            pg.display.flip()
            
                
    
    
    def waitForStart(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYDOWN:
                    waiting = False
                    self.running = True
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.twoPlayers = True
                        waiting = False
                        self.running = True

    def drawText(self,text,size,colour,x,y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, colour)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def Highscore(self):
        self.screen.fill(WHITE)
        pg.display.flip()
        

    def show_go_screen(self):
        # game over/continue
        pg.mixer.music.load("Venus.wav")
        pg.mixer.music.play(loops = -1)
        self.twoPlayers = False
        self.bHoleAmmo = 0
        self.LazerCount = 0
        self.alivePlayers = 2
        if self.highscore < self.player.score:
            self.screen.fill(WHITE)
            self.highscore = self.player.score
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.player.score))
            self.HIGHS = pg.Rect(40,40,300,50)
            self.startText = pg.image.load("NEW HIGHSCORE.png")
            self.screen.blit(self.startText,self.HIGHS)
            self.drawText(str(self.player.score), 50, BLACK, WIDTH * 3/4 + 70 ,36)
            self.green = pg.Rect(20,HEIGHT/2,300,50)
            self.startText = pg.image.load("Single Player.png")
            self.screen.blit(self.startText,self.green)
            self.Coop = pg.Rect(20,HEIGHT*3/4,300,50)
            self.startCoop = pg.image.load("CO OP.png")
            self.screen.blit(self.startCoop,self.Coop)
        else:
            self.screen.fill(RED)
            self.Died = pg.Rect(40,40,300,50)
            self.startText = pg.image.load("YOU DIED.png")
            self.screen.blit(self.startText,self.Died)
            self.drawText(("Your Score: "+ str(self.player.score)),50,SILVER,WIDTH * 1/4,HEIGHT/2 - 100)
            self.green = pg.Rect(20,HEIGHT/2,300,50)
            self.startText = pg.image.load("Single Player.png")
            self.screen.blit(self.startText,self.green)
            self.Coop = pg.Rect(20,HEIGHT*3/4,300,50)
            self.startCoop = pg.image.load("CO OP.png")
            self.screen.blit(self.startCoop,self.Coop)

        pg.display.flip()
        self.clickCheck()


startTime = time.time()
g = Game()
g.load_data()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
