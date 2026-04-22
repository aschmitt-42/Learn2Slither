import json
import random

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)


class Agent:
    def __init__(self):
        self.alpha = 0.1    # Learning rate
        self.gamma = 0.9    # Discount factor
        self.epsilon = 1.0  # Exploration au départ
        self.epsilon_decay = 0.99988
        self.epsilon_min = 0.01
        self.Q_table = {}  # état: [q_up, q_down, q_left, q_right]

    def get_q(self, state):
        if state not in self.Q_table:
            self.Q_table[state] = [0, 0, 0, 0]
        return self.Q_table[state]

    def choose_action(self, state):
        rand = random.random()
        if rand < self.epsilon:
            return random.randint(0, 3)
        else:
            q_values = self.get_q(state)
            return q_values.index(max(q_values))

    def update(self, state, action, reward, next_state, done):
        current = self.get_q(state)[action]
        if done:
            target = reward
        else:
            target = reward + self.gamma * max(self.get_q(next_state))
        self.Q_table[state][action] = current + self.alpha * (target - current)
        # self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

    def save(self, path):
        tmp = {str(key): value for key, value in self.Q_table.items()}
        with open(path, "w", encoding="utf-8") as file:
            json.dump(tmp, file, indent=4)

    def load(self, path):
        with open(path, "r", encoding="utf-8") as file:
            loaded_q_table = json.load(file)

        self.Q_table = {eval(key): value
                        for key, value in loaded_q_table.items()}
