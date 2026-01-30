import pygame, random, classes, math
pygame.init()
screen = pygame.display.set_mode([1300, 700])

#TOTAL POPULATION
POPULATION = 0
RATE = 0
INFECTIONDIST = 0
SURVIVAL = 0
INCUBE = 0
INFECT = 0
VACCINATED = 0
QUARANTINE = 0

FPS = 60
clock = pygame.Clock()

#ASSETS
rateslider = classes.Slider(1050, 200, [0,0,0], 100, 5, 0.5, "slider.png", 10, 20)
popslider = classes.Slider(1050, 200, [0,0,0], 100, 5, 0.5, "slider.png", 10, 20)
distslider = classes.Slider(1050, 300, [0,0,0], 100, 5, 0.5, "slider.png", 10, 20)
surviveslider = classes.Slider(1050, 400, [0,0,0], 100, 5, 0.5, "slider.png", 10, 20)
incubeslider = classes.Slider(1050, 300, [0,0,0], 100, 5, 0.5, "slider.png", 10, 20)
infectslider = classes.Slider(1050, 400, [0,0,0], 100, 5, 0.5, "slider.png", 10, 20)
vacslider = classes.Slider(1050, 500, [0,0,0], 100, 5, 0, "slider.png", 10, 20)
qslider = classes.Slider(1050, 500, [0,0,0], 100, 5, 0, "slider.png", 10, 20)
timeslider = classes.Slider(367, 456, [0,0,0], 401, 5, 1, "slider.png", 10, 20)
covidbutton = classes.Button(1050, 600, 100, 50, "Covid 19")
tbbutton = classes.Button(1200, 600, 100, 50, "TB")
rhinobutton = classes.Button(1050, 660, 100, 50, "Rhinovirus")
measlesbutton = classes.Button(1200, 660, 100, 50, "Measles")
startbutton = classes.Button(1044, 554, 100, 50, "Start")
infectbutton = classes.Button(1044, 609, 100, 50, "Infect")
resetbutton = classes.Button(1044, 662, 100, 50, "Reset")


simstate = "start"
paused = True
showinstructions = False

dataanalysis = pygame.image.load("dataanalysis.png")
dataanalysis = pygame.transform.scale(dataanalysis, [1300, 700])
dataanalysis.set_colorkey([0,0,0])
instructions = pygame.image.load("instructions.png")
instructions = pygame.transform.scale(instructions, [650, 700])
instructions.set_colorkey([0,0,0])
instructionsrect = instructions.get_rect(center = (650, 350))

trackframes = 0
tracknorm = []
trackinfect = []
trackrecover = []
trackdead = []

people = []

isrunning = True
while isrunning:
    screen.fill([100, 100, 100])
    pygame.display.set_caption("COVID 19 SIM")
    if simstate == "start":
        classes.text(650, 45, 400, 100, "ViralX Virus Sim", [255,255,255], screen)

        classes.text(1050, 150, 200, 25, f"Population = {POPULATION}", [0,0,0], screen)
        popslider.update(screen)
        classes.text(1050, 250, 200, 25, f"Incubation Time = {INCUBE}", [0,0,0], screen)
        incubeslider.update(screen)
        classes.text(1050, 350, 200, 25, f"Infection Time = {INFECT}", [0,0,0], screen)
        infectslider.update(screen)
        classes.text(1050, 450, 200, 25, f"Vaccination Rate = {VACCINATED}", [0,0,0], screen)
        vacslider.update(screen)

        POPULATION = round(popslider.findvalue(10, 300))
        INCUBE = incubeslider.findvalue(1, 10)
        INFECT = infectslider.findvalue(1, 40)
        VACCINATED = vacslider.findvalue(0, 1)

        classes.text(1125, 550, 200, 25, f"Disease Presets", [0,0,0], screen)
        covidbutton.update(screen)
        tbbutton.update(screen)
        rhinobutton.update(screen)
        measlesbutton.update(screen)

        if covidbutton.checkcollisions():
            incubeslider.rect.centerx = 1028
            infectslider.rect.centerx = 1050
            rateslider.rect.centerx = 1033
            distslider.rect.centerx = 1033
            surviveslider.rect.centerx = 1096
        if tbbutton.checkcollisions():
            incubeslider.rect.centerx = 1100
            infectslider.rect.centerx = 1088
            rateslider.rect.centerx = 1011
            distslider.rect.centerx = 1031
            surviveslider.rect.centerx = 1090
        if rhinobutton.checkcollisions():
            incubeslider.rect.centerx = 1006
            infectslider.rect.centerx = 1028
            rateslider.rect.centerx = 1025
            distslider.rect.centerx = 1050
            surviveslider.rect.centerx = 1099
        if measlesbutton.checkcollisions():
            incubeslider.rect.centerx = 1058
            infectslider.rect.centerx = 1063
            rateslider.rect.centerx = 1090
            distslider.rect.centerx = 1100
            surviveslider.rect.centerx = 1097

        classes.text(750, 450, 200, 25, "Press SPACE to continue", [0,0,0], screen)
        classes.text(750, 550, 200, 25, "Press P to pause", [0,0,0], screen)
        classes.text(750, 650, 200, 25, "Press I for instructions", [0,0,0], screen)

        if pygame.key.get_just_pressed()[pygame.K_i]:
            showinstructions = not showinstructions
        if showinstructions:
            pygame.draw.rect(screen, [50, 50, 50], instructionsrect)
            screen.blit(instructions, instructionsrect)
        if pygame.key.get_just_pressed()[pygame.K_SPACE]:
            for i in range(POPULATION):
                people.append(classes.Person(random.randint(10, 640), random.randint(10, 690), 15, 1, random.randint(1, 360), "normal", INCUBE, INFECT))
            for i in range(math.floor(POPULATION * VACCINATED)):
                people[i].state = "recovered"
            people[0].state = "infected"
            simstate = "sim"

    if simstate == "sim":
        for person in people:
            if paused:
                person.render(screen)
            else:
                person.update(screen, people, INFECTIONDIST, RATE, SURVIVAL, QUARANTINE)

        classes.text(1050, 50, 150, 50, "Control Panel", [0,0,0], screen)

        startbutton.update(screen)
        infectbutton.update(screen)
        resetbutton.update(screen)
        if startbutton.checkcollisions():
            paused = False
        if infectbutton.checkcollisions():
            for person in people:
                if person.state == "normal":
                    person.state = "infected"
                    break
        if resetbutton.checkcollisions():
            trackframes = 0
            tracknorm = []
            trackinfect = []
            trackrecover = []
            trackdead = []

            people = []
            for i in range(POPULATION):
                people.append(classes.Person(random.randint(10, 640), random.randint(10, 690), 15, 1, random.randint(1, 360), "normal", INCUBE, INFECT))
            for i in range(math.floor(POPULATION * VACCINATED)):
                people[i].state = "recovered"
            people[0].state = "infected"

        classes.text(1050, 150, 200, 25, f"Infection Rate = {RATE}", [0,0,0], screen)
        rateslider.update(screen)
        classes.text(1050, 250, 200, 25, f"Infection Distance = {INFECTIONDIST}", [0,0,0], screen)
        distslider.update(screen)
        classes.text(1050, 350, 200, 25, f"Survival Rate = {SURVIVAL}", [0,0,0], screen)
        surviveslider.update(screen)
        classes.text(1050, 450, 220, 25, f"Quarantine Distance = {QUARANTINE}", [0,0,0], screen)
        qslider.update(screen)

        RATE = rateslider.findvalue(0, 1)
        INFECTIONDIST = distslider.findvalue(0, 50)
        SURVIVAL = surviveslider.findvalue(0, 1)
        QUARANTINE = qslider.findvalue(0, 50)

        if pygame.key.get_just_pressed()[pygame.K_p]:
            paused = not paused

        if trackinfect != []:
            if trackinfect[-1] == 0:
                classes.text(825, 650, 300, 25, "Press SPACE to Analyse Data", [0, 0, 0], screen)
                if pygame.key.get_just_pressed()[pygame.K_SPACE]:
                    simstate = "analysis"
                    totalseconds = len(tracknorm)
                    normpoints = []
                    infectpoints = []
                    recoverpoints = []
                    deadpoints = []
                    for i in range(totalseconds):
                        pointx = pygame.math.lerp(167, 567, i / totalseconds)
                        pointy = pygame.math.lerp(367, 176, tracknorm[i] / POPULATION)
                        normpoints.append([pointx, pointy])
                    for i in range(totalseconds):
                        pointx = pygame.math.lerp(167, 567, i / totalseconds)
                        pointy = pygame.math.lerp(367, 176, trackinfect[i] / POPULATION)
                        infectpoints.append([pointx, pointy])
                    for i in range(totalseconds):
                        pointx = pygame.math.lerp(167, 567, i / totalseconds)
                        pointy = pygame.math.lerp(367, 176, trackrecover[i] / POPULATION)
                        recoverpoints.append([pointx, pointy])
                    for i in range(totalseconds):
                        pointx = pygame.math.lerp(167, 567, i / totalseconds)
                        pointy = pygame.math.lerp(367, 176, trackdead[i] / POPULATION)
                        deadpoints.append([pointx, pointy])
        if pygame.key.get_just_pressed()[pygame.K_1]:
            simstate = "analysis"
            totalseconds = len(tracknorm)
            normpoints = []
            infectpoints = []
            recoverpoints = []
            deadpoints = []
            for i in range(totalseconds):
                pointx = pygame.math.lerp(167, 567, i / totalseconds)
                pointy = pygame.math.lerp(367, 176, tracknorm[i] / POPULATION)
                normpoints.append([pointx, pointy])
            for i in range(totalseconds):
                pointx = pygame.math.lerp(167, 567, i / totalseconds)
                pointy = pygame.math.lerp(367, 176, trackinfect[i] / POPULATION)
                infectpoints.append([pointx, pointy])
            for i in range(totalseconds):
                pointx = pygame.math.lerp(167, 567, i / totalseconds)
                pointy = pygame.math.lerp(367, 176, trackrecover[i] / POPULATION)
                recoverpoints.append([pointx, pointy])
            for i in range(totalseconds):
                pointx = pygame.math.lerp(167, 567, i / totalseconds)
                pointy = pygame.math.lerp(367, 176, trackdead[i] / POPULATION)
                deadpoints.append([pointx, pointy])

        #TRACK FOR ANALYSIS
        if trackframes == 0 and not paused:
            norm = 0
            infect = 0
            recover = 0
            dead = 0
            for person in people:
                if person.state == "normal":
                    norm += 1
                elif person.state == "infected":
                    infect += 1
                elif person.state == "recovered":
                    recover += 1
                elif person.state == "dead":
                    dead += 1
            tracknorm.append(norm)
            trackinfect.append(infect)
            trackrecover.append(recover)
            trackdead.append(dead)
        if not paused:
            trackframes += 1
        trackframes = trackframes % 60

    if simstate == "analysis":
        screen.blit(dataanalysis, [0,0])
        classes.text(650, 50, 500, 100, "Data Analysis", [0,0,0], screen)
        #UI SCALES
        classes.text(49, 331, 36, 25, round(POPULATION * 0.25), [0,0,0], screen)
        classes.text(49, 278, 36, 25, round(POPULATION * 0.5), [0,0,0], screen)
        classes.text(49, 224, 36, 25, round(POPULATION * 0.75), [0,0,0], screen)
        classes.text(49, 176, 36, 25, POPULATION, [0,0,0], screen)

        classes.text(229, 437, 36, 25, round(totalseconds * 0.25), [0,0,0], screen)
        classes.text(350, 437, 36, 25, round(totalseconds * 0.5), [0,0,0], screen)
        classes.text(459, 437, 36, 25, round(totalseconds * 0.75), [0,0,0], screen)
        classes.text(567, 437, 36, 25, totalseconds, [0,0,0], screen)

        #DRAW LINE GRAPH
        pygame.draw.lines(screen, [255,255,255], False, normpoints, 4)
        pygame.draw.lines(screen, [0,150,0], False, infectpoints, 4)
        pygame.draw.lines(screen, [0,255,255], False, recoverpoints, 4)
        pygame.draw.lines(screen, [150,0,0], False, deadpoints, 4)

        #DRAW SLIDER + BAR
        timeslider.update(screen)
        sliderx = timeslider.findvalue(167, 568)
        longrect = pygame.rect.Rect(0, 0, 3, 325)
        longrect.centerx = sliderx
        longrect.centery = 255
        pygame.draw.rect(screen, [0,0,0], longrect)
        slidertime = math.floor(timeslider.findvalue(0, totalseconds - 1))

        #TEXTUI
        classes.text(489, 491, 72, 25, f"{tracknorm[slidertime]}={round(tracknorm[slidertime] / POPULATION * 100)}%", [0,0,0], screen)
        classes.text(384, 547, 72, 25, f"{trackinfect[slidertime]}={round(trackinfect[slidertime] / POPULATION * 100)}%", [0,0,0], screen)
        classes.text(456, 601, 72, 25, f"{trackrecover[slidertime]}={round(trackrecover[slidertime] / POPULATION * 100)}%", [0,0,0], screen)
        classes.text(247, 657, 72, 25, f"{trackdead[slidertime]}={round(trackdead[slidertime] / POPULATION * 100)}%", [0,0,0], screen)
        classes.text(1237, 671, 125, 25, f"Days = {slidertime}", [0,0,0], screen)


        #PIE CHART
        normangle = 360 * tracknorm[slidertime] / POPULATION
        infangle = normangle + 360 * trackinfect[slidertime] / POPULATION
        recangle = infangle + 360 * trackrecover[slidertime] / POPULATION
        for i in range(360):
            dx = math.cos(math.radians(i)) * 200 + 993
            dy = -math.sin(math.radians(i)) * 200 + 373
            if i <= normangle:
                pygame.draw.line(screen, [255,255,255], [993, 373], [dx, dy], 6)
            elif i <= infangle:
                pygame.draw.line(screen, [0,150,0], [993, 373], [dx, dy], 6)
            elif i <= recangle:
                pygame.draw.line(screen, [0,255,255], [993, 373], [dx, dy], 6)
            else:
                pygame.draw.line(screen, [150,0,0], [993, 373], [dx, dy], 6)

    if pygame.key.get_just_pressed()[pygame.K_w]:
        mouse = pygame.mouse.get_pos()
        print(mouse)

            #print("rate", slider.rect.centerx)

    #HANDLE AT ALL TIMES
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isrunning = False
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
