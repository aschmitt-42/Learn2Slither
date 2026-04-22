import random

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)


REWARD_DEAD = -50
REWARD_NOTHING = -0.1
REWARD_RED_APPLE = -5
REWARD_GREEN_APPLE = 20

FREE_SPACE = "0"


class Board:
    def __init__(self, rows=10, cols=10):
        self.rows = rows
        self.cols = cols
        self.snake = []
        self.red_apple = (0, 0)
        self.green_apples = []
        self.snake = self._init_snake()
        self.red_apple = self._random_empty_cell()
        self.green_apples.append(self._random_empty_cell())
        self.green_apples.append(self._random_empty_cell())

    def _random_empty_cell(self):
        while True:
            pos = (random.randint(0, self.rows - 1),
                   random.randint(0, self.cols - 1))
            if (pos in self.snake):
                continue
            if (pos in self.green_apples):
                continue
            if (pos == self.red_apple):
                continue
            return pos

    def _init_snake(self):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while True:
            head = self._random_empty_cell()
            dx, dy = random.choice(directions)

            segment1 = (head[0] + dx, head[1] + dy)
            segment2 = (head[0] + (2 * dx), head[1] + (2 * dy))

            if (
                0 <= segment1[0] < self.rows and 0 <= segment1[1] < self.cols
                    and 0 <= segment2[0] < self.rows
                    and 0 <= segment2[1] < self.cols
            ):
                return [head, segment1, segment2]

    def get_current_direction(self):
        if (len(self.snake) < 2):
            return None
        head = self.snake[0]
        neck = self.snake[1]
        return (head[0] - neck[0], head[1] - neck[1])

    def display_terminal(self):
        print("W" * (self.cols + 2))
        for row in range(self.rows):
            line = "W"
            for col in range(self.cols):
                pos = (row, col)
                if pos == self.snake[0]:
                    line += "H"
                elif pos in self.snake[1:]:
                    line += "S"
                elif pos == self.red_apple:
                    line += "R"
                elif pos in self.green_apples:
                    line += "G"
                else:
                    line += FREE_SPACE
            line += 'W'
            print(line)
        print("W" * (self.cols + 2))

    def move(self, dir):
        done = False
        reward = 0
        new_head = (self.snake[0][0] + dir[0], self.snake[0][1] + dir[1])

        if not (0 <= new_head[0] < self.rows and 0 <= new_head[1] < self.cols):
            done = True
            reward = REWARD_DEAD
        elif new_head in self.snake[1:]:
            done = True
            reward = REWARD_DEAD
        elif new_head in self.green_apples:
            reward = REWARD_GREEN_APPLE
            self.green_apples.remove(new_head)
            self.snake.insert(0, new_head)
            self.green_apples.append(self._random_empty_cell())
        elif new_head == self.red_apple:
            self.snake.insert(0, new_head)
            self.snake.pop()
            self.snake.pop()
            if len(self.snake) == 0:
                done = True
                reward = REWARD_DEAD
            else:
                reward = REWARD_RED_APPLE
                self.red_apple = self._random_empty_cell()
        else:
            self.snake.insert(0, new_head)
            self.snake.pop()                 # avance sans grandir
            reward = REWARD_NOTHING

        return done, reward

    def _cell_symbol(self, pos):
        if pos == self.snake[0]:
            return "H"
        if pos in self.snake[1:]:
            return "S"
        if pos == self.red_apple:
            return "R"
        if pos in self.green_apples:
            return "G"
        return FREE_SPACE

    def get_rayons(self):
        if (len(self.snake) == 0):
            return None
        head = self.snake[0]
        rays = {
            "NORD": ["H"],
            "SUD": ["H"],
            "OUEST": ["H"],
            "EST": ["H"],
        }

        directions = {
            "NORD": UP,
            "SUD": DOWN,
            "OUEST": LEFT,
            "EST": RIGHT,
        }

        for name, (dr, dc) in directions.items():
            r, c = head
            while True:
                r += dr
                c += dc
                if not (0 <= r < self.rows and 0 <= c < self.cols):
                    break
                rays[name].append(self._cell_symbol((r, c)))

        for name, r in rays.items():
            r.remove("H")
            r.append("W")

        return rays

    def get_state(self):
        if (len(self.snake) == 0):
            return None
        r = self.get_rayons()

        def pad(ray, n=3):
            extended = ray + ['W'] * n
            return tuple(extended[:n])
        return (
            *pad(r["NORD"]),
            *pad(r["SUD"]),
            *pad(r["OUEST"]),
            *pad(r["EST"]),
            self.get_current_direction()
        )

    def display_vision(self, action):
        print(action, "\n")
        rays = self.get_rayons()

        Nord = rays["NORD"]
        Sud = rays["SUD"]
        Ouest = rays["OUEST"]
        Est = rays["EST"]

        head_column = len(Ouest)

        for cell in reversed(Nord):
            print(" " * head_column + cell)

        horizontal = "".join(cell for cell in reversed(Ouest))
        horizontal += "H"
        horizontal += "".join(cell for cell in Est)
        print(horizontal)

        for cell in Sud:
            print(" " * head_column + cell)
        print()
