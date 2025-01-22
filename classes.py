import pygame as pg
import constants as const
import random as r

class Player(pg.sprite.Sprite):
    def __init__(self, xTile, yTile):
        pg.sprite.Sprite.__init__(self)
        self.xTile = xTile
        self.yTile = yTile
        self.xPos = self.xTile * const.TILE_SIZE
        self.yPos = const.WINDOW_HEIGHT - self.yTile * const.TILE_SIZE - const.TILE_SIZE
        self.img = const.textures['player_f']
        self.rot = 0    # 0 : forward, 1 : right, 2: backward, 3: left
        self.rect = pg.Rect(self.xPos, self.yPos, self.img.get_width(), self.img.get_height())
        self.score = 0

    def draw(self, screen):
        screen.blit(self.img, (self.xPos, self.yPos))
    
    def move_forward(self):
        self.img = const.textures['player_f']
        self.rot = 0
        self.yTile += 1
        self.yPos -= const.TILE_SIZE
        self.rect = pg.Rect(self.xPos, self.yPos, 64, 64)
    
    def move_backward(self):
        self.img = const.textures['player_b']
        self.rot = 1
        self.yTile -= 1
        self.yPos += const.TILE_SIZE
        self.rect = pg.Rect(self.xPos, self.yPos, 64, 64)
    
    def move_right(self):
        self.img = const.textures['player_r']
        self.rot = 2
        self.xTile += 1
        self.xPos += const.TILE_SIZE
        self.rect = pg.Rect(self.xPos, self.yPos, 64, 64)

    def move_left(self):
        self.img = const.textures['player_l']
        self.rot = 3
        self.xTile -= 1
        self.xPos -= const.TILE_SIZE
        self.rect = pg.Rect(self.xPos, self.yPos, 64, 64)



# class Trunk(pg.sprite.Sprite):
#     def __init__(self, xPos, yTile, direction):
#         pg.sprite.Sprite.__init__(self)
#         self.img = const.textures['trunk_1']
#         self.xPos = xPos
#         self.yTile = yTile
#         self.direction = direction # 'right' or 'left'
#         self.yPos = const.WINDOW_HEIGHT - self.yTile * const.TILE_SIZE - const.TILE_SIZE
#         self.speed = const.TRUNK_SPEED
#         # rect for collisions

#     def draw(self, screen, shift):
#         screen.blit(self.img, (self.xPos, self.yPos + shift*const.TILE_SIZE))

#     def update(self, direction):
#         if direction == 'right':
#             self.xPos += self.speed
#         elif direction == 'left':
#             self.xPos -= self.speed
#         # update rect


class Vehicle(pg.sprite.Sprite):
    def __init__(self, yTile, direction):
        pg.sprite.Sprite.__init__(self)
        self.yTile = yTile
        self.direction = direction
        self.yPos = const.WINDOW_HEIGHT - self.yTile * const.TILE_SIZE - const.TILE_SIZE
        if direction == 'right':
            self.xPos = 0 - self.img.get_width() - r.randint(0, 300)
        elif direction == 'left':
            self.xPos = const.WINDOW_WIDTH + r.randint(0, 300)
            self.img = pg.transform.flip(self.img, True, False)
        self.rect = pg.Rect(self.xPos, self.yPos, self.img.get_width(), 64)

    def draw(self, screen, shift):
        screen.blit(self.img, (self.xPos, self.yPos + shift*const.TILE_SIZE - self.yoffset))
    
    def update(self, direction, shift):
        if direction == 'right':
            self.xPos += self.speed
        elif direction == 'left':
            self.xPos -= self.speed
        self.rect = pg.Rect(self.xPos, self.yPos + shift*const.TILE_SIZE, self.img.get_width(), 64)


class ShortCar(Vehicle):
    def __init__(self, yTile, direction):
        self.img = const.textures['short_car_1']['img']
        self.yoffset = const.textures['short_car_1']['yoffset']
        self.speed = const.SHORT_CAR_SPEED
        super().__init__(yTile, direction)

class MediumCar_1(Vehicle):
    def __init__(self, yTile, direction):
        self.img = const.textures['medium_car_1']['img']
        self.yoffset = const.textures['medium_car_1']['yoffset']
        self.speed = const.MEDIUM_CAR_SPEED
        super().__init__(yTile, direction)

class MediumCar_2(Vehicle):
    def __init__(self, yTile, direction):
        self.img = const.textures['medium_car_2']['img']
        self.yoffset = const.textures['medium_car_2']['yoffset']
        self.speed = const.MEDIUM_CAR_SPEED
        super().__init__(yTile, direction)

class Taxi(Vehicle):
    def __init__(self, yTile, direction):
        self.img = const.textures['taxi_1']['img']
        self.yoffset = const.textures['taxi_1']['yoffset']
        self.speed = const.TAXI_SPEED
        super().__init__(yTile, direction)

class Truck(Vehicle):
    def __init__(self, yTile, direction):
        self.img = const.textures['truck_1']['img']
        self.yoffset = const.textures['truck_1']['yoffset']
        self.speed = const.TRUCK_SPEED
        super().__init__(yTile, direction)