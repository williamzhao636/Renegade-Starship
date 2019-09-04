'''
Andrew ID: wzhao3

Randomizes enemy spawns depending on the current game difficulty and
subtle differences within each enemy level.
'''


import pygame
import random

from Classes import objects
from Classes import ships

#Two Alpha enemies to choose from
def spawnAlpha1(data):
    enemyX = random.randint(0 - int(data.scrollX),
        data.width - int(data.scrollX))
    enemyY = random.randint(0 - int(data.scrollY),
        data.height - int(data.scrollY))
    height = objects.AlphaBulkhead.height
    width = objects.AlphaBulkhead.width
    commandModule = objects.CommandModule(enemyX, enemyY, 10)
    bot = objects.AlphaBulkhead(enemyX, enemyY + height)
    laserGun = objects.LaserGun(enemyX, enemyY - height, 90, 5)

    layout =    [   [None, None, None],
                    [None, laserGun, None],
                    [None, commandModule, None],
                    [None, bot, None],
                    [None, None, None]
                    ]
    connections =   [   [None, None, None],
                        [None, 'DOWN', None],
                        [None, 'CM', None],
                        [None, 'UP', None],
                        [None, None, None]
                        ]

    newEnemy = ships.EnemyShip(enemyX, enemyY, layout, connections, 0)
    return newEnemy

def spawnAlpha2(data):
    enemyX = random.randint(0 - int(data.scrollX),
        data.width - int(data.scrollX))
    enemyY = random.randint(0 - int(data.scrollY),
        data.height - int(data.scrollY))
    height = objects.AlphaBulkhead.height
    width = objects.AlphaBulkhead.width
    commandModule = objects.CommandModule(enemyX, enemyY, 10)
    left = objects.AlphaBulkhead(enemyX - width, enemyY)
    right = objects.AlphaBulkhead(enemyX + width, enemyY)
    laserGun = objects.LaserGun(enemyX, enemyY - height, 90, 5)

    layout =    [   [None, None, None, None, None],
                    [None, None, laserGun, None, None],
                    [None, left, commandModule, right, None],
                    [None, None, None, None, None],
                    [None, None, None, None, None]
                    ]
    connections =   [   [None, None, None, None, None],
                        [None, None, 'DOWN', None, None],
                        [None, 'RIGHT', 'CM', 'LEFT', None],
                        [None, None, None, None, None],
                        [None, None, None, None, None]
                        ]

    newEnemy = ships.EnemyShip(enemyX, enemyY, layout, connections, 0)
    return newEnemy

def spawnAlpaEnemy(data):
    if random.randint(0, 1) == 0:
        newEnemy = spawnAlpha1(data)
    else:
        newEnemy = spawnAlpha2(data)
    return newEnemy


#Two Bravo enemies to choose from
def spawnBravo1(data):
    enemyX = random.randint(0 - int(data.scrollX),
        data.width - int(data.scrollX))
    enemyY = random.randint(0 - int(data.scrollY),
        data.height - int(data.scrollY))

    width = objects.BravoBulkhead.width
    height = objects.BravoBulkhead.height
    commandModule = objects.CommandModule(enemyX, enemyY, 25)
    right = objects.BravoBulkhead(enemyX + width, enemyY)
    left = objects.BravoBulkhead(enemyX - width, enemyY)
    bot = objects.BravoBulkhead(enemyX, enemyY + height)
    laserGun = objects.LaserGun(enemyX, enemyY - height, 90, 5)
    layout =    [   [None, None, None, None, None],
                    [None, None, laserGun, None, None],
                    [None, left, commandModule, right, None],
                    [None, None, bot, None, None, None],
                    [None, None, None, None, None]
                    ]
    connections =   [   [None, None, None, None, None],
                        [None, None, 'DOWN', None, None],
                        [None, 'RIGHT', 'CM', 'LEFT', None],
                        [None, None, 'UP', None, None],
                        [None, None, None, None, None]
                        ]

    newEnemy = ships.EnemyShip(enemyX, enemyY, layout, connections, 1, -3)
    return newEnemy

def spawnBravo2(data):
    enemyX = random.randint(0 - int(data.scrollX),
        data.width - int(data.scrollX))
    enemyY = random.randint(0 - int(data.scrollY),
        data.height - int(data.scrollY))

    width = objects.BravoBulkhead.width
    height = objects.BravoBulkhead.height
    commandModule = objects.CommandModule(enemyX, enemyY, 25)
    right = objects.BravoBulkhead(enemyX + width, enemyY)
    top = objects.BravoBulkhead(enemyX, enemyY - height)
    left = objects.BravoBulkhead(enemyX - width, enemyY)
    bot = objects.BravoBulkhead(enemyX, enemyY + height)
    laserGun = objects.LaserGun(enemyX, enemyY - 2*height, 90, 5)
    layout =    [   [None, None, laserGun, None, None],
                    [None, None, top, None, None],
                    [None, left, commandModule, right, None],
                    [None, None, bot, None, None, None],
                    [None, None, None, None, None]
                    ]
    connections =   [   [None, None, 'DOWN', None, None],
                        [None, None, 'DOWN', None, None],
                        [None, 'RIGHT', 'CM', 'LEFT', None],
                        [None, None, 'UP', None, None],
                        [None, None, None, None, None]
                        ]

    newEnemy = ships.EnemyShip(enemyX, enemyY, layout, connections, 1, -3)
    return newEnemy

def spawnBravoEnemy(data):
    if random.randint(0, 1) == 0:
        newEnemy = spawnBravo1(data)
    else:
        newEnemy = spawnBravo2(data)
    return newEnemy


def spawnCharlie1(data):
    enemyX = random.randint(0 - int(data.scrollX),
        data.width - int(data.scrollX))
    enemyY = random.randint(0 - int(data.scrollY),
        data.height - int(data.scrollY))

    width = objects.CharlieBulkhead.width
    height = objects.CharlieBulkhead.height
    commandModule = objects.CommandModule(enemyX, enemyY, 50)
    right = objects.CharlieBulkhead(enemyX + width, enemyY)
    top = objects.CharlieBulkhead(enemyX, enemyY - height)
    left = objects.CharlieBulkhead(enemyX - width, enemyY)
    bot = objects.CharlieBulkhead(enemyX, enemyY + height)
    laserGun1 = objects.LaserGun(enemyX, enemyY - height, 90, 5, 20)
    laserGun2 = objects.LaserGun(enemyX - width, enemyY - height, 90, 5, 20)
    laserGun3 = objects.LaserGun(enemyX + width, enemyY - height, 90, 5, 20)
    layout =    [   [None, None, None, None, None],
                    [None, laserGun2, laserGun1, laserGun3, None],
                    [None, left, commandModule, right, None],
                    [None, None, bot, None, None],
                    [None, None, None, None, None]
                    ]
    connections =   [   [None, None, None, None, None],
                        [None, 'DOWN', 'DOWN', 'DOWN', None],
                        [None, 'RIGHT', 'CM', 'LEFT', None],
                        [None, None, 'UP', None, None],
                        [None, None, None, None, None]
                        ]

    newEnemy = ships.EnemyShip(enemyX, enemyY, layout, connections, 2, -4)
    return newEnemy


def spawnCharlie2(data):
    enemyX = random.randint(0 - int(data.scrollX),
        data.width - int(data.scrollX))
    enemyY = random.randint(0 - int(data.scrollY),
        data.height - int(data.scrollY))

    width = objects.CharlieBulkhead.width
    height = objects.CharlieBulkhead.height
    commandModule = objects.CommandModule(enemyX, enemyY, 50)
    top = objects.CharlieBulkhead(enemyX, enemyY - height)
    bot = objects.CharlieBulkhead(enemyX, enemyY + height)
    laserGun1 = objects.LaserGun(enemyX, enemyY - height, 90, 5, 20)
    laserGun2 = objects.LaserGun(enemyX - width, enemyY, 180, 10, 20)
    laserGun3 = objects.LaserGun(enemyX + width, enemyY, 0, 10, 20)
    layout =    [   [None, None, None, None, None],
                    [None, None, laserGun1, None, None],
                    [None, laserGun2, commandModule, laserGun3, None],
                    [None, None, bot, None, None],
                    [None, None, None, None, None]
                    ]
    connections =   [   [None, None, None, None, None],
                        [None, None, 'DOWN', None, None],
                        [None, 'RIGHT', 'CM', 'LEFT', None],
                        [None, None, 'UP', None, None],
                        [None, None, None, None, None]
                        ]

    newEnemy = ships.EnemyShip(enemyX, enemyY, layout, connections, 2, -4)
    return newEnemy

def spawnCharlie3(data):
    enemyX = random.randint(0 - int(data.scrollX),
        data.width - int(data.scrollX))
    enemyY = random.randint(0 - int(data.scrollY),
        data.height - int(data.scrollY))

    width = objects.CharlieBulkhead.width
    height = objects.CharlieBulkhead.height
    commandModule = objects.CommandModule(enemyX, enemyY, 50)
    right = objects.CharlieBulkhead(enemyX + width, enemyY)
    top = objects.CharlieBulkhead(enemyX, enemyY - height)
    left = objects.CharlieBulkhead(enemyX - width, enemyY)
    bot = objects.CharlieBulkhead(enemyX, enemyY + height)
    rocketLauncher1 = objects.RocketLauncher(enemyX, enemyY - height, 90, 15)
    rocketLauncher2 = objects.RocketLauncher(enemyX, enemyY + 2*height, 270, 15)
    laserGun1 = objects.LaserGun(enemyX, enemyY - height, 90, 5, 20)
    laserGun2 = objects.LaserGun(enemyX - width, enemyY - height, 90, 5, 20)
    laserGun3 = objects.LaserGun(enemyX + width, enemyY - height, 90, 5, 20)
    layout =    [   [None, None, None, None, None],
                    [None, laserGun2, rocketLauncher1, laserGun3, None],
                    [None, left, commandModule, right, None],
                    [None, None, bot, None, None],
                    [None, None, rocketLauncher2, None, None],
                    [None, None, None, None, None]
                    ]
    connections =   [   [None, None, None, None, None],
                        [None, 'DOWN', 'DOWN', 'DOWN', None],
                        [None, 'RIGHT', 'CM', 'LEFT', None],
                        [None, None, 'UP', None, None],
                        [None, None, 'UP', None, None],
                        [None, None, None, None, None]
                    ]

    newEnemy = ships.EnemyShip(enemyX, enemyY, layout, connections, 2, -4)
    return newEnemy

def spawnCharlieEnemy(data):
    choice = random.randint(0, 2)
    if choice == 0:
        newEnemy = spawnCharlie1(data)
    elif choice == 1:
        newEnemy = spawnCharlie2(data)
    else:
        newEnemy = spawnCharlie3(data)
    return newEnemy



def spawnDeltaEnemy(data):
    enemyX = random.randint(0 - int(data.scrollX),
        data.width - int(data.scrollX))
    enemyY = random.randint(0 - int(data.scrollY),
        data.height - int(data.scrollY))

    width = objects.DeltaBulkhead.width
    height = objects.DeltaBulkhead.height
    command = objects.CommandModule(enemyX, enemyY, 150)
    right = objects.DeltaBulkhead(enemyX + width, enemyY)
    top = objects.DeltaBulkhead(enemyX, enemyY - height)
    topLeft = objects.DeltaBulkhead(enemyX - width, enemyY - height)
    topRight = objects.DeltaBulkhead(enemyX + width, enemyY - height)
    left = objects.DeltaBulkhead(enemyX - width, enemyY)
    bot = objects.DeltaBulkhead(enemyX, enemyY + height)
    rocket1 = objects.RocketLauncher(enemyX - width, enemyY - 2*height, 90, 35, 50, 15)
    rocket2 = objects.RocketLauncher(enemyX + width, enemyY - 2*height, 90, 35, 50, 15)
    rocket3 = objects.RocketLauncher(enemyX, enemyY + 2*height, 270, 35, 50, 20)
    laser1 = objects.LaserGun(enemyX, enemyY - height, 90, 25, 50)
    laser2 = objects.LaserGun(enemyX - width, enemyY + height, 270, 25, 50)
    laser3 = objects.LaserGun(enemyX + width, enemyY + height, 270, 25, 50)
    laser4 = objects.LaserGun(enemyX - 2*width, enemyY - height, 180, 25, 50)
    laser5 = objects.LaserGun(enemyX + 2*width, enemyY - height, 0, 25, 50)
    layout =    [   [None, None, None, None, None, None, None],
                    [None, None, rocket1, laser1, rocket2, None, None],
                    [None, laser4, topLeft, top, topRight, laser5, None],
                    [None, None, left, command, right, None, None],
                    [None, None, laser2, bot, laser3, None, None],
                    [None, None, None, rocket3, None, None, None],
                    [None, None, None, None, None, None, None]
                    ]
    connections =   [   [None, None, None, None, None, None, None],
                        [None, None, 'DOWN', 'DOWN', 'DOWN', None, None],
                        [None, 'RIGHT', 'DOWN', 'DOWN', 'DOWN', 'LEFT', None],
                        [None, None, 'RIGHT', 'CM', 'LEFT', None, None],
                        [None, None, 'UP', 'UP', 'UP', None, None],
                        [None, None, None, 'UP', None, None, None],
                        [None, None, None, None, None, None, None]
                        ]

    newEnemy = ships.EnemyShip(enemyX, enemyY, layout, connections, 2, -5)
    return newEnemy


#Randomizes the enemy level spawn
def spawnEnemy(data):
    if len(data.enemiesGroup) < data.maxEnemies:
        baseEnemyLevel = data.crimeLevel
        choice = random.randint(data.crimeLevel - 1, data.crimeLevel + 1)
        if choice <= 0:
            newEnemy = spawnAlpaEnemy(data)
        if choice == 1:
            newEnemy = spawnBravoEnemy(data)
        if choice == 2:
            newEnemy = spawnCharlieEnemy(data)
        if choice >= 3:
            data.crimeLevel = 4
            newEnemy = spawnDeltaEnemy(data)

        needRespawn = False

        #Checks if it will spawn on top of the player
        if len(pygame.sprite.groupcollide(newEnemy.itemsGroup,
                data.player.itemsGroup, False, False)) > 0:
            spawnEnemy(data)
        else:
            #Checks if it will spawn on top of an enemy
            for enemy in data.enemiesGroup:
                if len(pygame.sprite.groupcollide(enemy.itemsGroup,
                    newEnemy.itemsGroup, False, False)) > 0:
                    needRespawn = True
            if needRespawn:
                spawnEnemy(data)
            else:
                data.enemiesGroup.add(newEnemy)



