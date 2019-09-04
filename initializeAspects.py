'''
Andrew ID: wzhao3

Sets up buttons, the player's ships and other one time called functions
'''

import pygame
import random

from Classes import objects
from Classes import ships
'''
All item image templates from https://captainforever.fandom.com/wiki/Main_Page
along with some custom created item images.
Star images taken from earthsky.org and nasa.gov.
Arrow image is from canva.com.
'''
def initObjectImages():
    objects.CommandModule.init()
    objects.AlphaBulkhead.init()
    objects.BravoBulkhead.init()
    objects.CharlieBulkhead.init()
    objects.DeltaBulkhead.init()
    objects.LaserGun.init()
    objects.RedStar.init()
    objects.WhiteStar.init()
    objects.PurpleStar.init()
    objects.RocketLauncher.init()
    objects.Rocket.init()


def initPlayerShip(data):
    height = objects.AlphaBulkhead.height
    command = objects.CommandModule(data.width/2, data.height/2)
    top = objects.AlphaBulkhead(data.width/2, data.height/2 - height)
    botBulkhead = objects.AlphaBulkhead(data.width/2, data.height/2 + height)
    right = objects.AlphaBulkhead(data.width/2 + 40, data.height/2)
    left = objects.AlphaBulkhead(data.width/2 - 40, data.height/2)
    rocketLauncher1 = objects.RocketLauncher(data.width/2,
        data.height/2 - 2*height, 90, 20)
    laserGun1 = objects.LaserGun(data.width/2 - 40, data.height/2 - height,
        90, 10)
    laserGun2 = objects.LaserGun(data.width/2 + 40, data.height/2 - height,
        90, 10)
    laserGun3 = objects.LaserGun(data.width/2, data.height/2 + height, 270, 60)
    layout =    [   [None, None, None, None, None],
                    [None, None, rocketLauncher1, None, None],
                    [None, laserGun1, top, laserGun2, None],
                    [None, left, command, right, None],
                    [None, None, laserGun3, None, None],
                    [None, None, None, None, None]
                ]
    connections =   [   [None, None, None, None, None],
                        [None, None, "DOWN", None, None],
                        [None, "DOWN", "DOWN", "DOWN", None],
                        [None, "RIGHT", 'CM', "LEFT", None],
                        [None, None, "UP", None, None],
                        [None, None, None, None, None]
                    ]
    data.player = ships.PlayerShip(command.x, command.y, layout, connections)

def initStarMap(data):
    data.starGroup = pygame.sprite.Group()
    data.filledX = [-data.width, 2*data.width]
    data.filledY = [-data.height, 2*data.height]
    for i in range(-data.height, 2*data.height, int(data.height/4)):
        for j in range(-data.width, 2*data.width, int(data.width/4)):
            randX = random.randint(j, j + int(data.width/4))
            randY = random.randint(i, i + int(data.height/4))
            starChoice = random.choice([1, 2, 3])

            if starChoice == 1:
                newStar = objects.RedStar(randX, randY)
            elif starChoice == 2:
                newStar = objects.WhiteStar(randX, randY)
            elif starChoice == 3:
                newStar = objects.PurpleStar(randX, randY)
            data.starGroup.add(newStar)

def initSaveConfirmationButton(data):
    white = (255, 255, 255)
    saveConfirmationFont = pygame.font.Font(None, 40)
    yesText = 'Yes'
    data.yesText = saveConfirmationFont.render(yesText, True, white)
    textDimensions = saveConfirmationFont.size(yesText)
    width, height = textDimensions[0], textDimensions[1]
    textX = data.width/2 - 3*width + width/4
    textY = data.height/2 + 3*height + height/2
    data.yesTextRect = pygame.Rect(textX, textY, width, height)
    yesButtonX = data.width/2 - 3*width
    yesButtonY = data.height/2 + 3*height
    data.yesButton = pygame.Rect(yesButtonX, yesButtonY, 1.5*width, 2*height)

    textDimensions = saveConfirmationFont.size(yesText)
    yesWidth, yesHeight = textDimensions[0], textDimensions[1]
    noButtonX = data.width/2 + 1.5*yesWidth
    noButtonY = data.height/2 + 3*yesHeight
    data.noButton = pygame.Rect(noButtonX, noButtonY, 1.5*yesWidth, 2*yesHeight)

    noText = 'No'
    data.noText = saveConfirmationFont.render(noText, True, white)
    textDimensions = saveConfirmationFont.size(noText)
    width, height = textDimensions[0], textDimensions[1]
    textX = data.width/2 + 1.5*yesWidth + width/2
    textY = data.height/2 + 3*yesHeight + height/2
    data.noTextRect = pygame.Rect(textX, textY, width, height)

def initGameOver(data):
    white = (255, 255, 255)
    gameOverFont = pygame.font.Font(None, 80)
    textString = "Game Over"
    textDimensions = gameOverFont.size(textString)
    width, height = textDimensions[0], textDimensions[1]
    data.gameOverText = gameOverFont.render(textString, True, white)
    rectX = data.width/2 - width/2
    rectY = height
    data.gameOverRect = pygame.Rect(rectX, rectY, width, height)

    restartButtonFont = pygame.font.Font(None, 40)
    textString = 'Restart'
    data.restartText = restartButtonFont.render(textString, True, white)
    textDimensions = restartButtonFont.size(textString)
    width, height = textDimensions[0], textDimensions[1]
    textX = data.width/2 - width/2
    textY = data.height - 7*height
    data.restartRect = pygame.Rect(textX, textY, width, height)
    buttonX = textX - width/4
    buttonY = textY - height
    data.restartButton = pygame.Rect(buttonX, buttonY,
        1.5*width, 3*height)

def initInstrctionStartButton(data):
    white = (255, 255, 255)
    startButtonFont = pygame.font.Font(None, 40)
    textString = 'Start Game'
    data.instructStartText = startButtonFont.render(textString, True, white)
    textDimensions = startButtonFont.size(textString)
    width, height = textDimensions[0], textDimensions[1]
    textX = data.width/2 - width/2
    textY = data.height - 6*height
    data.instructStartTextRect = pygame.Rect(textX, textY, width, height)
    buttonX = textX - width/4
    buttonY = textY - height
    data.instructionStartButton = pygame.Rect(buttonX, buttonY,
        1.5*width, 3*height)

def initStartMenuButtons(data):
    white = (255, 255, 255)
    StartMenuButtonsFont = pygame.font.Font(None, 40)

    textString = 'Instructions'
    data.instructionText = StartMenuButtonsFont.render(textString, True, white)
    textDimensions = StartMenuButtonsFont.size(textString)
    longWidth, height = textDimensions[0], textDimensions[1]
    textX = data.width/2 - longWidth/2
    textY = data.height - 9*height
    data.instructionsTextRect = pygame.Rect(textX, textY, longWidth, height)
    buttonX = textX - longWidth/4
    buttonY = textY - height
    data.startMenuInstructionButton = pygame.Rect(buttonX, buttonY,
        1.5*longWidth, 3*height)


    textString = 'Start Game'
    data.startGameText = StartMenuButtonsFont.render(textString, True, white)
    textDimensions = StartMenuButtonsFont.size(textString)
    width, height = textDimensions[0], textDimensions[1]
    textX = data.width/2 - width/2
    textY = data.height - 5*height
    data.startGameRect = pygame.Rect(textX, textY, width, height)
    buttonY = textY - height
    data.startMenuStartButton = pygame.Rect(buttonX, buttonY,
        1.5*longWidth, 3*height)

def initStartMenuFlyByShip(data):
    startX = 5*data.width/4
    startY = 3*data.height/8
    top = objects.AlphaBulkhead(startX, startY - 40)
    bot = objects.AlphaBulkhead(startX, startY + 40)
    right = objects.AlphaBulkhead(startX + 40, startY)
    left = objects.AlphaBulkhead(startX - 40, startY)
    command = objects.CommandModule(startX, startY)
    laserGun1 = objects.LaserGun(startX - 80, startY, 90, 10)
    laserGun2 = objects.LaserGun(startX + 80, startY, 270, 10)
    laserGun3 = objects.LaserGun(startX, startY - 80, 0, 10)
    layout =    [   [None, None, None, None, None, None, None],
                    [None, None, None, laserGun3, None, None, None],
                    [None, None, None, top, None, None, None],
                    [None, laserGun1, left, command, right, laserGun2, None],
                    [None, None, None, bot, None, None, None],
                    [None, None, None, None, None, None, None]
                ]
    connection =   [   [None, None, None, None, None, None, None],
                        [None, None, None, "DOWN", None, None, None],
                        [None, None, None, "DOWN", None, None, None],
                        [None, "RIGHT", "RIGHT", 'CM', "LEFT", "LEFT", None],
                        [None, None, None, "UP", None, None, None],
                        [None, None, None, None, None, None, None]
                    ]
    data.flyByShip = ships.PlayerShip(command.x, command.y, layout, connection)
    data.flyByShip.forwardAccelerate = True
    data.flyByShip.isShooting = True
    data.flyByShip.speed = -data.flyByShip.maxSpeed
    data.flyByShip.angle = -90
    data.flyByShip.rotateHelper(data, 0)


