from GameEngine import *
import random
from _thread import *
import threading
import asyncio

# I am so sorry that this code is garbage I rushed it in a week
# Also I am sorry about comments just run it don't read it

# Constants that are probably needed
width = 1080
height = round((width / 16) * 9)

sunTotal = 400
zombieHealth = 100
plantHealth = 150
zombiesSpawning = [30]
zombieCount = [30]

engine = GameEngine(width=width, height=height)


def loadupAnimationFromFile(filename):
    file1 = open(filename, "r")
    zombieAnimation = file1.readlines()
    zombieAnimation2 = []
    for i in zombieAnimation:
        zombieAnimation2.append(i.replace("\n", ""))
    file1.close()
    return zombieAnimation2


engine.setWindowIcon("resources/graphics/logo.gif")
engine.setTitle("Plants vs Zombies v2")
engine.setResizable(False)
engine.setBackgroundColor("light blue")

canvas = Canvas(engine.main, width=width, height=height)
canvas.pack()

tile = Tilemap(-(width / 2) + 50, -(height / 2) + 150, canvas, rows=7, collumns=4)
tile.draw()
tile.hide()
tiles = tile.rectangles

bg_image = canvas.create_background(
    0,
    0,
    "resources/graphics/Items/Background/Background_0.gif",
    width=width,
    height=height,
)

SunText = canvas.create_text(450, -250, text="Sun: {}".format(sunTotal))
sunImg = canvas.create_image(
    385,
    -250,
    "resources/graphics/Plants/Sun/Sun_0.png",
    width=50,
    height=50,
    collisionMesh="misc",
)

# Animations Loading from file
zombieAnimation2 = loadupAnimationFromFile("Zombie-ZombieAttack.txt")
zombieAnimation3 = loadupAnimationFromFile("Zombie-Zombie.txt")
zombieAnimation4 = loadupAnimationFromFile("Zombie-ZombieDie.txt")
peaShooterAnimation = loadupAnimationFromFile("Peashooter.txt")
sunFlowerAnimation = loadupAnimationFromFile("SunFlower.txt")
repeaterPeaAnimation = loadupAnimationFromFile("RepeaterPea.txt")
wallNutAnimation = loadupAnimationFromFile("WallNut-WallNut.txt")
potatoMine1 = loadupAnimationFromFile("PotatoMine-PotatoMine.txt")
potatoMine2 = loadupAnimationFromFile("PotatoMine-PotatoMineInit.txt")
potatoMine3 = loadupAnimationFromFile("PotatoMine-PotatoMineExplode.txt")
sunAnimation = loadupAnimationFromFile("Sun.txt")

# The predetermined Animations
sun = canvas.animateImage(sunImg, 100, sunAnimation)


# The cards for creating objects
canvas.create_rectangle(0, (height / 2) - 50, (width), 100)
peaShooter = canvas.create_image(
    (-width / 2) + 100,
    (height / 2) - 50,
    "resources/graphics/Cards/card_peashooter.png",
    width=75,
    height=100,
    radius=2,
    collisionMesh="cards",
)
sunFlower = canvas.create_image(
    (-width / 2) + 200,
    (height / 2) - 50,
    "resources/graphics/Cards/card_sunflower.png",
    width=75,
    height=100,
    radius=2,
    collisionMesh="cards",
)

repeaterPea = canvas.create_image(
    (-width / 2) + 300,
    (height / 2) - 50,
    "resources/graphics/Cards/card_repeaterpea.png",
    width=75,
    height=100,
    radius=2,
    collisionMesh="cards",
)
wallObj = canvas.create_image(
    (-width / 2) + 400,
    (height / 2) - 50,
    "resources/graphics/Cards/card_wallnut.png",
    width=75,
    height=100,
    radius=2,
    collisionMesh="cards",
)
potatoMineObj = canvas.create_image(
    (-width / 2) + 500,
    (height / 2) - 50,
    "resources/graphics/Cards/card_potatomine.png",
    width=75,
    height=100,
    radius=2,
    collisionMesh="cards",
)

# Handling the exit button
def closeWindow():
    engine.stopSound()
    engine.remove()
    exit()



# Winning or losing
once = True
def finale(win):
    global once
    if once == True:
        answer = "are a failure!"
        if win == True:
            answer = "WON!"
        else:
            answer = "LOST"
        engine.createText(text="You {}".format(answer), font=("Courier", 50)).pack()
        engine.createButton(
            text="Exit Game!", command=closeWindow, font=("Courier", 40)
        ).pack()
        once = False


doZombie = [[True, 100]]
zombiesPerLine = [0, 0, 0, 0]
doPeaShoot = [True]
chosenPeaShoot = 0

## I don't even know what happened here
def __peaShoot(item, peaShootNumb):
    global chosenPeaShoot
    global zombieCount
    global doPeaShoot
    global sunTotal
    global zombiesPerLine
    if doPeaShoot[peaShootNumb] == True:
        if canvas.getLocation(item)[0] >= width:
            canvas.delete(item)
        else:
            c = canvas.collision(item)
            if c[0] == False:
                canvas.move(10, 0, item)
                engine.delay(50, lambda: __peaShoot(item, peaShootNumb))
            else:
                canvas.delete(item)
                if c[1].getHealth() <= 0:
                    canvas.removeFromCollision(c[1])
                    canvas.delete(c[1])
                    sunTotal += 20
                    canvas.updateText([SunText], text="Sun: {}".format(sunTotal))
                    zombiesPerLine[item.getLineNum()] -= 1
                    zombieCount[0] -= 1
                    if zombieCount[0] <= 0:
                        finale(True)
                        canvas.stopAllAnimations()
                        l = 0
                        for i in doPeaShoot:
                            doPeaShoot[l] = False
                            l += 1
                        l = 0
                        for i in doSun:
                            doSun[l] = False
                            l += 1
                        canvas.hide()
                else:
                    health = canvas.items[c[2]].getHealth()
                    canvas.items[c[2]].setHealth(health - 20)
    else:
        canvas.delete(item)


def peaShootCreateBullet(peaShootNumb, x, y, speed, item2):
    bullet = canvas.create_image(
        x,
        y - 20,
        "resources/graphics/Bullets/PeaNormal/PeaNormal_0.png",
        width=50,
        height=50,
        radius=20,
        player=True,
    )
    item = bullet
    item.setLineNum(item2.getLineNum())
    canvas.canvas.update()
    engine.delay(5, __peaShoot(item, peaShootNumb))
    __peaShootTimer(peaShootNumb, x, y, speed, item2)


def __peaShootTimer(peaShootNumb, x, y, speed, item):
    global chosenPeaShoot
    global doPeaShoot
    global zombiesPerLine
    if doPeaShoot[peaShootNumb] == True:
        if zombiesPerLine[item.getLineNum()] > 0:
            randomInteger = random.randint(1000, 5000)
            if speed == "FAST":
                randomInteger = random.randint(333, 1666)
            engine.delay(
                randomInteger,
                lambda: peaShootCreateBullet(peaShootNumb, x, y, speed, item),
            )
        else:
            engine.delay(100, lambda: __peaShootTimer(peaShootNumb, x, y, speed, item))


# Ability Definitions
def peaShoot(item, x, y, speed, chosenAnimation):
    global doPeaShoot
    x -= width / 2
    y -= height / 2
    item[0].setRadius(50)
    item[0].setAbilityNum(doPeaShoot[-1])
    item[0].setAbilityVar("PEASHOOT")
    if y == -154:
        item[0].setLineNum(0)
    elif y == -54:
        item[0].setLineNum(1)
    elif y == 46:
        item[0].setLineNum(2)
    elif y == 146:
        item[0].setLineNum(3)
    engine.delay(5, lambda: __peaShootTimer(doPeaShoot[-1], x, y, speed, item[0]))
    doPeaShoot.append(True)


doSun = [True]
chosenOne = 0


def __makeSun(doingSun, item):
    global doSun
    global sunTotal
    if doSun[doingSun] == True:
        randomInteger = random.randint(1000, 10000)
        sunTotal += 10
        canvas.updateText([SunText], text="Sun: {}".format(sunTotal))
        engine.delay(randomInteger, lambda: __makeSun(doingSun, item))


def makeSun(item, x, y, objectType, chosenAnimation):
    global chosenOne
    item[0].setRadius(50)
    item[0].setAbilityNum(chosenOne)
    item[0].setAbilityVar("SUN")
    randomInteger = random.randint(2000, 20000)
    engine.delay(randomInteger, lambda: __makeSun(chosenOne, item))
    chosenOne += 1
    doSun.append(True)


def wall(item, x, y, objectType, chosenAnimation):
    item[0].setRadius(50)
    item[0].setHealth(500)
    item[0].setAbilityVar("WALL")
    item[0].setAbilityNum(0)


potatoMineRun = [True]


def potatoMineCheck(item, chosenAnimation, chosenINDEX):
    global potatoMineRun
    c = canvas.collision(item)
    if potatoMineRun[chosenINDEX] == True:
        if c[0] == True:
            canvas.stopAnimation(chosenAnimation)
            canvas.animateImage(item, 100, potatoMine3)
            potatoMineRun[chosenINDEX] = False
            canvas.delete(item)
            canvas.delete(c[1])
        else:
            engine.delay(
                50, lambda: potatoMineCheck(item, chosenAnimation, chosenINDEX)
            )


def potatoMineLoaded(item, chosenAnimation, chosenINDEX):
    canvas.stopAnimation(chosenAnimation)
    canvas.animateImage(item, 200, potatoMine1)
    item.setRadius(80)
    potatoMineCheck(item, chosenAnimation, chosenINDEX)


def potatoMine(item, x, y, objectType, chosenAnimation):
    global potatoMineRun
    item = item[0]
    item.setRadius(1)
    item.setHealth(100)
    item.setAbilityVar("POTATOMINE")
    item.setAbilityNum(0)
    engine.delay(
        1000, lambda: potatoMineLoaded(item, chosenAnimation, potatoMineRun[-1])
    )
    potatoMineRun.append(True)


## Zombie Creation System
chosenZombie = 0

zombiesSpawned = 0


def zombieRun(item, animation, ZombieOne):
    c = canvas.collision(item, tag="plants")
    if c[0] == True:
        canvas.stopAnimation(animation)
        animation = canvas.animateImage(item, 100, zombieAnimation2)
        health = c[1].getHealth()
        c[1].setHealth(health - 20)
        if health <= 0:
            var = c[1].getAbilityVar()
            if var == "SUN":
                doSun[c[1].getAbilityNum()] = False
            elif var == "PEASHOOT":
                doPeaShoot[c[1].getAbilityNum()] = False
            canvas.delete(c[1])
            canvas.stopAnimation(animation)
            animation = canvas.animateImage(item, 100, zombieAnimation3)
        engine.delay(
            (len(zombieAnimation2) - 1) * 100,
            lambda: zombieRun(item, animation, ZombieOne),
        )
    else:
        if doZombie[ZombieOne][0] == True:
            if c[0] == False:
                if canvas.getLocation(item)[0] <= 50:
                    if canvas.getLocation(item) != (0, 0):
                        finale(False)
                        canvas.stopAllAnimations()
                        l = 0
                        for i in doPeaShoot:
                            doPeaShoot[l] = False
                            l += 1
                        l = 0
                        for i in doSun:
                            doSun[l] = False
                            l += 1
                        canvas.hide()
                        # engine.delay(50,canvas.destroy())
                else:
                    canvas.move(-2, 0, item)
                    engine.delay(50, lambda: zombieRun(item, animation, ZombieOne))


def zombieCreate(x, y, ZombieOne, collumnPick):
    global zombiesSpawned
    global zombiesPerLine
    if zombiesSpawned < zombiesSpawning[0]:
        zombiesSpawned += 1
        zomb = canvas.create_image(
            x,
            y,
            "resources/graphics/Zombies/NormalZombie/Zombie/Zombie_0.png",
            width=150,
            height=100,
            radius=20,
            player=False,
        )
        zomb.setLineNum(collumnPick)
        zombiesPerLine[collumnPick] += 1
        ani = canvas.animateImage(zomb, 50, zombieAnimation3)
        engine.delay(50, zombieRun(zomb, ani, ZombieOne))
        engine.delay(50, zombieTimer(ZombieOne))


def zombieTimer(ZombieOne):
    global doZombie
    if doZombie[ZombieOne][0] == True:
        randomInteger = random.randint(1000, 10000)
        x = 500
        collumnPick = random.randint(0, 3)
        y = -185 + (collumnPick * 100)
        engine.delay(randomInteger, lambda: zombieCreate(x, y, ZombieOne, collumnPick))


def zombieSpawn():
    global chosenZombie
    global doZombie
    engine.delay(5, lambda: zombieTimer(chosenZombie))
    chosenZombie += 1
    doZombie.append([True, 100])


##Plant System
clickables = [peaShooter, sunFlower, repeaterPea, wallObj, potatoMineObj]
objectPath = [
    "resources/graphics/Plants/Peashooter/Peashooter_0.png",
    "resources\graphics\Plants\SunFlower\SunFlower_0.png",
    "resources/graphics/Plants/RepeaterPea/RepeaterPea_0.png",
    "resources/graphics/Plants/WallNut/WallNut/WallNut_0.png",
    "resources/graphics/Plants/PotatoMine/PotatoMineInit/PotatoMineInit_0.png",
]
animationPath = [
    peaShooterAnimation,
    sunFlowerAnimation,
    repeaterPeaAnimation,
    wallNutAnimation,
    potatoMine2,
]
sunCost = [100, 50, 200, 50, 25]
abilities = [peaShoot, makeSun, peaShoot, wall, potatoMine]
TYPE = ["NORMAL", "NORMAL", "FAST", "NORMAL", "NORMAL"]
SIZE = [[100, 100], [100, 100], [100, 100], [80, 100], [100, 80]]
meshType = ["plants", "plants", "plants", "plants", "mines"]
zombie = True
paused = False
## Setup the frame here
frame = Frame(engine.main)
b1 = engine.createButton(text="Exit Game!", command=closeWindow, font=("Courier", 40))

def pauseMenu(e):
    global paused
    global frame
    global b1
    if paused == False:
        canvas.hide()
        frame.pack()
        b1.pack()
        paused = True
    else:
        canvas.pack()
        frame.hide()
        b1.pack_forget()
        paused = False


# Collision detection
colliders = []


def updateFunction():
    global colliders
    for i in colliders:
        if canvas.collision(i):
            canvas.delete(i)


following = False
followingItem = None
tile = Tilemap(-(width / 2) + 50, -(height / 2) + 150, canvas, rows=7, collumns=4)
tile.draw()
tile.hide()
tiles = tile.rectangles
usedTiles = [False] * len(tiles)


def mouseMove(e):
    global following
    global followingItem
    if following == True:
        if followingItem != None:
            canvas.followMouse(followingItem, e.x, e.y)


sunPlaceCost = 0
abilityChosen = 0
chosenAnimation = 0


def click(e):
    global following, followingItem, tiles, sunTotal, sunPlaceCost, abilityChosen, usedTiles, TYPE, SIZE, meshType, chosenAnimation
    x = e.x
    y = e.y
    foundItem = False
    for g in range(len(clickables)):
        a, b, c, d = canvas.bbox(clickables[g])
        if engine.boundCheck(x, y, a, b, c, d):
            following = True
            if followingItem == None:
                sunPlaceCost = sunCost[g]
                if sunTotal >= sunPlaceCost:
                    plant = canvas.create_image(
                        0,
                        0,
                        objectPath[g],
                        width=SIZE[g][0],
                        height=SIZE[g][1],
                        collisionMesh=meshType[g],
                    )
                    chosenAnimation = canvas.animateImage(plant, 100, animationPath[g])
                    sunPlaceCost = sunCost[g]
                    abilityChosen = g
                    followingItem = plant
                    foundItem = True
                    canvas.followMouse(followingItem, e.x, e.y)
    if foundItem == False:
        if followingItem != None:
            l = 0
            for i in tiles:
                if usedTiles[l] == False:
                    t = Item(i)
                    a, b, c, d = canvas.bbox(t)
                    if engine.boundCheck(x, y, a, b, c, d):
                        x, y = canvas.getLocation(t)
                        x += 50
                        y += 50
                        canvas.followMouse(followingItem, x, y)
                        sunTotal -= sunPlaceCost
                        abilities[abilityChosen](
                            [followingItem], x, y, TYPE[abilityChosen], chosenAnimation
                        )
                        canvas.updateText([SunText], text="Sun: {}".format(sunTotal))
                        followingItem = None
                        usedTiles[l] = True
                l += 1


# Management stuff
engine.playSound("resources\music\Plants vs Zombies.wav")
engine.input(pauseMenu, keyType="ESCAPE")
engine.protocol("WindowClose", closeWindow)
engine.input(click, keyType="LEFTCLICK")
engine.input(mouseMove, keyType="MOUSEMOVE")

zombieSpawn()

engine.run()
