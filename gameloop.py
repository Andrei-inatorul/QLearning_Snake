import sys
from random import randrange

import pygame
from snake import Snake, Direction, Position
from map import Fruit, Map
import utils
import pygame

# ----- Custom Events -----
FRUITSPAWN_EVENT = pygame.USEREVENT + 1
FRUITSPAWN_TIMER = 1000
# -------------------------

BACKGROUNDCOLOR = (168, 198, 78)

player: Snake = None
fruit: Fruit = None

def HandleEvents(events: list):
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == FRUITSPAWN_EVENT:
            global fruit
            if fruit.eaten:
                x = randrange(utils.GRIDSIZE)
                y = randrange(utils.GRIDSIZE)
                fruit = Fruit(Position(x, y))
                while fruit.position in player.get_postion():
                    x = randrange(utils.GRIDSIZE)
                    y = randrange(utils.GRIDSIZE)
                    fruit = Fruit(Position(x, y))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player.change_direction(Direction.LEFT)
            if event.key == pygame.K_d:
                player.change_direction(Direction.RIGHT)
            if event.key == pygame.K_w:
                player.change_direction(Direction.UP)
            if event.key == pygame.K_s:
                player.change_direction(Direction.DOWN)
            if event.key == pygame.K_UP: # debug only
                player.grow()


def Update():
    # -- update game here
   #d player.move()
    if player.check_collision_with_fruit(fruit):
        player.grow()
        fruit.eaten = True
    else:
        player.move()
    pass

def Render(screen : pygame.Surface):
    screen.fill((34, 139, 34))
    Map.Render(screen)
    player.render(screen)
    if not fruit.eaten:
        fruit.render(screen)
    # -- render code goes here
    pygame.display.update()