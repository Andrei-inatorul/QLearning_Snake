import configparser

import pygame
import gameloop
from QAgent import QAgent

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
    screen = pygame.display.set_mode((width, height))
    utils.SCALE = width/gridsize
    utils.GRIDSIZE = gridsize
    pygame.display.set_caption("Q_Learning_Snake - Lefter Andrei & Lunca Vlad")

    # ---------- Init Game Logic ----------
    gameloop.start(gridsize)
    clock = pygame.time.Clock()
    speed = 1000 if gameloop.train_mode else 10
    # ---------- Game Loop ----------
    agent = QAgent(epsilon=1.0 if gameloop.train_mode else 0.0)
   # pygame.time.set_timer(gameloop.AGENT_DECISION_EVENT, gameloop.AGENT_DECISION_TIMER)
    while True:
        # ---------- Handle KeyPresses and Other Events ----------
        gameloop.handle_events(pygame.event.get())
        alive = gameloop.handle_situation(agent)
        if not alive:
            gameloop.reset(agent, gridsize)
        # try:
        #     pass
        #     # Încercăm să executăm pasul de joc prin AI
        #     # handle_situation va rula logica de snake.move() care dă eroarea
        #    # gameloop.handle_situation(agent)
        #     gameloop.handle_events(pygame.event.get(), agent)
        # except NotImplementedError:
        #     gameloop.reset(agent,gridsize)
        # ---------- Update Physics ----------
        #gameloop.update()
        # ---------- Render Window ----------
        gameloop.render(screen)
        clock.tick(speed)

if __name__ == '__main__':
    main()
