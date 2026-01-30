import pygame, random, math

def text(centerx, centery, w, h, txt, color, screen):
    font = pygame.font.Font("FantasqueSansMono-Regular.ttf")
    fontrect = pygame.rect.Rect(6, 7, w, h)
    fontrect.center = [centerx, centery]
    fontsurface = font.render(str(txt), False, color)
    fontsurface = pygame.transform.scale(fontsurface, (w, h))
    screen.blit(fontsurface, fontrect)


class Person:
    def __init__(self, x, y, r, sped, dir, state, incube, infect):
        self.x = x
        self.y = y
        self.r = r

        self.rect = pygame.rect.Rect(6, 7, self.r * 2, self.r * 2)
        self.rect.centerx = self.x
        self.rect.centery = self.y

        self.sped = sped
        self.dir = dir
        self.state = state
        self.xv = math.cos(math.radians(self.dir)) * self.sped
        self.yv = -math.sin(math.radians(self.dir)) * self.sped
        self.state = state
        self.infecttimer = random.randint(0, 30)
        self.recoverytimer = infect * 60
        self.carriertime = self.recoverytimer - incube * 60
        self.images = []

        for filename in ["normal.png", "carrier.png", "sick.png", "recovered.png", "dead.png"]:
            self.image = pygame.image.load(filename)
            self.image = pygame.transform.scale(self.image, [self.r * 2, self.r * 2])
            self.image.set_colorkey([0, 0, 0])
            self.images.append(self.image)



    def render(self, screen):
        if self.state == "normal":
            screen.blit(self.images[0], self.rect)
        elif self.state == "infected":
            if self.recoverytimer <= self.carriertime:
                screen.blit(self.images[2], self.rect)
            else:
                screen.blit(self.images[1], self.rect)
        elif self.state == "recovered":
            screen.blit(self.images[3], self.rect)
        elif self.state == "dead":
            screen.blit(self.images[4], self.rect)

    def move(self, others, quarantine):
        if self.state != "dead":
            if self.x <= self.r or self.x + self.r >= 650:
                self.xv *= -1
            if self.y <= self.r or self.y + self.r >= 700:
                self.yv *= -1

            self.x += self.xv
            self.y += self.yv
            self.rect.centerx = self.x
            self.rect.centery = self.y
        if self.state != "infected":
            for person in others:
                if math.dist([self.x, self.y], [person.x, person.y]) <= quarantine and person.state == "infected" and person.recoverytimer <= person.carriertime:
                    self.distance = math.dist([self.x, self.y], [person.x, person.y])
                    if self.distance > 0:
                        self.xv = (self.x - person.x) / self.distance * self.sped
                        self.yv = (self.y - person.y) / self.distance * self.sped
    def infect(self, others, mindist, chance):
        if self.recoverytimer <= self.carriertime:
            self.chance = chance
        else:
            self.chance = chance / 2

        for person in others:
            if person.state == "normal" and math.dist([self.x, self.y], [person.x, person.y]) <= mindist and random.random() <= self.chance:
                person.state = "infected"



    def update(self, screen, others, mindist, chance, survival, quarantine):
        self.move(others, quarantine)
        if self.state == "infected":
            self.infecttimer = (self.infecttimer + 1) % 60
            self.recoverytimer -= 1
            if self.recoverytimer <= 0:
                if random.random() <= survival:
                    self.state = "recovered"
                else:
                    self.state = "dead"
        if self.state == "infected" and self.infecttimer == 0:
            self.infect(others, mindist, chance)
        self.render(screen)


class Slider:
    def __init__(self, barcenterx, barcentery, barcolor, barlength, barwidth, initialpercentage, sliderimage, sliderimagew, sliderimageh):
        self.barcenterx = barcenterx
        self.barcentery = barcentery
        self.barcolor = barcolor
        self.barlength = barlength
        self.barwidth = barwidth
        self.initalpercentage = initialpercentage
        self.sliderimage = sliderimage
        self.sliderimagew = sliderimagew
        self.sliderimageh = sliderimageh
        self.image = pygame.image.load(sliderimage)
        self.image = pygame.transform.scale(self.image, (self.sliderimagew, self.sliderimageh))
        self.image.set_colorkey([0, 0, 0])
        self.rect = pygame.rect.Rect(0, 0, self.sliderimagew, self.sliderimageh)
        self.rect.centerx = pygame.math.lerp(self.barcenterx - self.barlength / 2, self.barcenterx + self.barlength / 2, self.initalpercentage)
        self.rect.centery = self.barcentery
        self.hasclicked = True

    def render(self, screen):
        pygame.draw.line(screen, self.barcolor, (self.barcenterx + self.barlength / 2, self.barcentery), (self.barcenterx - self.barlength / 2, self.barcentery), self.barwidth)
        screen.blit(self.image, self.rect)

    def updatepos(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) and pygame.mouse.get_pressed()[0]:
            self.hasclicked = True
        if not pygame.mouse.get_pressed()[0]:
            self.hasclicked = False
        if self.hasclicked:
            self.rect.centerx = pygame.math.clamp(pygame.mouse.get_pos()[0], self.barcenterx - self.barlength / 2, self.barcenterx + self.barlength / 2)
            self.rect.centery = self.barcentery

    def update(self, screen):
        self.updatepos()
        self.render(screen)

    def findvalue(self, startval, endval):
        self.weight = (self.rect.centerx - (self.barcenterx - self.barlength / 2)) / self.barlength
        return round(pygame.math.lerp(startval, endval, self.weight), 2)

class Button:
    def __init__(self, centerx, centery, w, h, text):
        self.centerx = centerx
        self.centery = centery
        self.w = w
        self.h = h
        self.txtwratio = 0.7
        self.txthratio = 0.8
        self.rect = pygame.rect.Rect(6, 7, self.w, self.h)
        self.txtrect = pygame.rect.Rect(6, 7, self.w * self.txtwratio, self.h * self.txthratio)
        self.rect.center = [self.centerx, self.centery]
        self.txtrect.center = [self.centerx, self.centery]
        self.text = text
        self.font = pygame.font.Font("FantasqueSansMono-Regular.ttf")
        if self.text != None:
            self.fontsurface = self.font.render(self.text, False, [0, 0, 0])
            self.fontsurface = pygame.transform.scale(self.fontsurface, (self.w * self.txtwratio, self.h * self.txthratio))

    def render(self, screen):
        pygame.draw.rect(screen, [255,255,255], self.rect)
        pygame.draw.rect(screen, [0,0,0], self.rect, 5)
        if self.text != None:
            screen.blit(self.fontsurface, self.txtrect)
    def update(self, screen):
        self.render(screen)
    def checkcollisions(self):
        return self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_just_pressed()[0]
