import pygame as pg
import random as r
import os
import constants as const
import tilemap
from classes import *

pg.init()
pg.font.init()

pg.display.set_caption(const.WINDOW_CAPTION)
pg.display.set_icon(const.textures['icon'])
screen = pg.display.set_mode((const.WINDOW_WIDTH, const.WINDOW_HEIGHT))

clock = pg.time.Clock()


def menu():
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                pg.quit()
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    running = False

        screen.fill((0, 0, 0))
        pg.display.update()
        clock.tick(const.FPS)


#######################################
### P L A Y I N G   F U N C T I O N ###
#######################################
def main() :

    map = tilemap.Tilemap()

    ### Pregen a few lines
    # for k in range (12):
    #     map.add_road()
    for line in range(const.PREGEN_GRASS_LINES):
        map.add_grass()
    for line in range(const.PREGEN_RANDOM_LINES):
        map.generate_line()

    ### Create player & add it to the player group for collisions
    player = Player(8, 0)
    playerGroup =pg.sprite.Group()
    playerGroup.add(player)

    ### Create a vehicle group for collisions
    vehicleGroup = pg.sprite.Group()

    running = True
    tickCounter = 0
    scoreFont = pg.font.Font(os.path.join('textures', 'font', '8_bit_font.TTF'), 50)
    ### MAIN LOOP
    while running:

    ###################
    ### I N P U T S ###
    ###################

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                pg.quit()

            ### CHECK KEYS
            if event.type == pg.KEYDOWN:

                ### MOVE FORWARD
                if event.key == pg.K_UP or event.key == pg.K_w:
                    ### Check if there is no obstacle in front of the player
                    if map.tilemap[player.yTile + 1][player.xTile] not in tilemap.non_crossable:
                        ### Move the player, not the background
                        if player.yPos > const.WINDOW_HEIGHT - const.TILE_SIZE * const.MOVEMENT_UP_MARGIN:
                            player.move_forward()
                        ### Move the background, not the player
                        else:
                            player.yTile += 1
                            map.shift_forward()
                            player.img = const.textures['player_f']
                            player.rot = 0
                        # Update score
                        if player.yTile > player.score:
                            player.score += 1
                            map.generate_line()

                ### MOVE BACKGROUND
                if event.key == pg.K_DOWN or event.key == pg.K_s:
                    ### Check if there is no obstacle behing the player
                    if map.tilemap[player.yTile - 1][player.xTile] not in tilemap.non_crossable:
                        ### Move the player, not the background
                        if player.yPos < const.WINDOW_HEIGHT - const.TILE_SIZE * const.MOVEMENT_DOWN_MARGIN or map.shift == 0:
                            if player.yTile > 0:
                                player.move_backward()
                        ### Move the background, not the player
                        else :
                            player.yTile -= 1
                            map.shift_backward()
                            player.img = const.textures['player_b']
                            player.rot = 1

                ### MOVE RIGHT
                if event.key == pg.K_RIGHT or event.key == pg.K_d:
                    ### Check if there is no obstacle
                    if map.tilemap[player.yTile][player.xTile + 1] not in tilemap.non_crossable:
                        ### Move the player
                        if player.xTile < const.TILEMAP_WIDTH - const.BORDER_WIDTH - 1:
                            player.move_right()

                ### MOVE LEFT
                if event.key == pg.K_LEFT or event.key == pg.K_a:
                    ### Check if there is no obstacle
                    if map.tilemap[player.yTile][player.xTile - 1] not in tilemap.non_crossable:
                        ### Move the player
                        if player.xTile > const.BORDER_WIDTH :
                            player.move_left()

                # if event.key == pg.K_SPACE:
                    # map.generate_line()
                # if event.key == pg.K_ESCAPE:
                #     running = False

    ##############################
    ### G A M E   U P D A T E  ###
    ##############################

        ### SPAWN VEHICLES
        for road in range(len(map.road_attributes) -1, 0, -1):
            ### Update is made only within a specific range, to decrease calculation time
            if road >= map.shift -2 and road <= map.shift + const.WINDOW_HEIGHT/const.TILE_SIZE + const.MOVING_OBJECT_UPDATE_DISTANCE:
                ### Check if the line is a road
                if map.road_attributes[road] != '':
                    ### Spawn Short Cars
                    if map.road_attributes[road]['type'] == 1:
                        if tickCounter%const.SHORT_CAR_INTERVAL == 0:
                            vehicle = ShortCar(road, map.road_attributes[road]['direction'])
                            vehicleGroup.add(vehicle)
                    ### Spawn Medium Car 1
                    if map.road_attributes[road]['type'] == 2:
                        if tickCounter%const.MEDIUM_CAR_INTERVAL == 0:
                            vehicle = MediumCar_1(road, map.road_attributes[road]['direction'])
                            vehicleGroup.add(vehicle)
                    ### Spawn Medium Car 2
                    if map.road_attributes[road]['type'] == 3:
                        if tickCounter%const.MEDIUM_CAR_INTERVAL == 0:
                            vehicle = MediumCar_2(road, map.road_attributes[road]['direction'])
                            vehicleGroup.add(vehicle)
                    ### Spawn Taxi
                    if map.road_attributes[road]['type'] == 4:
                        if tickCounter%const.TAXI_INTERVAL == 0:
                            vehicle = Taxi(road, map.road_attributes[road]['direction'])
                            vehicleGroup.add(vehicle)
                    ### Spawn Truck
                    if map.road_attributes[road]['type'] == 5:
                        if tickCounter%const.TRUCK_INTERVAL == 0:
                            vehicle = Truck(road, map.road_attributes[road]['direction'])
                            vehicleGroup.add(vehicle)


        ### UPDATE VEHICLES
        updatedVehicleCounter = 0 # Used for debug only
        for vehicle in vehicleGroup:
            # Update is made only within a specific range, to decrease calculation time
            if vehicle.yTile >= map.shift -2 and vehicle.yTile <= map.shift + const.WINDOW_HEIGHT/const.TILE_SIZE + const.MOVING_OBJECT_UPDATE_DISTANCE:
                vehicle.update(vehicle.direction, map.shift)
                # vehicle.rect = pg.Rect(vehicle.xPos, vehicle.yPos, 128, 64)
                updatedVehicleCounter += 1 # Used for debug only
            # Kill the vehicle if not in the screen horizontally
            if vehicle.xPos > const.WINDOW_WIDTH + 700 or vehicle.xPos < -700: # Change the values to the hitbox width
                vehicle.kill()
            # Kill the vehicles that are far behind, off the screen
            if vehicle.yTile < map.shift - const.MOVING_OBJECT_KILL_DISTANCE:
                vehicle.kill()
        # collision = pg.sprite.spritecollide(player, vehicleGroup, True)

        collisions = pg.sprite.groupcollide(playerGroup, vehicleGroup, False, False)
        if len(collisions) > 0:
            running = False

    #################################
    ### S C R E E N   U P D A T E ###
    #################################

        screen.fill((0, 0, 0))

        ### Draw the background lines
        map.draw_lines(screen)
        ### Draw lilypads on the rivers
        map.draw_lilypads(screen)
        ### Draw the player
        player.draw(screen)

        ### Draw obstacles and vehicles
        ### The drawing is made from top to bottom, to have the right superposition and perspective.
        for line in range(map.length - 1, 0, -1):
            if line > map.shift -2 and line < map.shift + const.WINDOW_HEIGHT/const.TILE_SIZE + 2:
                map.draw_obstacles_line(screen, line)
                for vehicle in vehicleGroup:
                    if vehicle.yTile == line:
                        vehicle.draw(screen, map.shift)


        ### Draw the darker borders
        map.draw_border(screen)

    ###############################
    ### T E X T   D I S P L A Y ###
    ###############################

        scoreTextOutline = scoreFont.render(f'{player.score}', True, (0, 0, 0))
        scoreText = scoreFont.render(f'{player.score}', True, (255, 255, 255))
        ### Draw Outline
        screen.blit(scoreTextOutline, (20, 20))
        screen.blit(scoreTextOutline, (30, 20))
        screen.blit(scoreTextOutline, (20, 30))
        screen.blit(scoreTextOutline, (30, 30))
        ### Draw Text
        screen.blit(scoreText, (25, 25))

    #################################
    ### F I N A L   U P D A T E S ###
    #################################

        pg.display.update()
        clock.tick(const.FPS)
        tickCounter += 1

    #################
    ### D E B U G ###
    #################
        # print(len(vehicleGroup), updatedVehicleCounter)
        # print(player.score)
        # print(player.rect)
        # if (tickCounter - 1)%1000 == 0:
        #     for v in vehicleGroup:
        #         print(v)
        # print(clock.get_fps())
        # print(map.length)


#################################
### D I E D   F U N C T I O N ###
#################################
def died():
    running = True
    font_H1 = pg.font.Font(os.path.join('textures', 'font', '8_bit_font.TTF'), 100)
    font_H2 = pg.font.Font(os.path.join('textures', 'font', '8_bit_font.TTF'), 40)

    background = pg.Surface((const.WINDOW_WIDTH, const.WINDOW_HEIGHT), pg.SRCALPHA)
    background.fill((0, 0, 0, 100))
    screen.blit(background, (0, 0))

    gameOverText = font_H1.render(f'GAME OVER', True, (250, 210, 30))
    gameOverOutlineText = font_H1.render(f'GAME OVER', True, (0, 0, 0))
    screen.blit(gameOverOutlineText, (90, 200))
    screen.blit(gameOverOutlineText, (110, 200))
    screen.blit(gameOverOutlineText, (100, 190))
    screen.blit(gameOverOutlineText, (100, 210))
    screen.blit(gameOverText, (100, 200))

    playAgainText = font_H2.render(f'Press SPACE to play again', True, (255, 255, 255))
    playAgainOutlineText = font_H2.render(f'Press SPACE to play again', True, (0, 0, 0))
    screen.blit(playAgainOutlineText, (85, 350))
    screen.blit(playAgainOutlineText, (95, 350))
    screen.blit(playAgainOutlineText, (90, 345))
    screen.blit(playAgainOutlineText, (90, 355))
    screen.blit(playAgainText, (90, 350))

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                pg.quit()
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    running = False

        pg.display.update()
        clock.tick(const.FPS)

###################################
### C A L L   F U N C T I O N S ###
###################################

# menu()
while True :
    main()
    died()