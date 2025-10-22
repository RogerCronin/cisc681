from collections import defaultdict
from math import inf
from random import choice, random
from typing import Literal

import gymnasium as gym
from gymnasium.envs.toy_text.frozen_lake import generate_random_map

type Action = int
type State = int
type Reward = float
type Exploration = Literal["random"] | tuple[Literal["epsilon_greedy"], float] | Literal["state_counting"]

SIZE = 4
RENDER_TO_SCREEN = True

class Agent:
    epsilon_greedy_param = 0.05

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

env = gym.make(
    "FrozenLake-v1",
    render_mode = "human" if RENDER_TO_SCREEN else None,
    desc = generate_random_map(size = SIZE),
    is_slippery = True,
    success_rate = 0.75,
    reward_schedule = (10, -10, 0)
)
agent = Agent([0, 1, 2, 3], ("epsilon_greedy", 0.05))

s, info = env.reset(seed = 67)
for _ in range(1000):
    action = agent.act(s)
    prev_s = s

    s, r, terminated, truncated, info = env.step(action)
    if terminated or truncated:
        observation, info = env.reset()

env.close()
