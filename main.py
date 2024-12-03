import random
import pygame
import numpy as np
from PIL import Image
import time
import base64
import re


class Engine:
    def __init__(self):
        pygame.init()  # initialize pygame
        pygame.font.init()  # initialize fonts
        self.basefont = pygame.font.SysFont("Comic Sans MS", 30)  # finish initializing font
        self.stopwatch = stopwatch()
        self.stopwatch.update()
        self.scoreboard = scoreboard()
        self.init_groups()
        self.init_screen()
        self.poodissapear = 1
        self.food = 0
        self.score = 0
        self.clock = pygame.time.Clock()
        self.resetiter = 0
        self.animationtimer = 0
        self.growtimer = 0
        self.winner = 0
        self.starttime = time.time()
        self.showcontrols = 1
        self.winscore = 0
        self.haspooped = 0
        self.mode = 0
        self.itt = interactivetextbox()
        self.stringbuffer = []

    def init_score(self):
        self.score = 0
        self.winscore = 0
        self.mapscore = 0
        for sprite in self.tileset:
            if sprite.tilename == "plant1stage3wet":
                self.mapscore = self.mapscore + 1
        for sprite in self.tileset:
            if (
                sprite.tilename == "plant1stage1wet"
                or sprite.tilename == "plant1stage2wet"
                or sprite.tilename == "dirtwet"
            ):
                self.winscore = self.winscore + 1

    def test_win(self):
        if self.score >= self.winscore:
            self.winner = 1
        if self.mode == 6:
            if self.mapnum == 3:
                self.scoreboard.write(self.stopwatch.totalsec)
                self.mapnum = self.mapnum + 1
        if self.winner == 1:
            for sprite in self.poopobj:
                sprite.kill()
            for sprite in self.fishobj:
                sprite.kill()
            for sprite in self.allvisible:
                sprite.kill()
            self.food = 0
            self.mode = 5
            self.animationtimer = 0
            
    def init_screen(self):
        self.windowh = 640
        self.windoww = 960
        self.screen = pygame.display.set_mode((self.windoww, self.windowh))

    def init_groups(self):
        self.poopobj = pygame.sprite.Group()  # all poops
        self.fishobj = pygame.sprite.Group()  # all fish
        self.tileset = pygame.sprite.Group()  # all tiles
        self.allvisible = pygame.sprite.Group()  # all visible sprites
        self.watertiles = pygame.sprite.Group()  # all watertiles
        self.toanimate = pygame.sprite.Group()

    def render_screen(self):
        
        if self.mode == 0:
            splashscreen = pygame.image.load(f"{self.splashprefix}startscreen.png")
            self.screen.blit(splashscreen, (0,0))
        elif self.mode == 1:
            splashscreen = pygame.image.load(f"{self.splashprefix}entername.png")
            self.screen.blit(splashscreen, (0,0))
            self.render_hud()
        elif self.mode == 2:
            splashscreen = pygame.image.load(f"{self.splashprefix}controls.png")
            self.screen.blit(splashscreen,(0,0))
        elif self.mode == 3:
            
            #game running
            for sprite in self.allvisible:
                
                self.screen.blit(
                    sprite.image,
                    (sprite.rect.x - cameraobj.rect.x, sprite.rect.y - cameraobj.rect.y),
                )
            self.screen.blit(mycat.image, (mycat.rect.x - cameraobj.rect.x, mycat.rect.y - cameraobj.rect.y))
                
            self.render_hud()
        elif self.mode == 4:
            splashscreen = pygame.image.load(f"{self.splashprefix}pause.png")
            self.screen.blit(splashscreen,(0,0))
            pass
        elif self.mode == 5:
            if self.mapnum != 3:
                if self.winner == 1:
                    splashscreen = pygame.image.load(f"{self.splashprefix}nextlevel1.png")
                    self.screen.blit(splashscreen,(0,0))
                else:
                    splashscreen = pygame.image.load(f"{self.splashprefix}nextlevel2.png")
                    self.screen.blit(splashscreen,(0,0))

            

        elif self.mode == 6:
            splashscreen = pygame.image.load(f"{self.splashprefix}winscreen.png")
            self.screen.blit(splashscreen, (0,0))
            self.render_hud()
            #game won

        
        pygame.display.flip()
        
        
    def render_hud(self):
        if self.mode == 1:
            self.itt.render()
        elif self.mode == 3:
            if self.showcontrols == 1:
                controlmessage = self.basefont.render("use the arrow keys or wasd to move", False, (255, 255, 255))
                self.screen.blit(controlmessage, ((self.windoww / 2) - 200, (self.windowh / 2) - 200))
            elif self.showcontrols == 0 and self.food < 2 and self.score < self.winscore:
                hungermes = self.basefont.render("you feel hungry", False, (255, 255, 255))
                self.screen.blit(hungermes, ((self.windoww / 2) - 100, (self.windowh / 2) - 200))
            elif self.showcontrols == 0 and self.food == 100 and self.score < self.winscore:
                fullmesg = self.basefont.render("you feel full", False, (255, 255, 255))
                self.screen.blit(fullmesg, ((self.windoww / 2) - 80, (self.windowh / 2) - 200))
            elif self.showcontrols == 0 and self.food > 2 and self.haspooped == 0:
                poomesg = self.basefont.render("use spacebar to poop. plants need poop to grow", False, (255, 255, 255))
                self.screen.blit(poomesg, ((self.windoww / 2) - 250, (self.windowh / 2) - 200))
            elif self.showcontrols == 0 and self.haspooped == 1:
                scoremesg = self.basefont.render(f"SCORE: {self.score}  /  {self.winscore}", False, (255, 255, 255))
                self.screen.blit(scoremesg, ((self.windoww / 2) - 58, (self.windowh / 10)))
            stopwatchmesg = self.basefont.render(self.stopwatch.stopwatchmesg, False, (255, 255, 255))
            self.screen.blit(stopwatchmesg, (50, ((self.windowh / 10) * 9)))
        elif self.mode == 5:
            pass
        elif self.mode == 6:
            
            winmessage = self.basefont.render("you win! thanks for playing my tech demo!", False, (255, 255, 255))
            self.screen.blit(winmessage, ((self.windoww / 2) - 180, self.windowh / 2 - 220))
            self.scoreboard.build()
            
            if len(self.scoreboard.top10) >= 1:
                self.screen.blit(self.scoreboard.mesg, (((self.windoww /2) - 50), self.windowh / 2 - 180))
                self.screen.blit(self.scoreboard.first, (((self.windoww / 2) - 145), self.windowh / 2 - 160))
            if len(self.scoreboard.top10) >= 2:
                self.screen.blit(self.scoreboard.second, (((self.windoww / 2) - 145), self.windowh / 2 - 140))
            if len(self.scoreboard.top10) >= 3:
                self.screen.blit(self.scoreboard.third, (((self.windoww / 2) - 145), self.windowh / 2 - 120))
            if len(self.scoreboard.top10) >= 4:
                self.screen.blit(self.scoreboard.fourth, (((self.windoww / 2) - 145), self.windowh / 2 - 100))
            if len(self.scoreboard.top10) >= 5:
                self.screen.blit(self.scoreboard.fifth, (((self.windoww / 2) - 145), self.windowh / 2 - 80))
            if len(self.scoreboard.top10) >= 6:
                self.screen.blit(self.scoreboard.sixth, (((self.windoww / 2) - 145), self.windowh / 2 - 60))
            if len(self.scoreboard.top10) >= 7:
                self.screen.blit(self.scoreboard.seventh, (((self.windoww / 2) - 145), self.windowh / 2 - 40))
            if len(self.scoreboard.top10) >= 8:
                self.screen.blit(self.scoreboard.eigth, (((self.windoww / 2) - 145), self.windowh / 2 - 20))
            if len(self.scoreboard.top10) >= 9:
                self.screen.blit(self.scoreboard.ninth, (((self.windoww / 2) - 145), self.windowh / 2))
            if len(self.scoreboard.top10) >= 10:
                self.screen.blit(self.scoreboard.tenth, ((((self.windoww / 2) - 145), ((self.windowh / 2) + 20))))
        

    def update_logic(self):
        
        if self.mode == 0:
            #title screen
            pass
        elif self.mode == 1:
            #enter name
            self.itt.update()
            pass
        elif self.mode == 2:
            #show controls
            pass
        elif self.mode == 3:
            
            self.normalize_velocity()
            
            self.update_fish()
            
            mycat.update()
            
            self.poopobj.update()
            
            self.animate_all()
            
            cameraobj.update()
            
            self.lock_in_bounds()
            
            self.calculate_score()
            
            self.test_win()
            
            self.grow_plants()
            
            if self.winner == 0:
                self.stopwatch.update()
                
        elif self.mode == 4:
            #paused
            self.stopwatch.update()
            pass
        elif self.mode == 5:
            #next level
            if self.mapnum == 3:    
                self.mode = 6
            else:
                if self.winner == 1:
                    for sprite in self.allvisible:
                        sprite.kill()
                    mycat.xv = 0
                    mycat.yv = 0
                    self.toanimate.add(mycat)
                    mycat.animiter = 0
                    self.mapnum = self.mapnum + 1
                    self.stopwatch.reset()
                    self.generate_bg()
                    self.init_score()
                    self.init_bg_frame()
                    self.winner = 0
            
        elif self.mode == 6:
            self.test_win()
            pass
            #won
            
        
    def animate_all(self):
        self.animationtimer = self.animationtimer + 1
        if self.animationtimer > 10:
            self.animationtimer = 0
            for sprite in self.toanimate:
                sprite.animate()

    def test_keys(self):
        
        if self.mode == 0:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.mode = 1
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
        elif self.mode == 1:
            #enter name
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.playername = "".join(self.stringbuffer)
                        self.stringbuffer = []
                        self.mode = 2
                    elif event.key == pygame.K_BACKSPACE:
                        if len(self.stringbuffer) >= 1:
                            self.stringbuffer.pop()
                    else:
                        self.stringbuffer.append(event.unicode)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
        elif self.mode == 2:
            #show controls
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.stopwatch.reset()
                        self.mode = 3
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
        elif self.mode == 3:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.winner = 1
                    if event.key == pygame.K_u:
                        mycat.catcolor = 0
                    if event.key == pygame.K_i:
                        mycat.catcolor = 1
                    if event.key == pygame.K_o:
                        mycat.catcolor = 2
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        mycat.xv = -10
                        self.showcontrols = 0
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        mycat.xv = 10
                        self.showcontrols = 0
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        mycat.yv = -10
                        self.showcontrols = 0
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        mycat.yv = 10
                        self.showcontrols = 0
                    if event.key == 27:  # escape
                        self.mode = 4
                        self.stopwatch.pause()
                        
                    elif event.key == 32:  # spacebar
                        if self.food > 0:
                            self.food = self.food - 1
                            if len(self.poopobj) < 10:
                                Poop(mycat.rect.left, mycat.rect.top)
                            else:
                                j = 0
                                tempi = 0
                                while tempi < 10:
                                    tempi = tempi + 1
                                    for e in self.poopobj:
                                        j = j + 1
                                        if j == 1:
                                            if self.poodissapear == 1:
                                                e.kill()
                                            Poop(mycat.rect.left, mycat.rect.top)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        mycat.resetx = 1
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        mycat.resetx = 1
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        mycat.resety = 1
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        mycat.resety = 1
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
        elif self.mode == 4:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == 27:
                            self.mode = 3
                            self.stopwatch.unpause()
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
        elif self.mode == 5:
            if self.winner == 0:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            self.mode = 3
                            self.stopwatch.reset()
            else:
                for event in pygame.event.get():
                    if event.key == pygame.K_RETURN:
                        #dump any presses of enter while we were leading to prevent unexpected behavior
                        pass
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            pass
        elif self.mode == 6:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

    def update_fish(self):
        if len(self.fishobj) < len(self.watertiles) * 2:
            for sprite in self.tileset:
                sprite.populate_fish()
        for e in self.fishobj:
            if e.rect.colliderect(mycat.rect) == True:
                if self.food < 100:
                    self.food = self.food + 1
                    e.kill()

    def calculate_score(self):
        self.score = 0
        for sprite in self.tileset:
            if sprite.tilename == "plant1stage3wet":
                self.score = self.score + 1
        self.score = self.score - self.mapscore

    def normalize_velocity(self):
        if mycat.xv > 10:
            mycat.xv = 10
        if mycat.yv > 10:
            mycat.yv = 10
        if mycat.xv < -10:
            mycat.xv = -10
        if mycat.yv < -10:
            mycat.yv = -10
        self.resetiter = self.resetiter + 1
        if self.resetiter > 5:
            self.resetiter = 0
            if mycat.resetx == 1:
                mycat.xv = 0
                mycat.resetx = 0
            if mycat.resety == 1:
                mycat.yv = 0
                mycat.resety = 0
            mycat.resetx = 0
            mycat.resety = 0

    def grow_plants(self):
        self.growtimer = self.growtimer + 1
        if self.growtimer > 60:
            self.growtimer = 0
            for sprite in self.tileset:
                sprite.grow()

    def lock_in_bounds(self):
        mycat.rect.clamp_ip(self.bgframe.rect)
        cameraobj.rect.clamp_ip(self.bgframe.rect)


class Camera(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(0, 0, myengine.windoww, myengine.windowh)
        self.update()

    def update(self):
        self.rect.centerx, self.rect.centery = mycat.rect.centerx, mycat.rect.centery


class interactivetextbox(pygame.sprite.Sprite):
    def __init__(self):
        pass
    def render(self):
        myengine.screen.blit(self.image,self.rect)
    def update(self):
        self.image = myengine.basefont.render("".join(myengine.stringbuffer), False , (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (myengine.windoww / 2, myengine.windowh / 2)
        pass

class Background(Engine):
    def __init__(self):
        super().__init__()
        self.tileprefix = "Assets/tiles/"  # prefix for tile filenames
        self.mapprefix = "Assets/maps/"  # prefix for input map filenames
        self.splashprefix = "Assets/splashscreens/"
        self.mapdict = {0:"Level1", 1:"Level2", 2:"Level3", 3:"pallette"}
        self.mapnum = 0
        self.generate_bg()
        
    def init_bg_frame(self):
        self.bgframe = Bgframe()
    def mapnum_to_mapname(self):
        self.mapname = self.mapdict[self.mapnum]

    def init_tiles(self, tilename=("finishinit"), x=0, y=0):
        # this function initializes the tileset with the proper states based on tilename
        assert (
            type(tilename) is str
        ), "check input to inittiles tilename must be a string"
        assert (
            type(x) is int and type(y) is int
        ), "check input to inittiles x and y must be positive ints"
        assert (
            x >= 0 and y >= 0
        ), "check input to inittiles x and y must be positive ints"
        if tilename == "catbeddry":
            Tile("catbeddry", f"{self.tileprefix}catbeddry.png", x, y, self)
        elif tilename == "catbedwet":
            Tile("catbedwet", f"{self.tileprefix}catbedwet.png", x, y, self)
        elif tilename == "dirtdry":
            Tile("dirtdry", f"{self.tileprefix}dirtdry.png", x, y, self)
        elif tilename == "dirtuntilled":
            Tile("dirtuntilled", f"{self.tileprefix}dirtuntilled.png", x, y, self)
        elif tilename == "dirtwet":
            Tile("dirtwet", f"{self.tileprefix}dirtwet.png", x, y, self)
        elif tilename == "grass1":
            Tile("grass1", f"{self.tileprefix}grass1.png", x, y, self)
        elif tilename == "plant1stage1dry":
            Tile("plant1stage1dry", f"{self.tileprefix}plant1stage1dry.png", x, y, self)
        elif tilename == "plant1stage1wet":
            Tile("plant1stage1wet", f"{self.tileprefix}plant1stage1wet.png", x, y, self)
        elif tilename == "plant1stage2dry":
            Tile("plant1stage2dry", f"{self.tileprefix}plant1stage2dry.png", x, y, self)
        elif tilename == "plant1stage2wet":
            Tile("plant1stage2wet", f"{self.tileprefix}plant1stage2wet.png", x, y, self)
        elif tilename == "plant1stage3dry":
            Tile("plant1stage3dry", f"{self.tileprefix}plant1stage3dry.png", x, y, self)
        elif tilename == "plant1stage3wet":
            Tile("plant1stage3wet", f"{self.tileprefix}plant1stage3wet.png", x, y, self)
        elif tilename == "water":
            Tile("water", f"{self.tileprefix}water.png", x, y, self)
        else:
            pass

    def map_to_tiles(self, mapname):
        mappath = f"{self.mapprefix}{mapname}.png"
        conversiondict = {  # dictionary of tuples of rgb values as keys for tile names
            (np.uint8(229), np.uint8(45), np.uint8(255)): "catbeddry",
            (np.uint8(183), np.uint8(4), np.uint8(134)): "catbedwet",
            (np.uint8(241), np.uint8(240), np.uint8(92)): "dirtdry",
            (np.uint8(202), np.uint8(195), np.uint8(67)): "dirtuntilled",
            (np.uint8(74), np.uint8(41), np.uint8(0)): "dirtwet",
            (np.uint8(32), np.uint8(254), np.uint8(0)): "grass1",
            (np.uint8(224), np.uint8(166), np.uint8(41)): "plant1stage1dry",
            (np.uint8(227), np.uint8(243), np.uint8(0)): "plant1stage1wet",
            (np.uint8(255), np.uint8(198), np.uint8(45)): "plant1stage2dry",
            (np.uint8(212), np.uint8(255), np.uint8(0)): "plant1stage2wet",
            (np.uint8(255), np.uint8(174), np.uint8(0)): "plant1stage3dry",
            (np.uint8(255), np.uint8(253), np.uint8(0)): "plant1stage3wet",
            (np.uint8(0), np.uint8(36), np.uint8(254)): "water",
        }
        img = Image.open(mappath)  # import image as a pillow image
        img = img.convert("RGB")  # drop alpha
        img = np.asarray(img)  # import picture as numpy array
        inputw = img.shape[1]  # set inputw to the width of the input image
        inputh = img.shape[0]  # set inputh to the height of the input image
        p = 0
        tiles = []  # initialize
        temparray = []  # initialize a temporary array to pop from
        rgbvalues = []  # flat array of tuples representing rgb values
        for (
            m
        ) in (
            img
        ):  # loop through the 3d numpy array to extract an 1d array of tuples of rgb values
            for n in m:
                for o in n:
                    if p < 3:
                        p = p + 1
                        temparray.append(o)
                    else:
                        p = 1
                        rgbvalues.append(tuple(temparray))
                        temparray = []
                        temparray.append(o)
        rgbvalues.append(tuple(temparray))
        temparray = []
        for x in rgbvalues:  # convert the array to an array of tile file names
            tiles.append(conversiondict[x])
        return (tiles, inputh, inputw)

    def tiles_to_full_map(self, listoftiles, numofrows, numofcols):
        assert len(listoftiles) + 1 != int(numofrows) * int(
            numofcols
        ), "the list passed to tilestofullmap would not generate a valid map"
        tilewidth = 200  # the width in pixels of the tiles
        tileheight = 200  # the width in pixels of the tiles
        j = 1
        witer = 0
        hiter = 0
        bgwidth = numofcols * tilewidth
        bgheight = numofrows * tileheight
        iterlist = [0] * len(listoftiles)
        for e in iterlist:
            if j < numofcols:
                self.init_tiles(listoftiles.pop(0), witer, hiter)
                witer = witer + tilewidth
            else:
                self.init_tiles(listoftiles.pop(0), witer, hiter)
                witer = 0
                j = 0
                hiter = hiter + tileheight
            j = j + 1
        self.bgwidth, self.bgheight = bgwidth, bgheight

    def generate_bg(self):
        self.mapnum_to_mapname()
        catchreturn1 = self.map_to_tiles(self.mapname)
        self.tiles_to_full_map(catchreturn1[0], catchreturn1[1], catchreturn1[2])


class Tile(pygame.sprite.Sprite, Background):
    def __init__(self, tilename, image_file, posx, posy, engine):
        assert type(tilename) is str, "tilename must be a string"
        assert (
            type(posx) is int and type(posy) is int and posx >= 0 and posy >= 0
        ), "posx and posy must be positivve ints"
        self.tilename = tilename
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file)  # load the tile image by name
        self.image = self.image.convert()
        self.rect = self.image.get_rect()  # prebaked rect from image
        self.rect.left, self.rect.top = (
            posx,
            posy,
        )  # takes in arguments to set position of rect
        tilename = tilename  # defines tilename
        engine.allvisible.add(self)  # adds to visible objects
        engine.tileset.add(self)
        if self.tilename == "water":  # adds to the group of water tiles if it is one
            engine.watertiles.add(self)

    def grow(self):
        # grows all plants that are wet and have [poop on them]
        if self.tilename == "plant1stage1wet":
            if pygame.sprite.spritecollideany(self, myengine.poopobj) is not None:
                self.tilename = "plant1stage2wet"
                self.image = pygame.image.load(
                    f"{myengine.tileprefix}plant1stage2wet.png"
                )
                self.image = self.image.convert()
                pooptokill = pygame.sprite.spritecollideany(self, myengine.poopobj)
                pooptokill.used = 1
        elif self.tilename == "plant1stage2wet":
            if pygame.sprite.spritecollideany(self, myengine.poopobj) is not None:
                self.tilename = "plant1stage3wet"
                self.image = pygame.image.load(
                    f"{myengine.tileprefix}plant1stage3wet.png"
                )
                self.image = self.image.convert()
                pooptokill = pygame.sprite.spritecollideany(self, myengine.poopobj)
                pooptokill.used = 1
        elif self.tilename == "dirtwet":
            if pygame.sprite.spritecollideany(self, myengine.poopobj) is not None:
                self.tilename = "plant1stage1wet"
                self.image = pygame.image.load(
                    f"{myengine.tileprefix}plant1stage1wet.png"
                )
                self.image = self.image.convert()
                pooptokill = pygame.sprite.spritecollideany(self, myengine.poopobj)
                pooptokill.used = 1

    def populate_fish(self):
        if self.tilename == "water":
            fish(
                random.randrange(
                    self.rect.left, (self.rect.left + self.rect.width) - 32
                ),
                random.randrange(self.rect.top, (self.rect.top + self.rect.width) - 32),
            )


class Bgframe(pygame.sprite.Sprite):
    # makes a rect around the background for collision detection
    def __init__(self):
        assert (
            type(myengine.bgwidth) is int and type(myengine.bgheight) is int
        ), "Bgframe requires bgheight and bgwidth to be non zero positive ints"
        assert (
            myengine.bgwidth > 0 and myengine.bgheight > 0
        ), "Bgframe requires bgheight and bgwidth to be non zero positive ints"
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(0, 0, myengine.bgwidth, myengine.bgheight)

class scoreboard:
    def __init__(self):
        with open("Assets/saves/sb.scoreboard", "r") as scoreboard:
            scoreboard_b64_list = scoreboard.readlines()
            unsortedScoreboard = []
            for i in scoreboard_b64_list:
                unsortedScoreboard.append(base64.standard_b64decode(i).decode())
            self.unsortedscoreboard = unsortedScoreboard
            self.sortedscoreboard = sorted(
                unsortedScoreboard, key=lambda test_string: list(map(int, re.findall(r"\d+", test_string)))[0]
            )
            self.top10 = []
            i = 0
            for score in self.sortedscoreboard:
                if i <= 9:
                    self.top10.append(score)
                    i = i + 1

    def write(self, timelapsed):
        winning_stopwatch = f"{myengine.playername}  {myengine.stopwatch.elapsedsec:.2f} seconds"
        winning_stopwatch = winning_stopwatch.encode("utf-8")
        with open("Assets/saves/sb.scoreboard", "a") as scoreboard:
            b64winning_stopwatch = base64.standard_b64encode(winning_stopwatch)
            scoreboard.write(b64winning_stopwatch.decode())
            scoreboard.write("\n")
        with open("Assets/saves/sb.scoreboard", "r") as scoreboard:
            scoreboard_b64_list = scoreboard.readlines()
            unsortedScoreboard = []
            for i in scoreboard_b64_list:
                unsortedScoreboard.append(base64.standard_b64decode(i).decode())
            self.unsortedscoreboard = unsortedScoreboard
            self.sortedscoreboard = sorted(
                unsortedScoreboard, key=lambda test_string: list(map(int, re.findall(r"\d+", test_string)))[0]
            )
            self.top10 = []
            i = 0
            for score in self.sortedscoreboard:
                if i <= 9:
                    self.top10.append(score)
                    i = i + 1
                    
    def build(self):
        self.__init__()
        if len(self.top10) >= 10:
            self.tenth = myengine.basefont.render(f"10). {self.top10[9]}", False, (255, 255, 255))
        if len(self.top10) >= 9:
            self.ninth = myengine.basefont.render(f"9). {self.top10[8]}", False, (255, 255, 255))
        if len(self.top10) >= 8:
            self.eigth = myengine.basefont.render(f"8). {self.top10[7]}", False, (255, 255, 255))
        if len(self.top10) >= 7:
            self.seventh = myengine.basefont.render(f"7). {self.top10[6]}", False, (255, 255, 255))
        if len(self.top10) >= 6:
            self.sixth = myengine.basefont.render(f"6). {self.top10[5]}", False, (255, 255, 255))
        if len(self.top10) >= 5:
            self.fifth = myengine.basefont.render(f"5). {self.top10[4]}", False, (255, 255, 255))
        if len(self.top10) >= 4:
            self.fourth = myengine.basefont.render(f"4). {self.top10[3]}", False, (255, 255, 255))
        if len(self.top10) >= 3:
            self.third = myengine.basefont.render(f"3). {self.top10[2]}", False, (255, 255, 255))
        if len(self.top10) >= 2:
            self.second = myengine.basefont.render(f"2). {self.top10[1]}", False, (255, 255, 255))
        if len(self.top10) >= 1:
            self.mesg = myengine.basefont.render("SCOREBOARD", False, (255,255,255))
            self.first = myengine.basefont.render(f"1). {self.top10[0]}", False, (255, 255, 255))




class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # initialize sprite
        self.catcolor = 0 # 0 for gray 1 for black 2 for brown
        self.catprefix = "Assets/sprites/cat/grayCat/"
        self.image = pygame.transform.scale2x(
            pygame.image. load(f"{self.catprefix}catstand1.png")
        )  # initialize the image of the cat stationary
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.update(
            (myengine.windoww / 2) - 30, (myengine.windowh / 2) - 30, 100, 100
        )
        self.animiter = 0
        myengine.allvisible.add(self)
        myengine.toanimate.add(self)
        
        self.xv = 0
        self.yv = 0
        self.resetx = 0
        self.resety = 0
        
    
    def update(self):
        self.rect.move_ip(self.xv, self.yv)

    def animate(self):
        if self.catcolor == 0:
            self.catprefix = "Assets/sprites/cat/grayCat/"
        elif self.catcolor == 1:
            self.catprefix = "Assets/sprites/cat/blackCat/"
        elif self.catcolor == 2:
            self.catprefix = "Assets/sprites/cat/brownCat/" 
        else:
            self.catcolor = 0
            self.catprefix = "Assets/sprites/cat/grayCat"
        self.animiter = self.animiter + 1
        self.left = 0
        self.right = 0
        self.down = 0
        self.up = 0
        self.idle = 0
# this section of logic determines which way the cat should face favoring left and right over up and down
        if self.xv >= 1:
            self.right = 1  
        if self.yv >= 1:
            self.down = 1
        if self.xv < 0:
            self.left = 1
        if self.yv < 0:
            self.up = 1
        if self.right == 1:
            self.up = 0
            self.down = 0
        if self.left == 1:
            self.up = 0
            self.down = 0
        if self.xv == 0 and self.yv == 0:
            self.up = 0
            self.right = 0
            self.left = 0
            self.down = 0
            self.idle = 1
        if self.left == 1:
            # handles changing the sprite for animation
            if self.animiter < 3:

                self.image = pygame.transform.scale2x(
                    pygame.image. load(f"{self.catprefix}catleft1.png")
                )
                self.image = self.image.convert_alpha()
            else:
                self.image = pygame.transform.scale2x(
                    pygame.image. load(f"{self.catprefix}catleft2.png")
                )
                self.image = self.image.convert_alpha()
                if self.animiter > 4:
                    self.animiter = 0
        if self.right == 1:
            # handles changing the sprite for animation
            if self.animiter < 3:
                self.image = pygame.transform.scale2x(
                    pygame.image. load(f"{self.catprefix}catright1.png")
                )
                self.image = self.image.convert_alpha()
            else:
                self.image = pygame.transform.scale2x(
                    pygame.image. load(f"{self.catprefix}catright2.png")
                )
                self.image = self.image.convert_alpha()
                if self.animiter > 4:
                    self.animiter = 0
        if self.up == 1:
            # handles changing the sprite for animation
            if self.animiter < 3:
                self.image = pygame.transform.scale2x(
                    pygame.image. load(f"{self.catprefix}catup1.png")
                )
                self.image = self.image.convert_alpha()
            else:
                self.image = pygame.transform.scale2x(
                    pygame.image. load(f"{self.catprefix}catup2.png")
                )
                self.image = self.image.convert_alpha()
                if self.animiter > 4:
                    self.animiter = 0
        if self.down == 1:
            # handles changing the sprite for animation
            if self.animiter < 3:
                self.image = pygame.transform.scale2x(
                    pygame.image. load(f"{self.catprefix}catwalkdown1.png")
                )
                self.image = self.image.convert_alpha()
            else:
                self.image = pygame.transform.scale2x(
                    pygame.image. load(f"{self.catprefix}catwalkdown2.png")
                )
                self.image = self.image.convert_alpha()
                if self.animiter > 4:
                    self.animiter = 0
        if self.idle == 1:
            # handles changing the sprite for animation this handles idle animations
            if self.animiter < 150:
                self.image = pygame.transform.scale2x(
                    pygame.image. load(f"{self.catprefix}catstand1.png")
                )
                self.image = self.image.convert_alpha()
            else:
                self.image = pygame.transform.scale2x(
                    pygame.image. load(f"{self.catprefix}catstand2.png")
                )
                self.image = self.image.convert_alpha()
                if self.animiter > 158:
                    self.animiter = 0


class Poop(pygame.sprite.Sprite):
    # this class makes poop objects
    def __init__(
        self, catx, caty, image="Assets/sprites/poop1.png"
    ):  # initialize poop object
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.update((catx + 50), (caty + 50), 32, 32)  # places the poop at the cat
        myengine.allvisible.add(self)
        myengine.poopobj.add(self)
        self.used = 0
        myengine.haspooped = 1

    def update(self):
        if self.used == 1:
            self.kill()


class fish(pygame.sprite.Sprite):
    # this class makes fish objects
    def __init__(self, tempx, tempy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            "Assets/sprites/fish1.png"
        )  # init fish sprite with image
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()  # init fish recct
        self.rect.update(tempx, tempy, 32, 32)  # place fish
        myengine.fishobj.add(self)  # add to group of fish
        myengine.allvisible.add(self)  # add to group of visible

class stopwatch:
    def __init__(self):
        self.starttime = time.time()
        self.pausedtime = 0
        self.totalpausedtime = 0
        self.paused = 0
        self.elapsedsec = 0
        self.totalsec = 0
    def reset(self):
        self.startime = time.time()
        self.totalsec = self.totalsec + self.elapsedsec
    def update(self):
        if self.paused == 0:
            self.elapsedsec = (time.time() - self.starttime) - self.totalpausedtime
            self.stopwatchmesg = f"time elapsed: {self.elapsedsec:.2f}  seconds"
        elif self.paused == 1:
            self.pausedtime = (time.time() - self.pausestart)
    def pause(self):        
        self.pausestart = time.time()
        self.paused = 1
    def unpause(self):
        self.totalpausedtime = self.totalpausedtime + self.pausedtime
        self.paused = 0


def start_game():
    global myengine
    global mycat
    global cameraobj
    myengine = Background()
    mycat = Player()
    cameraobj = Camera()
    myengine.init_bg_frame()
    myengine.init_score()


def main():
    start_game()
    myengine.init_bg_frame()
    myengine.init_score()
    while True:
        myengine.test_keys()
        myengine.update_logic()
        myengine.render_screen()
        myengine.clock.tick(60)
main()
