from collections import defaultdict
from random import choice, random
from typing import Literal

import gymnasium as gym
from gymnasium.envs.toy_text.frozen_lake import generate_random_map

import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.patches import Polygon

type Action = int
type State = int
type Reward = float
type Exploration = Literal["random"] | tuple[Literal["epsilon_greedy"], float] | Literal["state_counting"]

SIZE = 4
RENDER_TO_SCREEN = False
POSSIBLE_ACTIONS = [0, 1, 2, 3]

class Agent:
    epsilon_greedy_param = 0.1

    def __init__(self, possible_actions: list[Action], exploration: Exploration, alpha: float = 0.2, gamma: float = 0.9):
        self.alpha = alpha
        self.gamma = gamma
        self.possible_actions = possible_actions
        self._q_table = defaultdict(float) # default value for Q(s, a) is 0
        # set the exploration function based on exploration_type
        if exploration == "random":
            self.act = self.act_random
        elif exploration == "state_counting":
            self.act = self.act_state_counting
        elif not hasattr(exploration, "__getitem__"): # checks if Exploration is a sequence-like
            raise ValueError("Invalid ExplorationType")
        elif exploration[0] == "epsilon_greedy":
            self.act = self.act_epsilon_greedy
            self.epsilon_greedy_param = exploration[1]
        else:
            raise ValueError("Invalid ExplorationType")
    
    def act(self, s: State) -> Action:
        raise NotImplementedError("Agent.act was not set, possibly invalid ExplorationType")

    # randomly pick an action every time
    def act_random(self, s: State) -> Action:
        return choice(self.possible_actions)
    
    # randomly pick with p = epsilon_greedy_param, otherwise use policy
    def act_epsilon_greedy(self, s: State) -> Action:
        if random() < self.epsilon_greedy_param:
            return choice(self.possible_actions)
        else:
            return self.pi(s)
    
    # exploration function outlined in class
    def act_state_counting(self, s: State) -> Action:
        ...

    # perform a step of q learning
    def compute_q(self, s: State, a: Action, r: Reward, s_prime: State):
        self._q_table[(s, a)] = (1 - self.alpha) * self.q(s, a) + self.alpha * (r + self.gamma * self.pi(s_prime))
    
    def q(self, s: State, a: Action) -> Reward:
        return self._q_table[(s, a)]
    
    # find arg max over a of q(s, a)
    def pi(self, s: State) -> Action:
        best_q_value = max([self.q(s, action) for action in self.possible_actions])
        best_actions = [action for action in self.possible_actions if self.q(s, action) == best_q_value]

        return choice(best_actions)

    def print_q_table(self):
        for row in range(SIZE):
            for column in range(SIZE):
                state = row * SIZE + column
                for action in self.possible_actions:
                    print(f"({state}, {action}): {self.q(state, action)}")

    # this code is adapted from asking ChatGPT to draw an NxN grid where each cell is made of four direcitonal triangles
    def show_q_table(self):
        cmap = plt.colormaps["viridis"]
        _, ax = plt.subplots(figsize = (6, 6))

        q_values = [self.q(row * SIZE + column, action) for row in range(SIZE) for column in range(SIZE) for action in self.possible_actions]
        q_min = min(q_values)
        q_max = max(q_values)

        for row in range(SIZE):
            for column in range(SIZE):
                s = row * SIZE + column

                x0, y0 = column, 3 - row
                cx, cy = x0 + 0.5, y0 + 0.5

                triangles = {
                    0: [(x0, y0), (x0, y0 + 1), (cx, cy)], # left
                    1: [(x0, y0), (x0 + 1, y0), (cx, cy)], # down
                    2: [(x0 + 1, y0), (x0 + 1, y0 + 1), (cx, cy)], # right
                    3: [(x0, y0 + 1), (x0 + 1, y0 + 1), (cx, cy)] # up
                }

                for action in self.possible_actions:
                    value = self.q(s, action)
                    norm_value = (value - q_min) / (q_max - q_min) if q_max != q_min else 0.5
                    color = cmap(norm_value)
                    triangle = Polygon(triangles[action], color = color)
                    ax.add_patch(triangle)
        
        ax.set_xlim(0, SIZE)
        ax.set_ylim(0, SIZE)
        ax.set_aspect("equal")
        ax.axis("off")

        sm = plt.cm.ScalarMappable(cmap = cmap, norm = colors.Normalize(vmin = q_min, vmax = q_max))
        sm.set_array([])
        plt.colorbar(sm, ax = ax, fraction = 0.046, pad = 0.04, label = "Q-Value")

        plt.tight_layout()
        plt.show()

env = gym.make(
    "FrozenLake-v1",
    render_mode = "human" if RENDER_TO_SCREEN else None,
    #desc = generate_random_map(size = SIZE),
    map_name = "4x4",
    is_slippery = True,
    success_rate = 0.75,
    reward_schedule = (10, -10, 0)
)
agent = Agent(POSSIBLE_ACTIONS, ("epsilon_greedy", 0.05))

s, info = env.reset()
for _ in range(1_000_000):
    action = agent.act(s)
    prev_s = s

    s, r, terminated, truncated, info = env.step(action)
    agent.compute_q(prev_s, action, float(r), s)

    if terminated or truncated:
        s, info = env.reset()

agent.show_q_table()
env.close()
