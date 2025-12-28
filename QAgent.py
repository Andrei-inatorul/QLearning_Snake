import random
import json
import os


class QAgent:
    def __init__(self, filename="snake_brain.json"):
        self.last_action = None
        self.q_table = {}  # Dicționar: {stare: [scor_sus, scor_jos, scor_stanga, scor_dreapta]}
        self.lr = 0.1
        self.gamma = 0.9
        self.epsilon = 0.1
        self.filename=filename
        self.load_model()



    def get_action(self, state):
        """Alege o acțiune bazată pe starea curentă."""
        state_str = str(state)

        if state_str not in self.q_table:
            self.q_table[state_str] = [0, 0, 0, 0]

        if random.random() < self.epsilon:
            return random.randint(0, 3)
        else:
            state_values = self.q_table[state_str]
            return state_values.index(max(state_values))

    def train(self, state, action, reward, next_state):
        if action is None:
            return
        state_str = str(state)
        next_state_str = str(next_state)
        self.last_action=action;
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