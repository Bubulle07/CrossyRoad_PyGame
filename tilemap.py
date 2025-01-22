import os
import random as r
import pygame as pg
import constants as const

### Set a value for each element, facilitating their use.
### The number can be changed, without impacting the code.
    ### Ground Materials
AIR = 0
GRASS = 1
WATER = 2
ROAD = 3
    ### Obstacles
TALL_TREE = 11
SMALL_TREE = 12
ROCK_1 = 13
    ### Water obstacles
LILYPAD_1 = 22
LILYPAD_2 = 23
LILYPAD_3 = 24
LILYPAD_4 = 25
RIVER = 31      ### Fictive obstacle that makes the river non crossable.

COIN = 50

### Dictionary of the ground textures.
textures = {
    GRASS : pg.image.load(os.path.join('textures', 'tiles', 'grass_tile.png')),
    WATER : pg.image.load(os.path.join('textures', 'tiles', 'water_tile.png')),
    ROAD : pg.image.load(os.path.join('textures', 'tiles', 'road_tile.png'))
}

### Dictionary of the sides textures.
### The "sides" are placed on top of the tile below to fake 3d.
sides = {
    GRASS : pg.image.load(os.path.join('textures', 'tiles', 'grass_side.png')),
    ROAD : pg.image.load(os.path.join('textures', 'tiles', 'road_side.png'))
}

### Dictionary of the obstacles textures.
obstacles = {
    TALL_TREE : {'img' : pg.image.load(os.path.join('textures', 'obstacles', 'tall_tree.png')),
            'yoffset' : 64},
    SMALL_TREE : {'img' : pg.image.load(os.path.join('textures', 'obstacles', 'small_tree.png')),
            'yoffset' : 64},
    ROCK_1 : {'img' : pg.image.load(os.path.join('textures', 'obstacles', 'rock_1.png')),
            'yoffset' : 0},
}

### Seperate dictionary for the 4 different lilypads textures.
lilypads = {
    LILYPAD_1 : {'img' : pg.image.load(os.path.join('textures', 'obstacles', 'lilypad_1.png')),
            'yoffset' : -4},
    LILYPAD_2 : {'img' : pg.image.load(os.path.join('textures', 'obstacles', 'lilypad_2.png')),
            'yoffset' : -4},
    LILYPAD_3 : {'img' : pg.image.load(os.path.join('textures', 'obstacles', 'lilypad_3.png')),
            'yoffset' : -4},
    LILYPAD_4 : {'img' : pg.image.load(os.path.join('textures', 'obstacles', 'lilypad_4.png')),
            'yoffset' : -4},
}



### List of all the non-crossable obstacles.
### This list is used in main.py to check if the user is allowed to move to the next tile.
non_crossable = [TALL_TREE, SMALL_TREE, ROCK_1, RIVER]



class Tilemap:
    def __init__(self):
        self.linemap = [GRASS]
        self.road_attributes = ['']
        self.tilemap = [[AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR]]
        self.length = len(self.linemap)
        self.shift = 0

    def draw_lines(self, screen):
        for line in range(self.length - self.shift):
            for tile in range(const.TILEMAP_WIDTH):
                screen.blit(textures[self.linemap[line + self.shift]], (tile*const.TILE_SIZE, const.WINDOW_HEIGHT - (line + 1)*const.TILE_SIZE))

                if self.linemap[line - 1 + self.shift] == WATER and self.linemap[line + self.shift] != WATER:
                    screen.blit(sides[self.linemap[line + self.shift]], (tile*const.TILE_SIZE, const.WINDOW_HEIGHT - (line)*const.TILE_SIZE))
            if self.linemap[line + self.shift] == GRASS and (line+ self.shift)%2 == 0:
                lineContrast = pg.Surface((const.WINDOW_WIDTH, const.TILE_SIZE), pg.SRCALPHA)
                lineContrast.fill((0, 0, 0, 20))
                screen.blit(lineContrast, (0, const.WINDOW_HEIGHT - (line + 1)*const.TILE_SIZE))

    def draw_border(self, screen):
        mapBorder = pg.Surface((const.TILE_SIZE*const.BORDER_WIDTH, const.WINDOW_HEIGHT), pg.SRCALPHA)
        mapBorder.fill((0, 0, 0, 80))
        screen.blit(mapBorder, (0, 0))
        screen.blit(mapBorder, (const.WINDOW_WIDTH - const.TILE_SIZE*const.BORDER_WIDTH, 0))

    
    def draw_obstacles(self, screen):
        for row in range (len(self.tilemap) - 1, 0, -1):
            if row > self.shift -2:
                for column in range (len(self.tilemap[row]) - 1):
                    if self.tilemap[row][column] in obstacles :
                        screen.blit(obstacles[self.tilemap[row][column]]['img'], (const.TILE_SIZE*column, const.WINDOW_HEIGHT - (row + 1)*const.TILE_SIZE + self.shift*const.TILE_SIZE - obstacles[self.tilemap[row][column]]['yoffset']))
   
    def draw_obstacles_line(self, screen, line):
        for column in range (len(self.tilemap[line]) - 1):
                    if self.tilemap[line][column] in obstacles :
                        screen.blit(obstacles[self.tilemap[line][column]]['img'], (const.TILE_SIZE*column, const.WINDOW_HEIGHT - (line + 1)*const.TILE_SIZE + self.shift*const.TILE_SIZE - obstacles[self.tilemap[line][column]]['yoffset']))


    def draw_lilypads(self, screen):
        for row in range (len(self.tilemap) - 1, 0, -1):
            if row > self.shift -2:
                for column in range (len(self.tilemap[row]) - 1):
                    if self.tilemap[row][column] in lilypads :
                        screen.blit(lilypads[self.tilemap[row][column]]['img'], (const.TILE_SIZE*column, const.WINDOW_HEIGHT - (row + 1)*const.TILE_SIZE + self.shift*const.TILE_SIZE - lilypads[self.tilemap[row][column]]['yoffset']))

    def shift_forward(self):
        self.shift += 1
    
    def shift_backward(self):
        self.shift -= 1
    
    def add_grass(self):
        self.linemap.append(GRASS)
        self.length = len(self.linemap)
        obstacles = []
        obstacleCount = 0
        for column in range (const.TILEMAP_WIDTH):
            if self.tilemap[len(self.tilemap) - 1][column] != LILYPAD_1 or LILYPAD_2 or LILYPAD_3 or LILYPAD_4:
                if r.randint(1, 100) in range(const.TALL_TREE_SPAWN_RATE) and obstacleCount < const.MAX_OBSTACLES_PER_LINE:
                    obstacles.append(TALL_TREE)
                    obstacleCount += 1
                elif r.randint(1, 100) in range(const.SMALL_TREE_SPAWN_RATE) and obstacleCount < const.MAX_OBSTACLES_PER_LINE:
                    obstacles.append(SMALL_TREE)
                    obstacleCount += 1
                elif r.randint(1, 100) in range(const.ROCK_SPAWN_RATE) and obstacleCount < const.MAX_OBSTACLES_PER_LINE:
                    obstacles.append(ROCK_1)
                    obstacleCount += 1
                else:
                    if r.randint(1, 100) in range(2):
                        obstacles.append(COIN)
                    else :
                        obstacles.append(AIR)
            else:
                obstacles.append(AIR)
        self.tilemap.append(obstacles)
        self.road_attributes.append('')

    def add_road(self):
        self.linemap.append(ROAD)
        self.length = len(self.linemap)
        obstacles = []
        for column in range (const.TILEMAP_WIDTH):
            obstacles.append(AIR)
        self.tilemap.append(obstacles)
        attribute = {'direction': '', 'type': 0}
        attribute['direction'] = ['left', 'right'][r.randint(0, 1)]
        attribute['type'] = r.randint(1, const.DIFFERENT_CAR_TYPES)
        self.road_attributes.append(attribute)

    def add_water(self):
        self.linemap.append(WATER)
        self.length = len(self.linemap)
        obstacles = []
        for column in range (const.TILEMAP_WIDTH):
            if r.randint(1, 100) in range(const.LILYPAD_SPAWN_RATE):
                obstacles.append([LILYPAD_1, LILYPAD_2, LILYPAD_3, LILYPAD_4][r.randint(0, 3)])
                self.tilemap[len(self.tilemap) -1][column] = AIR
            else : 
                obstacles.append(RIVER)
        for k in range (2):
            column = r.randint(const.BORDER_WIDTH, const.TILEMAP_WIDTH - const.BORDER_WIDTH - 1)
            obstacles[column] = LILYPAD_1
            self.tilemap[len(self.tilemap) -1][column] = AIR
        self.tilemap.append(obstacles)
        self.road_attributes.append('')

    def generate_line(self):
        if r.randint(1, 100) in range(const.ROAD_GEN_RATE):
            self.add_road()
        elif r.randint(1, 100) in range(const.WATER_GEN_RATE) and self.linemap[self.length - 1] != WATER:
            self.add_water()
        else:
            self.add_grass()