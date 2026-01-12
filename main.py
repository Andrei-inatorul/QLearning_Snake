import configparser

import pygame
import gameloop
from QAgent import QAgent
import os
import utils
import sys
import ui
from gameloop import train_mode

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

    gametype = ui.titlescreen(screen)
    ai_mode = False
    if(gametype == 1):
        gameloop.train_mode = False
        ai_mode = False
    elif gametype == 2:
        gameloop.train_mode = True
        ai_mode = True
    elif gametype == 3:
        gameloop.train_mode = False
        ai_mode = True

    # ---------- Init Game Logic ----------
    gameloop.start(gridsize)
    clock = pygame.time.Clock()
    speed = 1000 if gameloop.train_mode else 10
    # ---------- Game Loop ----------
    agent = QAgent(epsilon=0.01 if gameloop.train_mode else 0.0)
   # pygame.time.set_timer(gameloop.AGENT_DECISION_EVENT, gameloop.AGENT_DECISION_TIMER)
    while True:
        # ---------- EVENIMENTE ----------
        gameloop.handle_events(pygame.event.get())
        alive = gameloop.handle_situation(agent) if ai_mode == True else gameloop.update()
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
