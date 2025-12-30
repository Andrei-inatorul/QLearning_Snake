import random
import json
import os
from snake import Direction

class QAgent:
    def __init__(self, filename="snake_brain.json", epsilon = 1.0):
        self.last_action = None
        self.q_table = {}  # Dicționar: {stare: [scor_sus, scor_jos, scor_stanga, scor_dreapta]}
        self.lr = 0.1
        self.gamma = 0.9
        self.epsilon = epsilon
        self.filename=filename
        self.load_model()
        self.explore_rate = 10000


    def get_action(self, state, current_direction):
        """Alege o acțiune bazată pe starea curentă."""
        state_str = str(state)

        if state_str not in self.q_table:
            self.q_table[state_str] = [0.0, 0.0, 0.0, 0.0]
        rand = random.random()
        directions = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]

        interzis = -1
        for i, d in enumerate(directions):
            if d == current_direction * -1:
                interzis = i
                break

        actiuni_valide = [i for i in range(4) if i != interzis]
        if rand < self.epsilon:
            return random.choice(actiuni_valide)
        else:
            state_values = list(self.q_table[state_str])
            masked_values = []
            for i in range(4):
                if i == interzis:
                    masked_values.append(-float('inf'))  # Impossible to pick
                else:
                    masked_values.append(state_values[i])

            return masked_values.index(max(masked_values))

    def train(self, state, action, reward, next_state):
        if action is None:
            return
        state_str = str(state)
        next_state_str = str(next_state)
        self.last_action=action
        if next_state_str not in self.q_table:
            self.q_table[next_state_str] = [0, 0, 0, 0]

        # Formula Q-Learning: Q(s,a) = Q(s,a) + lr * [R + gamma * max(Q(s',a')) - Q(s,a)]
        old_value = self.q_table[state_str][action]
        next_max = max(self.q_table[next_state_str])

        new_value = old_value + self.lr * (reward + self.gamma * next_max - old_value)
        self.q_table[state_str][action] = new_value

    def save_model(self):
        with open(self.filename, 'w') as f:
            json.dump(self.q_table, f)
        print(f"Model salvat! Stari cunoscute: {len(self.q_table)}")

    def load_model(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    self.q_table = json.load(f)
                print(f"Model încărcat cu succes! ({len(self.q_table)} stări)")
            except:
                print("Eroare la încărcarea fișierului JSON. Se începe de la zero.")