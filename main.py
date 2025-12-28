import configparser
import pygame
import gameloop
from QAgent import QAgent

from map import Fruit
from snake import Snake, Direction
import utils

def main():
    # ------------- Init Pygame ----------
    pygame.init()
    cfg_parser = configparser.ConfigParser()
    cfg_parser.read('config.ini')

    # ---------- Window Settings ----------
    width = int(cfg_parser.get('Display Settings', 'width'))
    height = int(cfg_parser.get('Display Settings', 'height'))
    gridsize = int(cfg_parser.get('Display Settings', 'gridsize'))
   #screen = pygame.display.set_mode((width, height))
    utils.SCALE = width/gridsize
    utils.GRIDSIZE = gridsize
    #pygame.display.set_caption("Q_Learning_Snake - Lefter Andrei & Lunca Vlad")

    # ---------- Init Game Logic ----------
    gameloop.start(gridsize)
    # ---------- Game Loop ----------
    agent = QAgent()

    while True:
        # ---------- Handle KeyPresses and Other Events ----------
        try:
            # Încercăm să executăm pasul de joc prin AI
            # handle_situation va rula logica de snake.move() care dă eroarea
            gameloop.handle_situation(agent)
        except NotImplementedError:
            gameloop.reset(agent,gridsize)
        # ---------- Update Physics ----------
            #gameloop.update()
        # ---------- Render Window ----------
       # gameloop.render(screen)

if __name__ == '__main__':
    main()
