import sys
from random import randrange

from snake import Snake, Direction, Position
from map import Fruit, Map
import utils
import pygame

# ----- Custom Events -----
FRUITSPAWN_EVENT = pygame.USEREVENT + 1
FRUITSPAWN_TIMER = 1000
# ------------------------a-

BACKGROUNDCOLOR = (168, 198, 78)

player: Snake = None
fruit: Fruit = None

def handle_events(events: list):
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


def handle_situation(QAgent):
    global fruit
    head_old = player.get_postion()[0]
    dist_old = abs(fruit.position.x - head_old.x) + abs(fruit.position.y - head_old.y)

    state_old = player.get_state(fruit)

    action = QAgent.get_action(state_old)
    QAgent.last_action = action

    directions = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
    player.change_direction(directions[action])

    player.move()

    head_new = player.get_postion()[0]
    dist_new = abs(fruit.position.x - head_new.x) + abs(fruit.position.y - head_new.y)

    reward = 0
    if player.check_collision_with_fruit(fruit):
        player.grow()
        fruit.eaten = True
        reward = 100
        print("Fruct mancat")
        fruit = Fruit(Position(randrange(utils.GRIDSIZE), randrange(utils.GRIDSIZE)))
    else:
        if dist_new < dist_old:
            reward = 0.01
        else:
            reward = -0.2

    # Antrenare
    state_new = player.get_state(fruit)
    QAgent.train(state_old, action, reward, state_new)

def update():
    # -- update game here
   #d player.move()
    if player.check_collision_with_fruit(fruit):
        player.grow()
        fruit.eaten = True
    else:
        player.move()
    pass

def render(screen : pygame.Surface):
    screen.fill((34, 139, 34))
    Map.render(screen)
    player.render(screen)
    if not fruit.eaten:
        fruit.render(screen)
    my_font = pygame.font.SysFont('Comic Sans MS', 30)
    text_surface = my_font.render(f'Score: {player.get_score()}', True, (0, 0, 0))
    screen.blit(text_surface, (0, 0))
    # -- render code goes here
    pygame.display.update()

def start(gridsize):
    global player, fruit
    player = Snake(gridsize//2, gridsize//2, Direction.DOWN,int(4 * utils.SCALE))
    fruit = Fruit(utils.Position(2, 2))
    pygame.time.set_timer(FRUITSPAWN_EVENT, FRUITSPAWN_TIMER)

def reset(agent,gridsize):
    # Cand se lpveste de cv resetam jocul pt a continua antrenarea
    state_now = player.get_state(fruit)
    agent.train(state_now, agent.last_action, -100, state_now)
    print("score:" + agent.getScore(state_now))
    start(gridsize)
    agent.save_model()