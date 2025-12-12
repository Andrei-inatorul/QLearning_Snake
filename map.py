import pygame
from utils import Position
import utils

class Fruit():
    eaten = False
    def __init__(self, position: Position):
        self.position = position
        self._image = pygame.image.load('./Assets/fruit.png')
        self._image = pygame.transform.scale(self._image, (utils.SCALE, utils.SCALE))

    def render(self, surface: pygame.Surface):
        surface.blit(self._image, (self.position.x * utils.SCALE, self.position.y * utils.SCALE))


class Map():
    @staticmethod
    def Render(screen: pygame.Surface):
        for i in range(0, utils.GRIDSIZE):
            for j in range(0, utils.GRIDSIZE):
                if j&1 == i&1:
                    pygame.draw.rect(screen, (16, 120, 0), pygame.Rect(i * utils.SCALE, j * utils.SCALE, utils.SCALE,
                                                                       utils.SCALE))