'''
Andrew ID: wzhao3

Code for the two types of starships, enemies and the player.
'''



import pygame
import math

from Classes import objects


def distance(x1, x2, y1, y2):
    distance = ((x1 - x2)**2 + (y1 - y2)**2)**0.5
    return distance


#Main ship class for player and enemy ships
class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, layout, connections):
        super().__init__()
        self.commandModuleX = x
        self.commandModuleY = y
        self.angle = 0
        self.layout = layout
        self.connections = connections
        self.laserGroup = pygame.sprite.Group()
        self.rocketGroup = pygame.sprite.Group()
        self.initItemsGroup()


    #Adds all items in layout to personal item group
    def initItemsGroup(self):
        self.itemsGroup = pygame.sprite.Group()
        for row in self.layout:
            for item in row:
                if item != None:
                    self.itemsGroup.add(item)

    def draw(self, screen, data):
        for item in self.itemsGroup:
            item.draw(screen, data)

    def doRotate(self, item):
        xDistance = item.coord[0] - self.commandModuleX
        yDistance = -(item.coord[1] - self.commandModuleY)
        angle = math.degrees(math.atan2((yDistance), (xDistance)))

        diagonal = distance(self.commandModuleX, item.coord[0],
                            self.commandModuleY, item.coord[1])
        dx = diagonal*math.cos(math.radians(self.angle + angle))
        dy = -diagonal*math.sin(math.radians(self.angle + angle))

        item.image = pygame.transform.rotate(item.baseImage, self.angle)
        item.x = self.commandModuleX + dx
        item.y = self.commandModuleY + dy


    def checkCollisions(self, item, data):
        if len(pygame.sprite.spritecollide(item,
                data.obstacleGroup, False)) > 0:
            return True

        if isinstance(self, PlayerShip):
            for enemy in data.enemiesGroup:
                if len(pygame.sprite.spritecollide(item,
                        enemy.itemsGroup, False)) > 0:
                    return True

        if isinstance(self, EnemyShip):
            if len(pygame.sprite.spritecollide(item,
                    data.player.itemsGroup, False)) > 0:
                return True
            # for enemy in data.enemiesGroup:
            #     if self != enemy:
            #         if len(pygame.sprite.spritecollide(item,
            #                 enemy.itemsGroup, False)) > 0:
            #             return True


    def checkMoveCollisions(self, data):
        dy = self.speed*math.cos(math.radians(self.angle))
        dx = self.speed*math.sin(math.radians(self.angle))
        for item in self.itemsGroup:
            item.update(dx, dy)
            collided = self.checkCollisions(item, data)
            item.update(-dx, -dy)
            if collided:
                return True
        return False


    def move(self, data):
        collided = self.checkMoveCollisions(data)
        # collided = False
        if not collided:
            dy = self.speed*math.cos(math.radians(self.angle))
            dx = self.speed*math.sin(math.radians(self.angle))
            for item in self.itemsGroup:
                item.update(dx, dy)
                if isinstance(item, objects.CommandModule):
                    self.commandModuleX += dx
                    self.commandModuleY += dy



    def checkRotationCollisions(self, angleChange, data):
        for item in self.itemsGroup:
            self.angle += angleChange
            self.doRotate(item)
            item.update(0, 0)
            if isinstance(item, objects.LaserGun):
                item.angle += angleChange

            collided = self.checkCollisions(item, data)
            self.angle -= angleChange
            self.doRotate(item)
            if isinstance(item, objects.LaserGun):
                item.angle -= angleChange
            if collided:
                return True
        return False


    def rotateHelper(self, data, angleChange):
        collided = self.checkRotationCollisions(angleChange, data)
        if not collided:
            self.angle += angleChange
            for item in self.itemsGroup:
                self.doRotate(item)
                if isinstance(item, objects.LaserGun) or \
                        isinstance(item, objects.RocketLauncher):
                    item.angle += angleChange


    #Lowers the cooldown of all Shooter type items
    def resetCooldowns(self, data):
        for item in self.itemsGroup:
            if isinstance(item, objects.LaserGun):
                if item.cooldownTimer == 0:
                    item.coolingDown = False
                if item.coolingDown:
                    item.cooldownTimer -= 1
            if isinstance(item, objects.RocketLauncher):
                if item.cooldownTimer == 0:
                    item.coolingDown = False
                if item.coolingDown:
                    item.cooldownTimer -= 1

    #Remove off screen lasers
    def removeProjectiles(self, data):
        for laser in self.laserGroup:
            inScreenX = 0 < laser.x + data.scrollX < data.width
            inScreenY = 0 < laser.y + data.scrollY < data.height
            if not inScreenX or not inScreenY or \
                    laser.currDistance > laser.maxDistance:
                self.laserGroup.remove(laser)
        for rocket in self.rocketGroup:
            inScreenX = 0 < rocket.x + data.scrollX < data.width
            inScreenY = 0 < rocket.y + data.scrollY < data.height
            if not inScreenX or not inScreenY or \
                    rocket.currDistance > rocket.maxDistance:
                self.rocketGroup.remove(rocket)

    #Destroys items with 0 health and items attached to destroyed items
    def destroyLinkedItems(self, sprite, row, col):
        if sprite.layout[row][col] == None:
            return
        else:
            #item that was just destroyed
            sprite.itemsGroup.remove(sprite.layout[row][col])
            sprite.layout[row][col] = None
            sprite.connections[row][col] = None
            #Branch out to find linked items
            if sprite.connections[row][col - 1] == 'RIGHT':
                self.destroyLinkedItems(sprite, row, col - 1)
            if sprite.connections[row][col + 1] == 'LEFT':
                self.destroyLinkedItems(sprite, row, col + 1)
            if sprite.connections[row - 1][col] == 'DOWN':
                self.destroyLinkedItems(sprite, row - 1, col)
            if sprite.connections[row + 1][col] == 'UP':
                self.destroyLinkedItems(sprite, row + 1, col)



class PlayerShip(Ship):
    def __init__(self, x, y, layout, connections):
        super().__init__(x, y, layout, connections)
        self.speed = 0
        self.forwardAccelerate = False
        self.backwardAccelerate = False
        self.turningLeft = False
        self.turningRight = False
        self.isShooting = False
        self.angleChange = 2.5
        self.maxSpeed = 8

    def rotateLeft(self):
        self.turningLeft = True

    def rotateRight(self):
        self.turningRight = True

    def stopTurningLeft(self):
        self.turningLeft = False

    def stopTurningRight(self):
        self.turningRight = False

    def accelerateForward(self):
        self.forwardAccelerate = True

    def accelerateBackward(self):
        self.backwardAccelerate = True

    def decelerateForward(self):
        self.forwardAccelerate = False

    def decelerateBackward(self):
        self.backwardAccelerate = False

    def rotate(self, data):
        if self.turningLeft:
            self.rotateHelper(data, self.angleChange)
        if self.turningRight:
            self.rotateHelper(data, -self.angleChange)

    #Mimics acceleration and deceleration
    def speedControl(self):
        if self.forwardAccelerate and self.speed > -self.maxSpeed:
            self.speed -= 0.3
        if self.backwardAccelerate and self.speed < self.maxSpeed/2:
            self.speed += 0.3
        if not self.forwardAccelerate and not self.backwardAccelerate:
            self.speed *= 0.9
            if -0.1 < self.speed < 0.1:
                self.speed = 0


    #Adds to sidescrolling if at edge of map
    def checkScrolling(self, data):
        collided = self.checkMoveCollisions(data)
        if data.mode == 'PLAYING' and not collided:
            dy = self.speed*math.sin(math.radians(self.angle + 90))
            dx = self.speed*math.cos(math.radians(self.angle + 90))
            data.scrollX += dx
            data.scrollY -= dy


    def update(self, data):
        self.removeProjectiles(data)
        self.resetCooldowns(data)
        self.speedControl()
        self.checkScrolling(data)
        self.rotate(data)
        self.move(data)
        self.shoot()
        self.checkHits(data)

    def shooting(self):
        self.isShooting = True

    def stopShooting(self):
        self.isShooting = False

    def shoot(self):
        if self.isShooting:
            for item in self.itemsGroup:
                if isinstance(item, objects.LaserGun) and not item.coolingDown:
                    item.coolingDown = True
                    item.cooldownTimer = item.cooldown
                    newLaser = objects.PlayerLaser(item.x, item.y,
                        item.angle, item.damage)
                    self.laserGroup.add(newLaser)
                elif isinstance(item, objects.RocketLauncher) and \
                        not item.coolingDown:
                    item.coolingDown = True
                    item.cooldownTimer = item.cooldown
                    magnitude = objects.RocketLauncher.height
                    width = objects.Rocket.width
                    dx = magnitude*math.cos(math.radians(item.angle))
                    dy = -magnitude*math.sin(math.radians(item.angle))
                    dx -= abs(width*math.cos(math.radians(item.angle)))
                    dy += abs(width/2*math.cos(math.radians(item.angle)))
                    newRocket = objects.Rocket(item.x + dx, item.y + dy,
                        item.angle, item.damage)
                    self.rocketGroup.add(newRocket)

    #Checks if any lasers or rockets hit an enemy
    def checkHits(self, data):
        for enemy in data.enemiesGroup:
            for row in range(len(enemy.layout)):
                for col in range(len(enemy.layout[0])):
                    item = enemy.layout[row][col]
                    if item != None:
                        collidedLasers = pygame.sprite.spritecollide(item,
                            data.player.laserGroup, True)
                        collidedRockets = pygame.sprite.spritecollide(item,
                            data.player.rocketGroup, True)
                        if len(collidedLasers) > 0:
                            for laser in collidedLasers:
                                item.health -= laser.damage
                                if isinstance(item, objects.CommandModule) and\
                                        item.health <= 0:
                                    enemy.defeated(data)
                                    break
                                elif item.health <= 0:
                                    self.destroyLinkedItems(enemy, row, col)
                                    break
                        if len(collidedRockets) > 0:
                            for rocket in collidedRockets:
                                item.health -= rocket.damage
                                if isinstance(item, objects.CommandModule) and\
                                        item.health <= 0:
                                    enemy.defeated(data)
                                    break
                                elif item.health <= 0:
                                    self.destroyLinkedItems(enemy, row, col)
                                    break

class EnemyShip(Ship):
    def __init__(self, x, y, layout, connections, level, speed=-2):
        super().__init__(x, y, layout, connections)
        self.speed = speed
        self.maxSpeed = speed
        self.level = level

    #If enemy is defeated, remove from game and drop all items
    def defeated(self, data):
        for item in self.itemsGroup:
            if not isinstance(item, objects.CommandModule):
                data.droppedItemsGroup.add(item)
        self.itemsGroup.empty()
        data.enemiesGroup.remove(self)
        if self.level > data.crimeLevel:
            data.crimeLevel += 1

    #Causes the enemy to rotate towards the player
    def directionFinder(self, data):
        xDistance = self.commandModuleX - data.player.commandModuleX
        yDistance = -(self.commandModuleY - data.player.commandModuleY)
        targetAngle = math.degrees(math.atan2((yDistance), (xDistance))) + 180
        pointDir = self.angle + 90
        pointDir %= 360

        if pointDir - targetAngle < 0 and abs(pointDir - targetAngle) < 180 or\
                360 + targetAngle - pointDir < 180:
            self.rotateHelper(data, 1)
        else:
            self.rotateHelper(data, -1)

    def update(self, data):
        self.removeProjectiles(data)
        self.resetCooldowns(data)
        if data.timer % 2 == 0:
            self.directionFinder(data)
        self.move(data)
        self.shoot(data)
        self.checkHits(data)

    #Only shoots if enemy is relatively pointing towards the player
    def shoot(self, data):
        for item in self.itemsGroup:
            if isinstance(item, objects.LaserGun) and not item.coolingDown:
                item.coolingDown = True
                item.cooldownTimer = item.cooldown
                newLaser = objects.EnemyLaser(item.x, item.y,
                    item.angle, item.damage)
                self.laserGroup.add(newLaser)
            elif isinstance(item, objects.RocketLauncher) and \
                    not item.coolingDown:
                item.coolingDown = True
                item.cooldownTimer = item.cooldown
                magnitude = objects.RocketLauncher.height
                width = objects.Rocket.width
                dx = magnitude*math.cos(math.radians(item.angle))
                dy = -magnitude*math.sin(math.radians(item.angle))
                dx -= abs(width*math.cos(math.radians(item.angle)))
                dy += abs(width/2*math.cos(math.radians(item.angle)))
                newRocket = objects.Rocket(item.x + dx, item.y + dy,
                    item.angle, item.damage, item.speed)
                self.rocketGroup.add(newRocket)


    def checkHits(self, data):
        for row in range(len(data.player.layout)):
            for col in range(len(data.player.layout[0])):
                item = data.player.layout[row][col]
                if item != None:
                    collidedLasers = pygame.sprite.spritecollide(item,
                        self.laserGroup, True)
                    collidedRockets = pygame.sprite.spritecollide(item,
                        self.rocketGroup, True)
                    if len(collidedLasers) > 0:
                        for laser in collidedLasers:
                            item.health -= laser.damage
                            if isinstance(item, objects.CommandModule) and \
                                    item.health <= 0:
                                data.mode = data.modes[3]
                            elif item.health <= 0:
                                self.destroyLinkedItems(data.player, row, col)
                                break
                    if len(collidedRockets) > 0:
                        for rocket in collidedRockets:
                            item.health -= rocket.damage
                            if isinstance(item, objects.CommandModule) and\
                                    item.health <= 0:
                                data.mode = data.modes[3]
                            elif item.health <= 0:
                                self.destroyLinkedItems(data.player, row, col)
                                break


        pygame.sprite.groupcollide(data.player.rocketGroup, self.laserGroup, True, True)

