import sys
from random import randrange
import numpy as np
from QAgent import QAgent
from snake import Snake, Direction, Position
from map import Fruit, Map
import utils
import pygame

import matplotlib.pyplot as plt

from utils import GRIDSIZE

#------ AICI AI TRAINING --------
train_mode = False
#---------------------------------


# ----- Custom Events -----
FRUITSPAWN_EVENT = pygame.USEREVENT + 1
FRUITSPAWN_TIMER = 1000
AGENT_DECISION_EVENT = pygame.USEREVENT + 2
AGENT_DECISION_TIMER = 1 if train_mode else 400
# ------------------------a-

# ----- Agent Stuff ---
decay_rate = 0.999
min_epsilon = 0.01 if train_mode else 0.0
# --------------------

# ------ plot stuff ------------
plt.ion()
fig, ax = plt.subplots()
score_line, = ax.plot([], [], 'r-', alpha=0.5)
mean_line, = ax.plot([], [], 'b-', linewidth=2, label='Scorul Mediu')
ax.set_xlabel('Iteratia')
ax.set_ylabel('Scorul')
ax.set_title('Progresul antrenarii')
AVERAGE_WINDOW_SIZE = 50
all_scores = []
# ------------------------------

BACKGROUNDCOLOR = (168, 198, 78)
player: Snake = None
fruit: Fruit = None
iteration: int = 1
scores: list[int] = []

def handle_events(events: list, agent):
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # if event.type == FRUITSPAWN_EVENT:
        #     global fruit
        #     if fruit.eaten:
        #         x = randrange(utils.GRIDSIZE)
        #         y = randrange(utils.GRIDSIZE)
        #         fruit = Fruit(Position(x, y))
        #         while fruit.position in player.get_postion():
        #             x = randrange(utils.GRIDSIZE)
        #             y = randrange(utils.GRIDSIZE)
        #             fruit = Fruit(Position(x, y))

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
        if event.type == AGENT_DECISION_EVENT:
            handle_situation(agent)

def handle_situation(QAgent):
    global fruit, player
    head_old = player.get_postion()[0]
    dist_old = abs(fruit.position.x - head_old.x) + abs(fruit.position.y - head_old.y)

    state_old = player.get_state(fruit)

    action = QAgent.get_action(state_old, player.facing)
    QAgent.last_action = action
    directions = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]

    player.change_direction(directions[action])

    reward = -0.1

    player.move()
    if player.check_collision_with_fruit(fruit):
        player.grow()
        fruit.eaten = True
        reward = 10
        player.movement_since_last_fruit = 0
        print("Fruct mancat")
        fruit = Fruit(Position(randrange(utils.GRIDSIZE), randrange(utils.GRIDSIZE)))
    else:
        player.movement_since_last_fruit += 1

        #if(player.move()):

    head_new = player.get_postion()[0]
    dist_new = abs(fruit.position.x - head_new.x) + abs(fruit.position.y - head_new.y)
    if player.movement_since_last_fruit > utils.GRIDSIZE * utils.GRIDSIZE:
        reward = -2  # living cost hehe ca sa fie motivat sa caute man care
            # Antrenare
    state_new = player.get_state(fruit)
    QAgent.train(state_old, action, reward, state_new)
    return player.is_alive

def update():
    # -- update game here
    #player.move()
    if player.check_collision_with_fruit(fruit):
        player.grow()
        fruit.eaten = True
    player.move()

def render(screen : pygame.Surface):
    screen.fill((34, 139, 34))
    Map.render(screen)
    player.render(screen)
    if not fruit.eaten:
        fruit.render(screen)
    my_font = pygame.font.SysFont('Comic Sans MS', 30)
    text_surface = my_font.render(f'Score: {player.get_score()}', True, (0, 0, 0))
    screen.blit(text_surface, (0, 0))
    global iteration
    text_surface = my_font.render(f'Iteration: {iteration}', True, (0, 0, 0))
    screen.blit(text_surface, (0, 30))
    # -- render code goes here
    pygame.display.update()

def start(gridsize):
    global player, fruit, speed
    player = Snake(gridsize//2, gridsize//2, Direction.DOWN,  500)#int(4 * utils.SCALE)) if train_mode == False else Snake(gridsize//2, gridsize//2, Direction.DOWN, 0)
    x = randrange(utils.GRIDSIZE)
    y = randrange(utils.GRIDSIZE)
    fruit = Fruit(Position(x, y))
    while fruit.position in player.get_postion():
        x = randrange(utils.GRIDSIZE)
        y = randrange(utils.GRIDSIZE)
        fruit = Fruit(Position(x, y))
    pygame.time.set_timer(FRUITSPAWN_EVENT, FRUITSPAWN_TIMER)

def plot():
    global iteration, scores
    current_score = player.get_score()
    all_scores.append(current_score)
    score_line.set_xdata(range(1, len(all_scores) + 1))
    score_line.set_ydata(all_scores)
    print("Scoruri de 0 pana acum: ", all_scores.count(0))
    if(len(all_scores) > 0):
        window = min(len(all_scores), AVERAGE_WINDOW_SIZE)
        moving_avg = np.convolve(all_scores, np.ones(window) / window, mode='valid')
        mean_line.set_xdata(range(window, len(all_scores) + 1))
        mean_line.set_ydata(moving_avg)

    ax.relim()
    ax.autoscale_view()

    plt.draw()
    plt.pause(0.0001)

def reset(agent: QAgent ,gridsize):
    # Cand se lpveste de cv resetam jocul pt a continua antrenarea
    global iteration, scores
    state_now = player.get_state(fruit)

    plot()

    print(f"========= Iteration {iteration} ==========")
    agent.epsilon = max(agent.epsilon * decay_rate, min_epsilon)
    print("Epsilon: ", agent.epsilon)
    start(gridsize)
    if(iteration % 100 == 0): # salvam o data la 100 de iteratii
        agent.save_model()
    agent.train(state_now, agent.last_action, -10, state_now)
    print("=================================================")
    if iteration == 10000:
        plt.savefig(f"antrenament_{iteration}.png")
        print(f"Graficul a fost salvat ca 'antrenament_{iteration}.png'")
        print(f"--- PAUZA: Iterația {iteration} atinsa ---")
        input("Apasa ORICE pentru a continua antrenamentul...")
    iteration += 1
