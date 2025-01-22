import os
import pygame as pg
# FILE WITH ALL THE CONSTANTS FOR THE GAME

# General WINDOW Constants
WINDOW_WIDTH = 1088 # 1088
WINDOW_HEIGHT = 704 # 704
WINDOW_CAPTION = 'Crossy Road!'
FPS = 60

TILE_SIZE = 64
TILEMAP_WIDTH = 17 # Number of tiles

BORDER_WIDTH = 3 # Number of tiles

MOVEMENT_UP_MARGIN = 6 # Number of tiles
MOVEMENT_DOWN_MARGIN = 3 # Number of tiles

# Moving Objects
MOVING_OBJECT_UPDATE_DISTANCE = 30
MOVING_OBJECT_KILL_DISTANCE = 20

TRUNK_SPEED = 2

    # Cars
DIFFERENT_CAR_TYPES = 5

SHORT_CAR_SPEED = 5 
SHORT_CAR_INTERVAL = 130

MEDIUM_CAR_SPEED = 4
MEDIUM_CAR_INTERVAL = 170

TAXI_SPEED = 6
TAXI_INTERVAL = 150

TRUCK_SPEED = 3
TRUCK_INTERVAL = 200

# Terrain Generation
PREGEN_GRASS_LINES = 5 # 10
PREGEN_RANDOM_LINES = 20 # 20

ROAD_GEN_RATE = 60
WATER_GEN_RATE = 40
### Else : GRASS

TALL_TREE_SPAWN_RATE = 8
SMALL_TREE_SPAWN_RATE = 8
ROCK_SPAWN_RATE = 8
LILYPAD_SPAWN_RATE = 30

MAX_OBSTACLES_PER_LINE = 6



# Textures

textures = {
    'icon' : pg.image.load(os.path.join('textures', 'player', 'player_r.png')),
    'player_f' : pg.image.load(os.path.join('textures', 'player', 'player_f.png')),
    'player_b' : pg.image.load(os.path.join('textures', 'player', 'player_b.png')),
    'player_r' : pg.image.load(os.path.join('textures', 'player', 'player_r.png')),
    'player_l' : pg.image.load(os.path.join('textures', 'player', 'player_l.png')),
    'trunk_1' : pg.image.load(os.path.join('textures', 'obstacles', 'trunk_1.png')),
    'short_car_1': {'img' : pg.image.load(os.path.join('textures', 'vehicles', 'short_car_1.png')),
                    'yoffset' : 64},
    'medium_car_1': {'img' : pg.image.load(os.path.join('textures', 'vehicles', 'medium_car_1.png')),
                    'yoffset' : 64},
    'medium_car_2': {'img' : pg.image.load(os.path.join('textures', 'vehicles', 'medium_car_2.png')),
                    'yoffset' : 64},
    'taxi_1': {'img' : pg.image.load(os.path.join('textures', 'vehicles', 'taxi_1.png')),
                    'yoffset' : 64},
    'truck_1': {'img' : pg.image.load(os.path.join('textures', 'vehicles', 'truck_1.png')),
                    'yoffset' : 64}
}