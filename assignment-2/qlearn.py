from collections import defaultdict, deque
from random import choice, random

import gymnasium as gym
from gymnasium.envs.toy_text.frozen_lake import generate_random_map

import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.patches import Polygon

import numpy as np

type Action = int
type State = int
type Utility = float
type Exploration = tuple[str, float]
type ConvergenceCriteria = tuple[str, float]

DRAW_STATE_INDEX = True
POSSIBLE_ACTIONS: list[Action] = [0, 1, 2, 3]

# default values, don't change these
SIZE = -1
IS_SLIPPERY = False
RENDER_TO_SCREEN = False

class Agent:
    def __init__(self, environment: gym.Env, exploration: Exploration, alpha: float = 0.1, gamma: float = 0.9):
        self.alpha = alpha
        self.gamma = gamma

        self.environment = environment
        self.state_representation = [cell.decode("utf-8") for row in environment.unwrapped.desc for cell in row] if environment else [] # pyright: ignore[reportAttributeAccessIssue]

        self.q_table = defaultdict(float) # default value for Q(s, a) is 0

        # set the exploration function based on exploration
        if exploration[0] == "random":
            self.act = self._act_random
        elif exploration[0] == "epsilon_greedy":
            self.act = self._act_epsilon_greedy
            self.epsilon_greedy_param = exploration[1]
        elif exploration[0] == "state_counting":
            self.act = self._act_state_counting
            self.compute_q = self._compute_q_state_counting
            self.state_counts = defaultdict(lambda: 1)
            self.state_counting_param = exploration[1]
        else:
            raise ValueError("Invalid ExplorationType")
    
    def act(self, s: State) -> Action:
        raise NotImplementedError("Agent.act was not set, possibly invalid ExplorationType")

    # randomly pick an action every time
    def _act_random(self, s: State) -> Action:
        return choice(POSSIBLE_ACTIONS)
    
    # randomly pick with p = epsilon_greedy_param, otherwise use policy
    def _act_epsilon_greedy(self, s: State) -> Action:
        if random() < self.epsilon_greedy_param:
            return choice(POSSIBLE_ACTIONS)
        else:
            return self.pi(s)
    
    def _state_counting_f(self, s: State, a: Action): # takes s, a instead of u, n for code brevity
        return self.q(s, a) + self.state_counting_param / self.state_counts[(s, a)]

    def _max_state_counting_f(self, s: State) -> Utility:
        return max([self._state_counting_f(s, a) for a in POSSIBLE_ACTIONS])

    def _compute_q_state_counting(self, s: State, a: Action, r: Utility, s_prime: State) -> float:
        old_q_value = self.q_table[(s, a)]
        new_q_value = (1 - self.alpha) * self.q(s, a) + self.alpha * (r + self.gamma * self._max_state_counting_f(s_prime))
        self.q_table[(s, a)] = new_q_value

        return abs(new_q_value - old_q_value)

    # exploration function outlined in class
    def _act_state_counting(self, s: State) -> Action:
        best_utility = self._max_state_counting_f(s)
        best_actions = [a for a in POSSIBLE_ACTIONS if self._state_counting_f(s, a) == best_utility]
        a = choice(best_actions)

        self.state_counts[(s, a)] += 1
        return a

    # find max over a of q(s, a)
    def _max_q_value(self, s: State) -> Utility:
        return max([self.q(s, a) for a in POSSIBLE_ACTIONS])
    
    def _average_q_value(self, s: State) -> Utility:
        return sum([self.q(s, a) for a in POSSIBLE_ACTIONS]) / len(POSSIBLE_ACTIONS)

    # perform a step of q learning, returning difference between old and updated q value
    def compute_q(self, s: State, a: Action, r: Utility, s_prime: State) -> float:
        old_q_value = self.q_table[(s, a)]
        new_q_value = (1 - self.alpha) * self.q(s, a) + self.alpha * (r + self.gamma * self._max_q_value(s_prime))
        self.q_table[(s, a)] = new_q_value
        
        return abs(new_q_value - old_q_value)
    
    def q(self, s: State, a: Action) -> Utility:
        return self.q_table[(s, a)]
    
    # find arg max over a of q(s, a)
    def pi(self, s: State) -> Action:
        return choice(self._best_actions(s))
    
    def _best_actions(self, s: State) -> list[Action]:
        best_q_value = self._max_q_value(s)
        best_actions = [action for action in POSSIBLE_ACTIONS if self.q(s, action) == best_q_value]

        return best_actions
    
    # returns the policy as a string
    def get_policy_representation(self) -> str:
        policy = []
        for i, s in enumerate(self.state_representation):
            if s == "H": # we don't care what action is taken on hole and goal states
                policy.append("h")
            if s == "G":
                policy.append("g")
            else:
                best_actions = self._best_actions(i)
                if len(best_actions) == 4:
                    policy.append("?")
                else:
                    policy.append(str(self.pi(i)))
        return "".join(policy) # concat into a single string

    def show_q_table(self):
        cmap = plt.colormaps["winter"] # thematic
        _, ax = plt.subplots(figsize = (6, 6))

        # this line of code is awesome
        q_values = [self.q(row * SIZE + column, action) for row in range(SIZE) for column in range(SIZE) for action in POSSIBLE_ACTIONS]
        q_min = min(q_values)
        q_max = max(q_values)

        for row in range(SIZE):
            for column in range(SIZE):
                s = row * SIZE + column
                x0, y0 = column, (SIZE - 1) - row
                cx, cy = x0 + 0.5, y0 + 0.5 # center of cell

                if self.state_representation[s] == 'H': # if hole, draw red square
                    ax.add_patch(Polygon([(x0, y0), (x0, y0 + 1), (x0 + 1, y0 + 1), (x0 + 1, y0)], facecolor = "red"))
                elif self.state_representation[s] == 'G': # if goal, draw green square
                    ax.add_patch(Polygon([(x0, y0), (x0, y0 + 1), (x0 + 1, y0 + 1), (x0 + 1, y0)], facecolor = "green"))
                else: # otherwise, draw q values
                    triangles = {
                        0: [(x0, y0), (x0, y0 + 1), (cx, cy)], # left
                        1: [(x0, y0), (x0 + 1, y0), (cx, cy)], # down
                        2: [(x0 + 1, y0), (x0 + 1, y0 + 1), (cx, cy)], # right
                        3: [(x0, y0 + 1), (x0 + 1, y0 + 1), (cx, cy)] # up
                    }

                    q_values = [(action, self.q(s, action)) for action in POSSIBLE_ACTIONS] # (a, q(s, a))
                    best_q_value = max([q_value[1] for q_value in q_values])
                    for q_value in q_values:
                        action, value = q_value
                        norm_value = (value - q_min) / (q_max - q_min) if q_max != q_min else 0.5
                        color = cmap(norm_value)
                        if value == best_q_value: # use hatching on the best action, i.e. the one the policy will follow
                            triangle = Polygon(triangles[action], facecolor = color, hatch = "|", edgecolor = "white", linewidth = 0)
                        else: # otherwise just draw normally
                            triangle = Polygon(triangles[action], facecolor = color)
                        ax.add_patch(triangle)
                
                if DRAW_STATE_INDEX:
                    ax.text(cx, cy, str(s)) # draw state index
        
        ax.set_xlim(0, SIZE)
        ax.set_ylim(0, SIZE)
        ax.set_aspect("equal")
        ax.axis("off")

        # have to do weird things with the normalization to make it work with the colormaps idk
        # matplotlib is weird
        sm = plt.cm.ScalarMappable(cmap = cmap, norm = colors.Normalize(vmin = q_min, vmax = q_max))
        sm.set_array([])
        plt.colorbar(sm, ax = ax, fraction = 0.046, pad = 0.04, label = "Q-Value")

        plt.tight_layout()
        plt.show()

class LearningEnvironment:
    episode_r = 0.0
    rewards_queue_length = 50

    def __init__(self, agent: Agent, convergence_criteria: ConvergenceCriteria):
        self.agent = agent
        self.env = agent.environment

        if convergence_criteria[0] == "none":
            self.test_convergence = self._test_convergence_none
        elif convergence_criteria[0] == "policy_delta":
            self.previous_policy = "x" * len(self.agent.state_representation)
            self.policy_delta_param = convergence_criteria[1]
            self.test_convergence = self._test_convergence_policy_delta
        elif convergence_criteria[0] == "v_delta":
            self.previous_v_values = [0.0] * len(self.agent.state_representation)
            self.v_delta_param = convergence_criteria[1]
            self.test_convergence = self._test_convergence_v_delta
        else:
            raise ValueError("Invalid ConvergenceCriteria")

    def compute_q(self, s: State, a: Action, r: Utility, s_prime: State) -> float:
        self.episode_r = self.episode_r + 0.1 * r
        return self.agent.compute_q(s, a, r, s_prime)

    def test_convergence(self):
        raise NotImplementedError("LearningEnvironment.test_convergence was not set, possibly invalid ConvergenceCriteria")

    def _test_convergence_none(self):
        return False

    def _test_convergence_policy_delta(self):
        if not self.has_won:
            return False
        if hasattr(self.agent, "state_counting_param"): # performs additional checks if using state counting
            if sum(self.agent.state_counts.values()) / len(self.agent.state_counts) < 2:
                return False

        policy = self.agent.get_policy_representation()

        delta = 0
        delta_states = []
        for s in range(len(self.agent.state_representation)):
            if policy[s] != self.previous_policy[s]:
                delta_states.append(f"{s}: ({policy[s], self.previous_policy[s]})")
                delta += 1
        self.previous_policy = policy
        
        if self.episode % 1_000 == 0:
            print(f"policy_delta: {delta}")
            print(f"delta_states: {delta_states}")

        if delta == 0: # policy converged!
            self.converged_episodes += 1
            # iterate for another policy_delta_param episodes to ensure its really converged
            if self.converged_episodes >= self.policy_delta_param:
                return True
        else:
            self.converged_episodes = 0
            return False

    def _test_convergence_v_delta(self):
        if self.episode < 100 or not self.has_won:
            return False

        v_values = [self.agent._average_q_value(s) for s in range(len(self.agent.state_representation))]
        v_deltas = [abs(x - y) for x, y in zip(v_values, self.previous_v_values)]
        self.previous_v_values = v_values

        if self.episode % 1_000 == 0:
            print(f"v_delta: {sum(v_deltas) / len(v_deltas)}")

        # check if every delta is below some epsilon
        for delta in v_deltas:
            if delta > self.v_delta_param: # greater than some epsilon
                return False
        return True

    def learn(self, show_q_table = True) -> int:
        self.has_won = False
        self.episode = 0
        steps = 0

        s, _ = self.env.reset()
        for steps in range(1_000_000): # take no more than 1,000,000 steps in case it doesn't converge in time
            a = self.agent.act(s)
            prev_s = s

            s, r, terminated, truncated, _ = self.env.step(a)
            self.compute_q(prev_s, a, float(r), s)
            steps += 1

            if terminated or truncated:
                if IS_SLIPPERY:
                    self.agent.alpha *= 0.9999 # anneal alpha

                if float(r) > 0:
                    self.has_won = True
                if self.test_convergence():
                    break

                s, _ = self.env.reset()
                self.episode += 1
        
        print(f"Converged after {self.episode} episodes taking {steps} steps")
        if show_q_table:
            self.agent.show_q_table()
        
        return self.episode

def learn(
    size: int,
    success_rate: float,
    alpha: float,
    gamma: float,
    exploration: Exploration,
    convergence_criteria: ConvergenceCriteria,
    reward_schedule: tuple[float, float, float] = (10, -10, 0)
):
    global SIZE, IS_SLIPPERY

    SIZE = size
    IS_SLIPPERY = False if success_rate == 1 else True
    
    env = gym.make(
        "FrozenLake-v1",
        render_mode = None,
        desc = generate_random_map(size = SIZE),
        is_slippery = IS_SLIPPERY,
        success_rate = success_rate,
        reward_schedule = reward_schedule
    )
    agent = Agent(env, exploration, alpha, gamma)
    learning_environment = LearningEnvironment(agent, convergence_criteria)

    return learning_environment.learn(True)

def main():
    # modify these lines below
    # or "import learn from qlearn" from a different python file
    SIZE = 4 # SIZE x SIZE map
    IS_SLIPPERY = False
    RENDER_TO_SCREEN = False

    env = gym.make(
        "FrozenLake-v1",
        render_mode = "human" if RENDER_TO_SCREEN else None,
        desc = generate_random_map(size = SIZE), # randomly generates a map
        #map_name = "4x4", # remember to change SIZE = 4
        #map_name = "8x8", # remember to change SIZE = 8
        is_slippery = IS_SLIPPERY,
        success_rate = 0.75,
        reward_schedule = (10, -10, 0)
    )

    """
    Exploration parameter values:
    ("epsilon_greedy", p) where p is the probability of taking a random action instead of following policy
    ("state_counting", k) where k is the state counting parameter; k = 1 works ok (for whatever reason)
    """

    if IS_SLIPPERY:
        agent = Agent(env, ("epsilon_greedy", 0.1), alpha = 0.05, gamma = 0.9)
    else:
        agent = Agent(env, ("state_counting", 1), alpha = 1, gamma = 0.9)

    """
    ConvergenceCriteria parameter values:
    ("none", ...) doesn't check for criteria, instead taking the max number of steps every time
    ("policy_delta", n) checks for criteria if the policy doesn't change for at least n episodes; try n = 2
    ("v_delta", e) checks if the difference between every average Q value between two consecutive runs is less than some epsilon
    """

    #learning_environment = LearningEnvironment(agent, ("none", 0))
    learning_environment = LearningEnvironment(agent, ("policy_delta", 3))
    #learning_environment = LearningEnvironment(agent, ("v_delta", 0.0001))
    learning_environment.learn(True)

if __name__ == "__main__":
    main()
