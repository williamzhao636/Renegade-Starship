'''
Andrew ID: wzhao3

Displays buttons, images, and other popups to the screen
'''

import pygame
import random
import os
import math

def displayPlayerHealths(screen, data):
    healthFont = pygame.font.Font(None, 24)
    white = (255, 255, 255)
    pos = pygame.mouse.get_pos()
    mouseX, mouseY = pos[0], pos[1]
    for item in data.player.itemsGroup:
        mapMouseX = mouseX - data.scrollX
        mapMouseY = mouseY - data.scrollY
        if item.rect.collidepoint(mapMouseX, mapMouseY):
            textString = 'Item Health: %s' % (item.health)
            textDimensions = healthFont.size(textString)
            width, height = textDimensions[0], textDimensions[1]
            text = healthFont.render(textString, True, white)
            screen.blit(text, [mouseX - width/2, mouseY - height])

def displayEnemyHealths(screen, data):
    healthFont = pygame.font.Font(None, 24)
    white = (255, 255, 255)
    pos = pygame.mouse.get_pos()
    mouseX, mouseY = pos[0], pos[1]
    for enemy in data.enemiesGroup:
        for row in range(len(enemy.layout)):
            for col in range(len(enemy.layout[0])):
                item = enemy.layout[row][col]
                if item != None:
                    mapMouseX = mouseX - data.scrollX
                    mapMouseY = mouseY - data.scrollY
                    if item.rect.collidepoint(mapMouseX, mapMouseY):
                        textString = 'Item Health: %s' % (item.health)
                        textDimensions = healthFont.size(textString)
                        width, height = textDimensions[0], textDimensions[1]
                        text = healthFont.render(textString, True, white)
                        screen.blit(text, [mouseX - width/2, mouseY - height])

def displayDroppedItemHealths(screen, data):
    healthFont = pygame.font.Font(None, 24)
    white = (255, 255, 255)
    pos = pygame.mouse.get_pos()
    mouseX, mouseY = pos[0], pos[1]
    for item in data.droppedItemsGroup:
        mapMouseX = mouseX - data.scrollX
        mapMouseY = mouseY - data.scrollY
        if item.rect.collidepoint(mapMouseX, mapMouseY):
            textString = 'Item Health: %s' % (item.health)
            textDimensions = healthFont.size(textString)
            width, height = textDimensions[0], textDimensions[1]
            text = healthFont.render(textString, True, white)
            screen.blit(text, [mouseX - width/2, mouseY - height])

def mouseDisplay(screen, data):
    displayPlayerHealths(screen, data)
    displayEnemyHealths(screen, data)
    displayDroppedItemHealths(screen, data)


def displayTitle(screen, data):
    startMenuTitleFont = pygame.font.Font(None, 80)
    color = (130, 63, 6)
    textString = "Renegade Starship"
    textDimensions = startMenuTitleFont.size(textString)
    width, height = textDimensions[0], textDimensions[1]
    text = startMenuTitleFont.render(textString, True, color)
    screen.blit(text, [data.width/2 - width/2, 2*height])

def displayStartMenuButtons(screen, data):
    backgroundColor = (132, 92, 5)
    outlineColor = (140, 140, 140)

    background = data.startMenuInstructionButton.copy()
    background.inflate_ip(40, 170)
    background.move_ip(0, 55)
    outline = background.copy()
    outline.inflate_ip(20, 20)

    pygame.draw.rect(screen, outlineColor, outline)
    pygame.draw.rect(screen, backgroundColor, background)



    color = (13, 63, 163)
    pygame.draw.rect(screen, color, data.startMenuInstructionButton)
    pygame.draw.rect(screen, color, data.startMenuStartButton)

    screen.blit(data.instructionText, data.instructionsTextRect)
    screen.blit(data.startGameText, data.startGameRect)

def displayInstructionStartButton(screen, data):
    outlineColor = (140, 140, 140)
    background = pygame.Rect(data.width/12, data.height/12,
        10*data.width/12, 10*data.height/12)
    outline = background.copy()
    outline.inflate_ip(20, 20)
    backgroundColor = (173, 153, 123)
    pygame.draw.rect(screen, outlineColor, outline)
    pygame.draw.rect(screen, backgroundColor, background)

    color = (13, 63, 163)
    pygame.draw.rect(screen, color, data.instructionStartButton)
    screen.blit(data.instructStartText, data.instructStartTextRect)

def displayInstructionTitle(screen, data):
    instructionTitleFont = pygame.font.Font(None, 50)
    white = (255, 255, 255)
    textString = "Instructions"
    textDimensions = instructionTitleFont.size(textString)
    width, height = textDimensions[0], textDimensions[1]
    text = instructionTitleFont.render(textString, True, white)
    screen.blit(text, [data.width/2 - width/2, 3*height])

def displayInstructions(screen, data):
    instructionFont = pygame.font.Font(None, 30)
    white = (255, 255, 255)
    instructionList =   [   "You are in control of a ship whose objective is to reach the destination shown",
                            "by the arrow while fighting against waves of never ending enemies.",
                            " ",
                            "Up - Accelerate Forward",
                            "Down - Accelerate Backward",
                            "Left - Rotate Left",
                            "Right - Rotate Right",
                            "Space - Shoot",
                            "Escape - Quit",
                            "P - Pause",
                            "S - Save Current Ship",
                            "L - Load Saved Ship",
                            " ",
                            "Defeated enemies drop their parts which can be dragged to attach to you ship.",
                            "You can also drag parts on your ship to customize it.",
                            "Be careful not to detach everything though!",
                            "And watch out for running into enemies; you wouldn't want to cause an engine failure...."
                        ]
    for i in range(len(instructionList)):
        displayText = instructionList[i]
        textDimensions = instructionFont.size(displayText)
        width, height = textDimensions[0], textDimensions[1]
        text = instructionFont.render(displayText, True, white)
        height = instructionFont.get_height()
        screen.blit(text, [data.width/6, 5*data.height/24 + height*i])

def displayGameOver(screen, data):
    color = (13, 63, 163)
    pygame.draw.rect(screen, color, data.restartButton)
    screen.blit(data.restartText, data.restartRect)


    background = data.gameOverRect.copy()
    background.inflate_ip(40, 40)
    outline = background.copy()
    outline.inflate_ip(20, 20)

    outlineColor = (140, 140, 140)
    pygame.draw.rect(screen, outlineColor, outline)
    backgroundColor = (119, 95, 38)
    pygame.draw.rect(screen, backgroundColor, background)

    screen.blit(data.gameOverText, data.gameOverRect)

def displaySaveConfirmation(screen, data):
    backgroundColor = (173, 153, 123)
    background = pygame.Rect(data.width/4, data.height/4,
        data.width/2, data.height/2)
    outlineColor = (140, 140, 140)
    outline = background.copy()
    outline.inflate_ip(20, 20)
    pygame.draw.rect(screen, outlineColor, outline)
    pygame.draw.rect(screen, backgroundColor, background)

    buttonColor = (13, 63, 163)
    white = (255, 255, 255)
    saveConfirmationFont = pygame.font.Font(None, 40)
    textList =  [   'Are you sure you',
                    'want to overwrite',
                    'your current save?'
                ]

    for i in range(len(textList)):
        text = textList[i]
        textDimensions = saveConfirmationFont.size(text)
        width, height = textDimensions[0], textDimensions[1]
        text = saveConfirmationFont.render(text, True, white)

        textX = data.width/2 - width/2
        textY = data.height/4 + (3 + i)*height
        textRect = pygame.Rect(textX, textY, width, height)
        screen.blit(text, textRect)

    pygame.draw.rect(screen, buttonColor, data.yesButton)
    pygame.draw.rect(screen, buttonColor, data.noButton)

    screen.blit(data.yesText, data.yesTextRect)
    screen.blit(data.noText, data.noTextRect)

def displayLoadConfirmation(screen, data):
    backgroundColor = (173, 153, 123)
    background = pygame.Rect(data.width/4, data.height/4,
        data.width/2, data.height/2)
    outlineColor = (140, 140, 140)
    outline = background.copy()
    outline.inflate_ip(20, 20)
    pygame.draw.rect(screen, outlineColor, outline)
    pygame.draw.rect(screen, backgroundColor, background)

    buttonColor = (13, 63, 163)
    white = (255, 255, 255)
    loadConfirmationFont = pygame.font.Font(None, 40)
    textList =  [   'You are about to replace',
                    'your current layout with',
                    'a saved one.',
                    ' ',
                    'Are you sure?',
                ]

    for i in range(len(textList)):
        text = textList[i]
        textDimensions = loadConfirmationFont.size(text)
        width, height = textDimensions[0], textDimensions[1]
        text = loadConfirmationFont.render(text, True, white)

        textX = data.width/2 - width/2
        textY = data.height/4 + (3 + i)*height
        textRect = pygame.Rect(textX, textY, width, height)
        screen.blit(text, textRect)

    pygame.draw.rect(screen, buttonColor, data.yesButton)
    pygame.draw.rect(screen, buttonColor, data.noButton)

    screen.blit(data.yesText, data.yesTextRect)
    screen.blit(data.noText, data.noTextRect)

def displayObjectiveArrow(screen, data):
    targetX, targetY = data.targetLocation
    yDistance = data.player.commandModuleY - targetY
    xDistance = data.player.commandModuleX - targetX
    angle = -math.degrees(math.atan2((yDistance), (xDistance))) + 180

    if 45 < angle < 135:
        newY = 40
        newX = data.width/2 + data.width/2*math.cos(math.radians(angle))
    elif 135 < angle < 225:
        newX = 40
        newY = data.height/2 + -data.height/2*math.sin(math.radians(angle))
    elif 225 < angle < 315:
        newY = data.height - 40
        newX = data.width/2 + data.width/2*math.cos(math.radians(angle))
    else:
        newX = data.width - 40
        newY = data.height/2 + -data.height/2*math.sin(math.radians(angle))


    w, h = data.arrowImage.get_size()
    newRect = pygame.Rect(newX, newY, w, h)

    image = pygame.transform.rotate(data.arrowImage, angle)
    screen.blit(image, newRect)


def displayObjectiveCoords(screen, data):
    objectiveCoordFont = pygame.font.Font(None, 30)
    white = (255, 255, 255)
    currXY = (int(data.player.commandModuleX), int(data.player.commandModuleY))
    textList =  [   "Target Location: " + str(data.targetLocation),
                    "Current Location: " + str(currXY)
                ]

    for i in range(len(textList)):
        text = textList[i]
        textDimensions = objectiveCoordFont.size(text)
        width, height = textDimensions[0], textDimensions[1]
        text = objectiveCoordFont.render(text, True, white)

        textX = data.width/2 - width/2
        textY = (1 + i)*height
        textRect = pygame.Rect(textX, textY, width, height)
        screen.blit(text, textRect)



def displayWinScreen(screen, data):
    color = (13, 63, 163)
    pygame.draw.rect(screen, color, data.restartButton)
    screen.blit(data.restartText, data.restartRect)

    winScreenFont = pygame.font.Font(None, 60)
    white = (255, 255, 255)
    textString = "You Win!"
    textDimensions = winScreenFont.size(textString)
    width, height = textDimensions[0], textDimensions[1]
    text = winScreenFont.render(textString, True, white)

    textX = data.width/2 - width/2
    textY = 5*height
    textRect = pygame.Rect(textX, textY, width, height)


    background = textRect.copy()
    background.inflate_ip(40, 40)
    outline = background.copy()
    outline.inflate_ip(20, 20)

    outlineColor = (140, 140, 140)
    pygame.draw.rect(screen, outlineColor, outline)
    backgroundColor = (119, 95, 38)
    pygame.draw.rect(screen, backgroundColor, background)



    screen.blit(text, textRect)



def displayCrime(screen, data):
    crimeFont = pygame.font.Font(None, 26)
    white = (255, 255, 255)
    textString = str(data.crimeShips[data.crimeLevel])
    textDimensions = crimeFont.size(textString)
    width, height = textDimensions[0], textDimensions[1]
    text = crimeFont.render(textString, True, white)
    screen.blit(text, [data.width - 1.5*width, height])


def displayStarMap(screen, data):
    for star in data.starGroup:
        star.draw(screen, data)
