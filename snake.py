from abc import ABC, abstractmethod
import pygame
from numpy.ma.core import left_shift

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
        self.facing: Position = direction
        self._speed: int = 1
        self.movespeed : int = movespeed
        self.lastfacing : Position = direction
        self.movement_since_last_fruit = 0
        self.will_grow = False
        self.is_alive = True

    def check_collision(self, other:Position):
        if other in self._bodyparts[:len(self._bodyparts)-1]:
            return True
        return False

    def is_unsafe(self, other:Position):
            if other.x < 0 or other.x >= utils.GRIDSIZE or other.y < 0 or other.y >= utils.GRIDSIZE:
                return True # ma lovesc de perete
            return self.check_collision(other) # ma lovesc de mine

    def get_state(this, fruit) -> tuple:
        head = this._bodyparts[0]

        delta_x = fruit.position.x - head.x
        delta_y = fruit.position.y - head.y

        l = Position(head.x - 1, head.y)
        r = Position(head.x + 1, head.y)
        u = Position(head.x, head.y - 1)
        d = Position(head.x, head.y + 1)

        state = (
            delta_x < 0,
            delta_x > 0,
            delta_y < 0,
            delta_y > 0,

            this.facing == Direction.UP,
            this.facing == Direction.DOWN,
            this.facing == Direction.LEFT,
            this.facing == Direction.RIGHT,

            this.is_unsafe(u),
            this.is_unsafe(d),
            this.is_unsafe(l),
            this.is_unsafe(r),
        )
        return tuple(map(int, state))

    def move(self):
        current_time = pygame.time.get_ticks()
        #if current_time - self.last_move_time > self.movespeed:
        new_head = (self._bodyparts[0] + self.facing)# % utils.GRIDSIZE # daca scoti % GRIDSIZE nu mai pleci dintr un capat in altul
        if self.check_collision(new_head) or new_head.x < 0 or new_head.x >= utils.GRIDSIZE or new_head.y < 0 or new_head.y >= utils.GRIDSIZE: # or new_head.x < 0 or new_head.x > GRIDSIZE or new_head.y < 0 or new_head.y > GRIDSIZE
            self.is_alive = False
            return
        if not self.will_grow:
            self._bodyparts.pop(-1)
        else:
            self.will_grow = False
        self._bodyparts.insert(0, new_head)
        self.last_move_time = current_time
        self.lastfacing = self.facing
            #return 1

    def get_score(self) -> int:
        return len(self._bodyparts) - 3
    

    def grow(self):
        self.will_grow = True
        # tail : Position = self._bodyparts[-1]
        # new_head : Position = (tail + self._facing)# % utils.GRIDSIZE # daca scoti % GRIDSIZE nu mai pleci dintr un capat in altul
        # self._bodyparts.insert(-1, new_head)

    def change_direction(self, direction:Position):
        if self.facing == (direction * -1):
            print(direction)
        self.facing = direction

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