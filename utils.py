SCALE = 0
GRIDSIZE = 0
WRAPAROUND = False

class Position():
    def __init__(self, x:float, y:float):
        self.x : float = x
        self.y : float = y
    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)
    def __mul__(self, other: float):
        return Position(self.x * other, self.y * other)
    def __mod__(self, other: int):
        return Position(self.x % other, self.y % other)
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __str__(self):
        return f'({self.x}, {self.y})'