'''
Andrew ID: wzhao3

Code for all game objects including stars, projectiles, and ship items.
'''

import pygame
import math
import os


def distance(x1, x2, y1, y2):
    distance = ((x1 - x2)**2 + (y1 - y2)**2)**0.5
    return distance

#General game object
class GameObject(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

#Main star class
class Star(GameObject):
    def __init__(self, x, y, image):
        super().__init__()
        self.x = x
        self.y = y
        self.image = image

    def draw(self, screen, data):
        w, h = self.image.get_size()
        itemX = self.x - w/2 + data.scrollX
        itemY = self.y - h/2 + data.scrollY
        newRect = pygame.Rect(itemX, itemY, w, h)
        screen.blit(self.image, newRect)

#Individual classes for each color
class RedStar(Star):
    @staticmethod
    def init():
        RedStar.image = pygame.transform.scale(
            pygame.image.load(os.path.join('Objects', 'Stars',
            'RedStar.jpeg')).convert_alpha(), (10, 10))

    def __init__(self, x, y):
        super().__init__(x, y, RedStar.image)

class WhiteStar(Star):
    @staticmethod
    def init():
        WhiteStar.image = pygame.transform.scale(
            pygame.image.load(os.path.join('Objects', 'Stars',
            'WhiteStar.png')).convert_alpha(), (10, 10))

    def __init__(self, x, y):
        super().__init__(x, y, WhiteStar.image)

class PurpleStar(Star):
    @staticmethod
    def init():
        PurpleStar.image = pygame.transform.scale(
            pygame.image.load(os.path.join('Objects', 'Stars',
            'PurpleStar.png')).convert_alpha(), (10, 10))

    def __init__(self, x, y):
        super().__init__(x, y, PurpleStar.image)


#Main class for all projectiles
class Projectile(GameObject):
    def __init__(self, x, y, angle, damage):
        super().__init__()
        self.x = x
        self.y = y
        self.angle = angle
        self.damage = damage


    def updateRect(self):
        updateX = self.x - self.length/2
        updateY = self.y - self.width/2
        self.rect = pygame.Rect(updateX, updateY, self.length, self.width)

    def update(self, data):
        self.x += self.speed*math.cos(math.radians(self.angle))
        self.y += self.speed*math.sin(math.radians(180 + self.angle))
        self.currDistance += self.speed
        self.updateRect()

#Lasers separated into two classes depending if player or enemy fired
class Laser(Projectile):
    def __init__(self, x, y, angle, damage):
        super().__init__(x, y, angle, damage)
        self.speed = 10
        self.maxDistance = 600
        self.currDistance = 0
        self.length = 15
        self.width = 5
        self.updateRect()

class PlayerLaser(Laser):
    def __init__(self, x, y, angle, damage):
        super().__init__(x, y, angle, damage)

    def draw(self, screen, data):
        color = (27, 65, 252)
        dx = self.length*math.cos(math.radians(self.angle))
        dy = self.length*math.sin(math.radians(180 + self.angle))
        oldX = self.x + data.scrollX
        oldY = self.y + data.scrollY
        newX = self.x + dx + data.scrollX
        newY = self.y + dy + data.scrollY
        pygame.draw.line(screen, color, [oldX, oldY], [newX, newY], self.width)

class EnemyLaser(Laser):
    def __init__(self, x, y, angle, damage):
        super().__init__(x, y, angle, damage)

    def draw(self, screen, data):
        color = (183, 5, 32)
        dx = self.length*math.cos(math.radians(self.angle))
        dy = self.length*math.sin(math.radians(180 + self.angle))
        oldX = self.x + data.scrollX
        oldY = self.y + data.scrollY
        newX = self.x + dx + data.scrollX
        newY = self.y + dy + data.scrollY
        pygame.draw.line(screen, color, [oldX, oldY], [newX, newY], self.width)


class Rocket(Projectile):
    @staticmethod
    def init():
        Rocket.width = width = 25
        Rocket.height = height = 60
        Rocket.image = pygame.transform.scale(
            pygame.image.load(os.path.join('Objects',
            'Rocket.png')).convert_alpha(), (width, height))

    def __init__(self, x, y, angle, damage, speed=8):
        super().__init__(x, y, angle, damage)
        self.speed = speed
        self.maxDistance = 1000
        self.baseImage = Rocket.image.copy()
        self.currDistance = 0
        self.length, self.width = self.image.get_size()
        self.updateRect()

    def draw(self, screen, data):
        w, h = self.image.get_size()
        newX = self.x - w/2 + data.scrollX
        newY = self.y - h/2 + data.scrollY
        newRect = pygame.Rect(newX, newY, w, h)
        image = pygame.transform.rotate(self.baseImage, self.angle - 90)
        screen.blit(image, newRect)



#General ship item class
class Item(GameObject):
    def __init__(self, x, y, image):
        super().__init__()
        self.x = x
        self.y = y
        self.coord = (x, y)
        self.image = image
        self.baseImage = image.copy()
        self.angle = 0
        self.updateRect()

    def updateRect(self):
        w, h = self.image.get_size()
        self.rect = pygame.Rect(self.x - w/2, self.y - h/2, w, h)

    def update(self, dx, dy):
        self.x = self.x + dx
        self.y = self.y + dy
        self.coord = (self.coord[0] + dx, self.coord[1] + dy)
        self.updateRect()

    def draw(self, screen, data):
        w, h = self.image.get_size()
        itemX = self.x - w/2 + data.scrollX
        itemY = self.y - h/2 + data.scrollY
        newRect = pygame.Rect(itemX, itemY, w, h)
        screen.blit(self.image, newRect)

class CommandModule(Item):
    @staticmethod
    def init():
        CommandModule.width = width = 40
        CommandModule.height = height = 40
        CommandModule.image = pygame.transform.scale(
            pygame.image.load(os.path.join('Objects',
            'Command.png')).convert_alpha(), (width, height))

    def __init__(self, x, y, health=25):
        super().__init__(x, y, CommandModule.image)
        self.health = health

class AlphaBulkhead(Item):
    @staticmethod
    def init():
        AlphaBulkhead.width = width = 40
        AlphaBulkhead.height = height = 40
        AlphaBulkhead.image = pygame.transform.scale(
            pygame.image.load(os.path.join('Objects',
            'AlphaBulkhead.png')).convert_alpha(), (width, height))

    def __init__(self, x, y):
        super().__init__(x, y, AlphaBulkhead.image)
        self.health = 20

class BravoBulkhead(Item):
    @staticmethod
    def init():
        BravoBulkhead.width = width = 40
        BravoBulkhead.height = height = 40
        BravoBulkhead.image = pygame.transform.scale(
            pygame.image.load(os.path.join('Objects',
            'BravoBulkhead.png')).convert_alpha(), (width, height))

    def __init__(self, x, y):
        super().__init__(x, y, BravoBulkhead.image)
        self.health = 40

class CharlieBulkhead(Item):
    @staticmethod
    def init():
        CharlieBulkhead.width = width = 40
        CharlieBulkhead.height = height = 40
        CharlieBulkhead.image = pygame.transform.scale(
            pygame.image.load(os.path.join('Objects',
            'CharlieBulkhead.png')).convert_alpha(), (width, height))

    def __init__(self, x, y):
        super().__init__(x, y, CharlieBulkhead.image)
        self.health = 60

class DeltaBulkhead(Item):
    @staticmethod
    def init():
        DeltaBulkhead.width = width = 40
        DeltaBulkhead.height = height = 40
        DeltaBulkhead.image = pygame.transform.scale(
            pygame.image.load(os.path.join('Objects',
            'DeltaBulkhead.jpg')).convert_alpha(), (width, height))

    def __init__(self, x, y):
        super().__init__(x, y, DeltaBulkhead.image)
        self.health = 100


class Obstacle(Item):
    def __init__(self, x, y, r, image):
        super().__init__(x, y, image)
        self.r = r

    def draw(self, screen, data):
        itemX = self.x + data.scrollX
        itemY = self.y + data.scrollY
        pygame.draw.circle(screen, green, [itemX, itemY], self.r)

#Separate class for items that fire projectiles
class Shooter(Item):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)


class LaserGun(Shooter):
    @staticmethod
    def init():
        LaserGun.width = width = 40
        LaserGun.height = height = 40
        LaserGun.image = pygame.transform.scale(
            pygame.image.load(os.path.join('Objects',
            'LaserGun.png')).convert_alpha(), (width, height))

    def __init__(self, x, y, angle, damage, health=10):
        super().__init__(x, y, LaserGun.image)
        self.angle = angle
        self.damage = damage
        self.cooldown = 40
        self.cooldownTimer = 0
        self.coolingDown = False
        self.health = health

    def draw(self, screen, data):
        w, h = self.image.get_size()
        newX = self.x - w/2 + data.scrollX
        newY = self.y - h/2 + data.scrollY
        newRect = pygame.Rect(newX, newY, w, h)
        image = pygame.transform.rotate(self.baseImage, self.angle - 90)
        screen.blit(image, newRect)

class RocketLauncher(Shooter):
    @staticmethod
    def init():
        RocketLauncher.width = width = 40
        RocketLauncher.height = height = 40
        RocketLauncher.image = pygame.transform.scale(
            pygame.image.load(os.path.join('Objects',
            'RocketLauncher.png')).convert_alpha(), (width, height))

    def __init__(self, x, y, angle, damage, health=10, speed=10):
        super().__init__(x, y, RocketLauncher.image)
        self.angle = angle
        self.damage = damage
        self.cooldown = 100
        self.cooldownTimer = 0
        self.coolingDown = False
        self.health = health
        self.speed = speed

    def draw(self, screen, data):
        w, h = self.image.get_size()
        newX = self.x - w/2 + data.scrollX
        newY = self.y - h/2 + data.scrollY
        newRect = pygame.Rect(newX, newY, w, h)
        image = pygame.transform.rotate(self.baseImage, self.angle - 90)
        screen.blit(image, newRect)
