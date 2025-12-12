import pygame
import gameloop
import configparser

from map import Fruit
from snake import Snake, Direction
import utils

def main():
    # ------------- Init Pygame ----------
    pygame.init()
    CfgParser = configparser.ConfigParser()
    CfgParser.read('config.ini')

    # ---------- Window Settings ----------
    width = int(CfgParser.get('Display Settings', 'width'))
    height = int(CfgParser.get('Display Settings', 'height'))
    gridsize = int(CfgParser.get('Display Settings', 'gridsize'))
    screen = pygame.display.set_mode((width, height))
    utils.SCALE = width/gridsize
    utils.GRIDSIZE = gridsize
    pygame.display.set_caption("Q_Learning_Snake - Lefter Andrei & Lunca Vlad")

    # ---------- Init Game Logic ----------
    clock = pygame.time.Clock()
    gameloop.player = Snake(gridsize//2, gridsize//2, Direction.DOWN, int(4 * utils.SCALE))
    gameloop.fruit = Fruit(utils.Position(2, 2))
    pygame.time.set_timer(gameloop.FRUITSPAWN_EVENT, gameloop.FRUITSPAWN_TIMER)
    # ---------- Game Loop ----------
    while True:
        # ---------- Handle KeyPresses and Other Events ----------
        gameloop.HandleEvents(pygame.event.get())
        # ---------- Update Physics ----------
        gameloop.Update()
        # ---------- Render Window ----------
        gameloop.Render(screen)

if __name__ == '__main__':
    main()
