from abc import ABC, abstractmethod
import pygame
import utils
from map import Fruit
from utils import Position

class Direction:
    UP = Position(0, -1)
    DOWN = Position(0, 1)
    LEFT = Position(-1, 0)
    RIGHT = Position(1, 0)

class AbstractSnake(ABC):
    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def grow(self):
        pass

    @abstractmethod
    def change_direction(self, direction:Position):
        pass

    @abstractmethod
    def render(self, screen : pygame.Surface):
        pass

    @abstractmethod
    def check_collision(self, other:Position):
        pass

    @abstractmethod
    def check_collision_with_fruit(self, other:Fruit):
        pass

class Snake(AbstractSnake):
    last_move_time = 0
    def __init__(self, initial_x:int, initial_y:int, direction:Position, movespeed:int):
        self._bodyparts: list[Position] = [Position(initial_x, initial_y), Position(initial_x, initial_y-1), Position(initial_x, initial_y-2)]
        self._facing: Position = direction
        self._speed: int = 1
        self.movespeed : int = movespeed
        self._lastfacing : Position = direction

    def check_collision(self, other:Position):
        if other in self._bodyparts[:len(self._bodyparts)-1]:
            return True
        return False

    def get_state(this, fruit):
        head = this._bodyparts[0]

        delta_x = fruit.position.x - head.x
        delta_y = fruit.position.y - head.y


        state = [
            this._facing,
            int(delta_x),
            int(delta_y),
            head.x == 0 or this.check_collision(Position(head.x - 1, head.y)),  # STANGA
            head.x == utils.GRIDSIZE - 1 or this.check_collision(Position(head.x + 1, head.y)),  # dreapta
            head.y == 0 or this.check_collision(Position(head.x, head.y - 1)),  # sus
            head.y == utils.GRIDSIZE - 1 or this.check_collision(Position(head.x, head.y + 1))  # jos
        ]
        return tuple(state)
    def move(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time > self.movespeed:
            new_head = (self._bodyparts[0] + self._facing)# % utils.GRIDSIZE # daca scoti % GRIDSIZE nu mai pleci dintr un capat in altul
            if self.check_collision(new_head) or new_head.x < 0 or new_head.x >= utils.GRIDSIZE or new_head.y < 0 or new_head.y >= utils.GRIDSIZE: # or new_head.x < 0 or new_head.x > GRIDSIZE or new_head.y < 0 or new_head.y > GRIDSIZE
                raise NotImplementedError("Aici trebuie sa pierzi")
                pass  # lose logic here
            self._bodyparts.pop(-1)
            self._bodyparts.insert(0, new_head)
            self.last_move_time = current_time
            self._lastfacing = self._facing


    def grow(self):
        head : Position = self._bodyparts[0]
        new_head : Position = (head + self._facing)# % utils.GRIDSIZE # daca scoti % GRIDSIZE nu mai pleci dintr un capat in altul
        self._bodyparts.insert(0, new_head)

    def change_direction(self, direction:Position):
        if self._lastfacing != (direction * -1):
            self._facing = direction

    def check_collision_with_fruit(self, other:Fruit):
        head = self._bodyparts[0]
        return  head == other.position

    def get_postion(self):
        return self._bodyparts

    def render(self, screen : pygame.Surface):
        size = len(self._bodyparts)
        from colour import Color
        red = Color("orange")
        colors = list(red.range_to(Color("coral"), size))
        for i, bodypart in enumerate(self._bodyparts):
            tile_color = Color.get_rgb(colors[i])
            tile_color = list((tile_color[0]*255, tile_color[1]*255, tile_color[2]*255))
            pygame.draw.rect(screen, tile_color, pygame.Rect(bodypart.x * utils.SCALE, bodypart.y * utils.SCALE, utils.SCALE, utils.SCALE))
            #pygame.draw.circle(screen, (255, 0, 0), (bodypart.x*SCALE+SCALE/2, bodypart.y*SCALE+SCALE/2), SCALE/2)