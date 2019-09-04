'''
Andrew ID: wzhao3

Handles game events including key pressed, mouse pressed, timer fired, etc.
'''
import pygame
import math
import os
import pickle

from Classes import objects
from spawnEnemies import *
from display import *
from initializeAspects import *


def distance(x1, x2, y1, y2):
    distance = ((x1 - x2)**2 + (y1 - y2)**2)**0.5
    return distance

#Sets the currently moved item x and y to mouse x and y
def movePieces(data):
    pos = pygame.mouse.get_pos()
    mouseX, mouseY = pos[0], pos[1]
    if data.movingPiece:
        item = data.movingItem
        item.x, item.y = mouseX - data.scrollX, mouseY - data.scrollY
        item.coord = (mouseX - data.scrollX, mouseY - data.scrollY)
        item.update(0, 0)


def findCommandRowCol(layout):
    for row in range(len(layout)):
        for col in range(len(layout[0])):
            item = layout[row][col]
            if isinstance(item, objects.CommandModule):
                commandRow = row
                commandCol = col
    return commandRow, commandCol

#Adds extra rows or cols to player layout and returns direction of new item
def updatePlayerLayoutAndConnections(positions, data):
    prevRow, prevCol, newRow, newCol = positions

    if newRow > prevRow:
        data.player.connections[newRow][newCol] = 'UP'
        data.player.layout.append( [None] * len(data.player.layout[0]) )
        data.player.connections.append( [None] * len(data.player.layout[0]) )
    if newRow < prevRow:
        data.player.connections[newRow][newCol] = 'DOWN'
        data.player.layout.insert(0, [None] * len(data.player.layout[0]) )
        data.player.connections.insert(0, [None] * len(data.player.layout[0]) )
    if newCol > prevCol:
        data.player.connections[newRow][newCol] = 'LEFT'
        for row in data.player.layout:
            row.append(None)
        for row in data.player.connections:
            row.append(None)
    if newCol < prevCol:
        data.player.connections[newRow][newCol] = 'RIGHT'
        for row in data.player.layout:
            row.insert(0, None)
        for row in data.player.connections:
            row.insert(0, None)

#Finds the attach direction
def getDirection(positions):
    prevRow, prevCol, newRow, newCol = positions
    if newRow > prevRow:
        return 'UP'
    if newRow < prevRow:
        return 'DOWN'
    if newCol > prevCol:
        return 'LEFT'
    if newCol < prevCol:
        return 'RIGHT'

#Creates a list of item indices are False and empty is True
def createVisitedItemsList(data):
    rows = len(data.player.layout)
    cols = len(data.player.layout[0])
    visitedItems = [ ([True] * cols) for row in range(rows) ]
    for row in range(len(data.player.layout)):
        for col in range(len(data.player.layout[0])):
            item = data.player.layout[row][col]
            if item != None:
                visitedItems[row][col] = False
    return visitedItems



#Find shortest diagonal to empty square but still within attach range
def findAttachPosition(attachDict):
    attachRange = 50
    bestDist = -1
    newPos = 0
    newCoords = 0

    for key in attachDict:
        if attachDict[key][0] < attachRange:
            if attachDict[key][1] < bestDist or bestDist == -1:
                bestDist = attachDict[key][1]
                newPos = key
                newCoords = attachDict[key][2]
    return (bestDist, newPos, newCoords)

#Sets the attaching items attributes according to its new location
def setItemAttributes(item, position, coords, data):
    prevRow, prevCol, newRow, newCol = position
    #find commandModule row and col
    commandRow, commandCol = findCommandRowCol(data.player.layout)
    #Set position of new item according to command module row and col
    colDiff = newCol - commandCol
    rowDiff = newRow - commandRow
    newX = data.player.commandModuleX + colDiff*40
    newY = data.player.commandModuleY + rowDiff*40

    item.coord = (newX, newY)
    item.x, item.y = coords

    if isinstance(item, objects.Shooter):
        direction = getDirection(position)
        if direction == 'LEFT':
            item.angle = data.player.angle + 0
        if direction == 'DOWN':
            item.angle = data.player.angle + 90
        if direction == 'RIGHT':
            item.angle = data.player.angle + 180
        if direction == 'UP':
            item.angle = data.player.angle + 270

#Checks if the item can be attached to the player
def checkItemAttach(droppedItem, data):
    playerCommandRow, playerCommandCol = findCommandRowCol(data.player.layout)
    rows, cols = len(data.player.layout), len(data.player.layout[0])
    visitedItems = createVisitedItemsList(data)
    attachDistancesDict = dict()

    findClosestSlot(droppedItem, data, playerCommandRow, playerCommandCol,
        playerCommandRow, playerCommandCol, visitedItems, attachDistancesDict)
    bestDist, newPos, newCoords = findAttachPosition(attachDistancesDict)

    if bestDist != -1:
        prevRow, prevCol, newRow, newCol = newPos
        prevItem = data.player.layout[prevRow][prevCol]
        #Can't add items connected to LaserGuns
        if isinstance(prevItem, objects.Shooter):
            return
        setItemAttributes(droppedItem, newPos, newCoords, data)

        #Add item to player layout and remove from dropped items group
        data.player.layout[newRow][newCol] = droppedItem

        updatePlayerLayoutAndConnections(newPos, data)
        data.player.itemsGroup.add(droppedItem)
        data.droppedItemsGroup.remove(droppedItem)
        data.player.rotateHelper(data, 0)

#Finds all possible attach locations for the dropped item
def findClosestSlot(droppedItem, data, row, col, prevRow, prevCol, visitedItems, attachDict):
    item = data.player.layout[row][col]
    visited = visitedItems[row][col]
    #Loop through all items to see if item can fit in available spots
    if item == None:
        #Find the distance from dropped item to prev item
        prevItem = data.player.layout[prevRow][prevCol]
        if isinstance(prevItem, objects.Shooter):
            return
        itemsDist = distance(droppedItem.x, prevItem.x,
            droppedItem.y, prevItem.y)

        #Find the coords of where the new item would be
        rowDiff = row - prevRow
        colDiff = col - prevCol
        changeX, changeY = colDiff*40, rowDiff*40

        newCoordX = prevItem.coord[0] + changeX
        newCoordY = prevItem.coord[1] + changeY

        #find new itemx and y based on player angle
        xDistance = newCoordX - data.player.commandModuleX
        yDistance = -(newCoordY - data.player.commandModuleY)
        angle = math.degrees(math.atan2((yDistance), (xDistance)))

        diagonal = distance(data.player.commandModuleX, newCoordX,
                            data.player.commandModuleY, newCoordY)
        dx = diagonal*math.cos(math.radians(data.player.angle + angle))
        dy = -diagonal*math.sin(math.radians(data.player.angle + angle))

        newX = data.player.commandModuleX + dx
        newY = data.player.commandModuleY + dy
        newCoords = (newCoordX, newCoordY)

        #Find the distance from the dropped item to the new item slot
        droppedDist = distance(newX, droppedItem.x, newY, droppedItem.y)
        value = (itemsDist, droppedDist, newCoords)
        attachDict[(prevRow, prevCol, row, col)] = value

    elif visited == True:
        return
    else:
        visitedItems[row][col] = True
        #Branch out to find linked items
        findClosestSlot(droppedItem, data, row, col - 1, row, col,
            visitedItems, attachDict)
        findClosestSlot(droppedItem, data, row, col + 1, row, col,
            visitedItems, attachDict)
        findClosestSlot(droppedItem, data, row - 1, col, row, col,
            visitedItems, attachDict)
        findClosestSlot(droppedItem, data, row + 1, col, row, col,
            visitedItems, attachDict)


#Extends the star background when the player reaches the edge
def addStarMap(data):
    xLow, xHigh = data.filledX[0], data.filledX[1]
    yLow, yHigh = data.filledY[0], data.filledY[1]
    #Adds stars to the left
    if xLow + data.width > data.player.commandModuleX:
        prevLow = xLow
        xLow -= data.width
        generateNewStars(xLow, prevLow, yLow, yHigh, data)
        data.filledX[0] = xLow
    #Add stars to the right
    elif data.player.commandModuleX > xHigh - data.width:
        prevHigh = xHigh
        xHigh += data.width
        generateNewStars(prevHigh, xHigh, yLow, yHigh, data)
        data.filledX[1] = xHigh
    #Adds stars above
    if yLow + data.height > data.player.commandModuleY:
        prevLow = yLow
        yLow -= data.height
        generateNewStars(xLow, xHigh, yLow, prevLow, data)
        data.filledY[0] = yLow
    #Add stars below
    elif data.player.commandModuleY > yHigh - data.height:
        prevHigh = yHigh
        yHigh += data.height
        generateNewStars(xLow, xHigh, prevHigh, yHigh, data)
        data.filledY[1] = yHigh


def generateNewStars(xLow, xHigh, yLow, yHigh, data):
    for i in range(yLow, yHigh, int(data.height/4)):
        for j in range(xLow, xHigh, int(data.width/4)):
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

def gameOverTextFall(data):
    lowerBound = data.height/2
    if not data.gameOverRect.collidepoint(data.width/2, lowerBound):
        data.gameOverRect.move_ip(0, 5)

#Wraps the start menu ship when it reaches the edge of the screen
def wrapFlyByShip(data):
    for row in range(len(data.flyByShip.layout)):
        for col in range(len(data.flyByShip.layout[0])):
            item = data.flyByShip.layout[row][col]
            if item != None:
                item.x %= 3*data.width/2


def getCommandRowCol(layout):
    for row in range(len(layout)):
        for col in range(len(layout[0])):
            item = layout[row][col]
            if item == 'CM':
                commandRow = row
                commandCol = col
    return commandRow, commandCol

#Saves the current player layout into a text file
def savePlayerLayout(data):
    rows = len(data.player.layout)
    cols = len(data.player.layout[0])
    layout = [[None for i in range(cols)] for i in range(rows)]
    for row in range(len(data.player.layout)):
        for col in range(len(data.player.layout[row])):
            item = data.player.layout[row][col]

            if isinstance(item, objects.CommandModule):
                layout[row][col] = 'CM'
            elif isinstance(item, objects.LaserGun):
                layout[row][col] ="LG"
            elif isinstance(item, objects.RocketLauncher):
                layout[row][col] = "RL"
            elif isinstance(item, objects.AlphaBulkhead):
                layout[row][col] = "A"
            elif isinstance(item, objects.BravoBulkhead):
                layout[row][col] = "B"
            elif isinstance(item, objects.CharlieBulkhead):
                layout[row][col] = "C"
            elif isinstance(item, objects.CharlieBulkhead):
                layout[row][col] = "D"
    fileObject = open('Saves.txt', 'wb')
    savePackage = (layout, data.player.connections)
    pickle.dump(savePackage, fileObject)

#Checks to see if the player clicked on a dropped item
def checkMovingDroppedItem(data):
    pos = pygame.mouse.get_pos()
    mouseX, mouseY = pos[0], pos[1]
    mapMouseX = mouseX - data.scrollX
    mapMouseY = mouseY - data.scrollY
    for item in data.droppedItemsGroup:
        if item.rect.collidepoint(mapMouseX, mapMouseY):
            data.movingPiece = True
            data.movingItem = item

#Checks to see if the player clicked on a item on their own ship
def checkMovingPlayerItem(data):
    pos = pygame.mouse.get_pos()
    mouseX, mouseY = pos[0], pos[1]
    mapMouseX = mouseX - data.scrollX
    mapMouseY = mouseY - data.scrollY
    for row in range(len(data.player.layout)):
        for col in range(len(data.player.layout[0])):
            item = data.player.layout[row][col]
            if item != None and not isinstance(item, objects.CommandModule):
                if item.rect.collidepoint(mapMouseX, mapMouseY):
                    data.movingPiece = True
                    data.movingItem = item
                    removeAttachedItems(data, row, col)

#If there are items attached to the current moving item, drop them
def removeAttachedItems(data, row, col):
    item = data.player.layout[row][col]
    if item == None:
        return
    else:
        #item that was just destroyed
        data.player.itemsGroup.remove(item)
        data.droppedItemsGroup.add(item)
        data.player.layout[row][col] = None
        data.player.connections[row][col] = None
        #Branch out to find linked items
        if data.player.connections[row][col - 1] == 'RIGHT':
            removeAttachedItems(data, row, col - 1)
        if data.player.connections[row][col + 1] == 'LEFT':
            removeAttachedItems(data, row, col + 1)
        if data.player.connections[row - 1][col] == 'DOWN':
            removeAttachedItems(data, row - 1, col)
        if data.player.connections[row + 1][col] == 'UP':
            removeAttachedItems(data, row + 1, col)

#Checks to see if the player is within range of the objective location
#Increases difficuly as player approaches the objective
def checkWinStatus(data):
    targetX, targetY = data.targetLocation
    totalDist = distance(data.width/2, targetX, data.height/2, targetY)
    if abs(data.player.commandModuleX - targetX) < data.width/6 and \
            abs(data.player.commandModuleY - targetY) < data.height/6:
        data.mode = data.modes[7]
    elif distance(data.player.commandModuleX, targetX,
            data.player.commandModuleY, targetY) < totalDist/4:
        data.crimeLevel = 4
        data.maxEnemies = 7
        data.enemySpawnInterval = 50
        despawnEnemies(data, 1.2*data.width)
    elif distance(data.player.commandModuleX, targetX,
            data.player.commandModuleY, targetY) < totalDist/3 and \
            data.crimeLevel < 3:
        data.crimeLevel = 3
        data.maxEnemies = 5
        data.enemySpawnInterval = 250
        despawnEnemies(data, 2*data.width)
    elif distance(data.player.commandModuleX, targetX,
            data.player.commandModuleY, targetY) < 2*totalDist/3 and \
            data.crimeLevel < 2:
        data.crimeLevel = 2
        data.maxEnemies = 4
        data.enemySpawnInterval = 300
        despawnEnemies(data, 3*data.width)
    else:
        despawnEnemies(data, 4*data.width)

#Loads a new layout for the player from a text file
def loadPlayerLayout(data):
    fileObject = open('Saves.txt', 'rb')
    layout, connections = pickle.load(fileObject)
    startX = data.width/2
    startY = data.height/2
    for enemy in data.enemiesGroup:
        if 0 < enemy.commandModuleX < data.width and \
                0 < enemy.commandModuleY < data.height:
            data.enemiesGroup.remove(enemy)

    commandRow, commandCol = getCommandRowCol(layout)

    for row in range(len(layout)):
        for col in range(len(layout[row])):
            item = layout[row][col]
            rowDiff = row - commandRow
            colDiff = col - commandCol
            changeX, changeY = colDiff*40, rowDiff*40

            itemX = startX + changeX
            itemY = startY + changeY
            if connections[row][col] == 'DOWN':
                angle = 90
            elif connections[row][col] == 'UP':
                angle = 270
            elif connections[row][col] == 'LEFT':
                angle = 0
            elif connections[row][col] == 'RIGHT':
                angle = 180

            if item == 'CM':
                layout[row][col] = objects.CommandModule(startX, startY)
            if item == 'LG':
                layout[row][col] = objects.LaserGun(itemX, itemY, angle, 10)
            if item == 'RL':
                layout[row][col] = objects.RocketLauncher(itemX, itemY,
                    angle, 20)
            if item == 'A':
                layout[row][col] = objects.AlphaBulkhead(itemX, itemY)
            if item == 'B':
                layout[row][col] = objects.BravoBulkhead(itemX, itemY)
            if item == 'C':
                layout[row][col] = objects.CharlieBulkhead(itemX, itemY)
            if item == 'D':
                layout[row][col] = objects.CharlieBulkhead(itemX, itemY)
    data.player = ships.PlayerShip(startX, startY, layout, connections)
    data.scrollX = 0
    data.scrollY = 0

def despawnEnemies(data, removeDist):
    for enemy in data.enemiesGroup:
        if distance(enemy.commandModuleX, data.player.commandModuleX,
                enemy.commandModuleY, data.player.commandModuleY) > removeDist:
            data.enemiesGroup.remove(enemy)



def init(data):
    data.timer = 0
    data.movingPiece = False
    data.movingItem = None
    data.maxEnemies = 2
    data.enemySpawnInterval = 350
    data.scrollX = 0
    data.scrollY = 0
    targetX = random.choice([7*data.width, -7*data.width])
    targetY = random.choice([7*data.height, -7*data.height])
    data.targetLocation = (targetX, targetY)
    data.arrowImage = pygame.transform.scale(
            pygame.image.load(os.path.join('Objects',
            'Arrow.png')).convert_alpha(), (30, 30))
    data.modes = ['START MENU', 'INSTRUCTION', 'PLAYING', 'GAME OVER',
        'PAUSED', 'SAVE SCREEN', 'LOAD SCREEN', 'WIN SCREEN']
    data.mode = data.modes[0]
    data.crimeLevel = 0
    data.crimeShips = ["Alpha", "Bravo", "Charlie", "Delta", "Delta", "Delta"]
    data.obstacleGroup = pygame.sprite.Group()
    data.enemiesGroup = pygame.sprite.Group()
    data.droppedItemsGroup = pygame.sprite.Group()
    initObjectImages()
    initStartMenuFlyByShip(data)
    initStartMenuButtons(data)
    initInstrctionStartButton(data)
    initSaveConfirmationButton(data)
    initGameOver(data)
    initStarMap(data)
    initPlayerShip(data)


def keyPressed(event, data):
    if data.mode == 'PLAYING':
        playingKeyPressed(event, data)

def keyReleased(event, data):
    if data.mode == 'PLAYING':
        playingKeyReleased(event, data)
    elif data.mode == 'PAUSED':
        pausedKeyReleased(event, data)

def mousePressed(data):
    if data.mode == 'PLAYING':
        playingMousePressed(data)
    elif data.mode == 'INSTRUCTION':
        instructionMousePressed(data)
    elif data.mode == 'START MENU':
        startMenuMousePressed(data)
    elif data.mode == 'GAME OVER':
        gameOverMousePressed(data)
    elif data.mode == 'SAVE SCREEN':
        saveScreenMousePressed(data)
    elif data.mode == 'LOAD SCREEN':
        loadScreenMousePressed(data)
    elif data.mode == 'WIN SCREEN':
        winScreenMousePressed(data)

def mouseReleased(data):
    if data.mode == 'PLAYING':
        playingMouseReleased(data)

def mouseMoved(data):
    if data.mode == 'PLAYING':
        playingMouseMoved(data)

def timerFired(data):
    if data.mode == 'PLAYING':
        playingTimerFired(data)
    elif data.mode == 'GAME OVER':
        gameOverTimerFired(data)
    elif data.mode == 'START MENU':
        startMenuTimerFired(data)

def redrawAll(screen, data):
    if data.mode == 'START MENU':
        startMenuRedrawAll(screen, data)
    elif data.mode == 'PLAYING':
        playingRedrawAll(screen, data)
    elif data.mode == 'INSTRUCTION':
        instructionRedrawAll(screen, data)
    elif data.mode == 'GAME OVER':
        gameOverRedrawAll(screen, data)
    elif data.mode == 'PAUSED':
        playingRedrawAll(screen, data)
    elif data.mode == 'SAVE SCREEN':
        saveScreenRedrawAll(screen, data)
    elif data.mode == 'LOAD SCREEN':
        loadScreenRedrawAll(screen, data)
    elif data.mode == 'WIN SCREEN':
        winScreenRedrawAll(screen, data)


def winScreenRedrawAll(screen, data):
    displayWinScreen(screen, data)

def winScreenMousePressed(data):
    pos = pygame.mouse.get_pos()
    mouseX, mouseY = pos[0], pos[1]
    if data.restartButton.collidepoint(mouseX, mouseY):
        init(data)
        data.mode = data.modes[0]


def loadScreenRedrawAll(screen, data):
    playingRedrawAll(screen, data)
    displayLoadConfirmation(screen, data)

def loadScreenMousePressed(data):
    pos = pygame.mouse.get_pos()
    mouseX, mouseY = pos[0], pos[1]
    if data.yesButton.collidepoint(mouseX, mouseY):
        loadPlayerLayout(data)
        data.mode = data.modes[2]
    if data.noButton.collidepoint(mouseX, mouseY):
        data.mode = data.modes[2]




def saveScreenRedrawAll(screen, data):
    playingRedrawAll(screen, data)
    displaySaveConfirmation(screen, data)

def saveScreenMousePressed(data):
    pos = pygame.mouse.get_pos()
    mouseX, mouseY = pos[0], pos[1]
    if data.yesButton.collidepoint(mouseX, mouseY):
        savePlayerLayout(data)
        data.mode = data.modes[2]
    if data.noButton.collidepoint(mouseX, mouseY):
        data.mode = data.modes[2]


def startMenuRedrawAll(screen, data):
    displayStarMap(screen, data)
    data.flyByShip.draw(screen, data)
    for laser in data.flyByShip.laserGroup:
        laser.draw(screen, data)
    for rocket in data.flyByShip.rocketGroup:
        rocket.draw(screen, data)
    displayTitle(screen, data)
    displayStartMenuButtons(screen, data)

def startMenuMousePressed(data):
    pos = pygame.mouse.get_pos()
    mouseX, mouseY = pos[0], pos[1]
    if data.startMenuInstructionButton.collidepoint(mouseX, mouseY):
        data.mode = data.modes[1]
    if data.startMenuStartButton.collidepoint(mouseX, mouseY):
        data.mode = data.modes[2]

def startMenuTimerFired(data):
    data.flyByShip.laserGroup.update(data)
    data.flyByShip.rocketGroup.update(data)
    data.flyByShip.update(data)
    wrapFlyByShip(data)


def pausedKeyReleased(event, data):
    if event.key == pygame.K_p:
        data.mode = data.modes[2]

def gameOverRedrawAll(screen, data):
    displayGameOver(screen, data)

def gameOverTimerFired(data):
    gameOverTextFall(data)

def gameOverMousePressed(data):
    pos = pygame.mouse.get_pos()
    mouseX, mouseY = pos[0], pos[1]
    if data.restartButton.collidepoint(mouseX, mouseY):
        init(data)
        data.mode = data.modes[0]


def instructionRedrawAll(screen, data):
    displayInstructionStartButton(screen, data)
    displayInstructions(screen, data)
    displayInstructionTitle(screen, data)


def instructionMousePressed(data):
    pos = pygame.mouse.get_pos()
    mouseX, mouseY = pos[0], pos[1]
    if data.instructionStartButton.collidepoint(mouseX, mouseY):
        data.mode = data.modes[2]

def playingRedrawAll(screen, data):
    displayStarMap(screen, data)
    for part in data.droppedItemsGroup:
        part.draw(screen, data)
    displayCrime(screen, data)
    displayObjectiveCoords(screen, data)
    for obstacle in data.obstacleGroup:
        obstacle.draw(screen)
    for laser in data.player.laserGroup:
        laser.draw(screen, data)
    for rocket in data.player.rocketGroup:
        rocket.draw(screen, data)
    data.player.draw(screen, data)
    for enemy in data.enemiesGroup:
        for laser in enemy.laserGroup:
            laser.draw(screen, data)
        for rocket in enemy.rocketGroup:
            rocket.draw(screen, data)
        enemy.draw(screen, data)
    mouseDisplay(screen, data)
    displayObjectiveArrow(screen, data)

def playingKeyPressed(event, data):
    if event.key == pygame.K_LEFT:
        data.player.rotateLeft()
    if event.key == pygame.K_RIGHT:
        data.player.rotateRight()
    if event.key == pygame.K_UP:
        data.player.accelerateForward()
    if event.key == pygame.K_DOWN:
        data.player.accelerateBackward()
    if event.key == pygame.K_SPACE:
        data.player.shooting()
    if event.key == pygame.K_s:
        data.mode = data.modes[5]
    if event.key == pygame.K_l:
        data.mode = data.modes[6]



def playingKeyReleased(event, data):
    if event.key == pygame.K_UP:
        data.player.decelerateForward()
    if event.key == pygame.K_DOWN:
        data.player.decelerateBackward()
    if event.key == pygame.K_SPACE:
        data.player.stopShooting()
    if event.key == pygame.K_LEFT:
        data.player.stopTurningLeft()
    if event.key == pygame.K_RIGHT:
        data.player.stopTurningRight()
    if event.key == pygame.K_p:
        data.mode = data.modes[4]

def playingMousePressed(data):
    checkMovingDroppedItem(data)
    checkMovingPlayerItem(data)


def playingMouseReleased(data):
    item = data.movingItem
    if data.movingPiece:
        checkItemAttach(item, data)
    data.movingPiece = False

def playingMouseMoved(data):
    movePieces(data)

def playingTimerFired(data):
    addStarMap(data)
    if data.timer % data.enemySpawnInterval == 0:
        spawnEnemy(data)
    data.player.laserGroup.update(data)
    data.player.rocketGroup.update(data)
    data.player.update(data)

    for enemy in data.enemiesGroup:
        enemy.laserGroup.update(data)
        enemy.rocketGroup.update(data)
    data.enemiesGroup.update(data)
    checkWinStatus(data)

